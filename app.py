import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from datetime import datetime
import tempfile
import os
from pathlib import Path
from exporters import ExportadorWord, ExportadorPDF, ExportadorPNG

# Configuração da página
st.set_page_config(
    page_title="Gerador de Gráficos GO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título e descrição
st.markdown("""
    <div class="header">
        <h1>📊 Gerador de Gráficos de Monitoramento GO</h1>
        <p>Gere gráficos de monitoramento R-2000 e R-4000 a partir de seus dados</p>
    </div>
""", unsafe_allow_html=True)

# Barra lateral com instruções
with st.sidebar:
    st.header("📋 Instruções")
    st.markdown("""
    ### Como usar:
    
    1. **Cole seus dados** na área de texto abaixo
    2. **Selecione as opções** de geração
    3. **Clique em "Gerar Gráficos"**
    4. **Baixe os arquivos** nos formatos desejados
    
    ### Formato esperado:
    - Dados em formato tabular (Tab-separated ou CSV)
    - Colunas: Município, Inscrição, Descrição/Órgão, Série, Meses (01/2025 a 12/2025)
    - Status válidos: C/ MOV, SEM MOVIMENTO, -, EM ANDAMENTO, SEM PROCURAÇÃO
    
    ### Formatos de exportação:
    - 📄 **Word (DOCX)** - Relatório completo com gráficos
    - 🖼️ **PNG** - Imagens dos gráficos
    - 📑 **PDF** - Documento com gráficos
    """)

# Seção de entrada de dados
st.header("📥 Entrada de Dados")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Cole seus dados aqui:")
    data_input = st.text_area(
        "Dados em formato tabular (Tab-separated ou CSV)",
        height=200,
        placeholder="Cole aqui seus dados...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Exemplo de formato:")
    example_data = """Município	Inscrição	Descrição	Série	01/2025	02/2025
Amaralina	14756596	FMAS	R-2000	C/ MOV	SEM MOV"""
    st.code(example_data, language="text")

# Configurações de geração
st.header("⚙️ Configurações")

col1, col2, col3 = st.columns(3)

with col1:
    gerar_r2000 = st.checkbox("Gerar R-2000", value=True)

with col2:
    gerar_r4000 = st.checkbox("Gerar R-4000", value=True)

with col3:
    incluir_municipios = st.multiselect(
        "Municípios (deixe vazio para todos):",
        options=[]
    )

# Formatos de exportação
st.subheader("📦 Formatos de Exportação")

col1, col2, col3 = st.columns(3)

with col1:
    exportar_word = st.checkbox("Word (DOCX)", value=True)

with col2:
    exportar_png = st.checkbox("PNG", value=True)

with col3:
    exportar_pdf = st.checkbox("PDF", value=True)

# Função para processar dados
def processar_dados(data_raw):
    """Processa dados brutos em DataFrame"""
    try:
        # Tenta ler como tab-separated
        df = pd.read_csv(io.StringIO(data_raw), sep='\t')
    except:
        try:
            # Tenta ler como CSV
            df = pd.read_csv(io.StringIO(data_raw))
        except Exception as e:
            st.error(f"Erro ao processar dados: {e}")
            return None
    
    # Limpeza de colunas
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace('\n', ' ')
    
    # Renomear colunas
    for col in df.columns:
        if "Série" in col or "Serie" in col:
            df.rename(columns={col: 'Serie'}, inplace=True)
        if "Descrição" in col or "Órgão" in col or "Orgao" in col or "Descrição / Órgão" in col:
            df.rename(columns={col: 'Orgao'}, inplace=True)
    
    # Criar rótulo Y
    df['Rotulo_Y'] = df['Orgao'].fillna('Não Identificado')
    
    return df

# Função para gerar gráficos
def gerar_graficos(df, filtro_serie, titulo_serie):
    """Gera gráficos para uma série específica"""
    
    # Meses desejados
    meses_desejados = [f"{i:02d}/2025" for i in range(1, 13)]
    
    # Garantir que todas as colunas de mês existem
    for mes in meses_desejados:
        if mes not in df.columns:
            df[mes] = '-'
    
    # Mapa de status
    status_map_text = {
        'C/ MOV': 'Com Movimento',
        'SEM MOVIMENTO': 'Sem Movimento',
        'SEM MOV': 'Sem Movimento',
        '-': 'Não Declarado',
        'NAN': 'Não Declarado',
        'EM ANDAMENTO': 'Ignorado',
        'SEM PROCURAÇÃO': 'Ignorado',
        'S/PROCURAÇÃO': 'Ignorado',
        'Ñ OBRIGATORIO': 'Ignorado',
        'NÃO OBRIGATÓRIO': 'Ignorado'
    }
    
    status_map_num = {
        'Não Declarado': 0,
        'Sem Movimento': 1,
        'Com Movimento': 2,
        'Ignorado': 3
    }
    
    # Cores acessíveis
    cores_lista = ['#D55E00', '#56B4E9', '#0072B2', '#FFFFFF']
    cmap_custom = ListedColormap(cores_lista)
    
    # Filtrar série
    df_serie = df[df['Serie'].str.contains(filtro_serie, na=False)].copy()
    
    if df_serie.empty:
        return None
    
    # Formato longo
    df_melted = df_serie.melt(
        id_vars=['Município', 'Rotulo_Y'],
        value_vars=meses_desejados,
        var_name='Mes',
        value_name='Status'
    )
    
    df_melted['Status'] = df_melted['Status'].astype(str).str.strip().str.upper()
    df_melted['Status_Texto'] = df_melted['Status'].map(status_map_text).fillna('Não Declarado')
    df_melted['Status_Code'] = df_melted['Status_Texto'].map(status_map_num).fillna(0)
    
    municipios = df_melted['Município'].unique()
    graficos = {}
    
    for municipio in municipios:
        try:
            df_city = df_melted[df_melted['Município'] == municipio].copy()
            
            # Pivot table
            heatmap_data = df_city.pivot_table(
                index='Rotulo_Y',
                columns='Mes',
                values='Status_Code',
                aggfunc='max'
            )
            
            heatmap_data = heatmap_data.reindex(columns=meses_desejados).fillna(0)
            
            # Criar figura
            altura = max(6, len(heatmap_data) * 0.8 + 3)
            fig, ax = plt.subplots(figsize=(15, altura))
            
            # Heatmap
            sns.heatmap(
                heatmap_data,
                cmap=cmap_custom,
                vmin=0, vmax=3,
                linewidths=1, linecolor='#e0e0e0',
                cbar=False,
                annot=False,
                ax=ax
            )
            
            # Título e labels
            ax.set_title(f'{titulo_serie} (2025)', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Competência', fontsize=12, fontweight='bold', labelpad=15)
            ax.set_ylabel('Órgão Declarante', fontsize=12, fontweight='bold')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            
            # Legenda
            patches = [
                mpatches.Patch(color=cores_lista[2], label='Com Movimento'),
                mpatches.Patch(color=cores_lista[1], label='Sem Movimento'),
                mpatches.Patch(color=cores_lista[0], label='Não Declarado'),
            ]
            ax.legend(handles=patches, bbox_to_anchor=(0.5, -0.25), loc='upper center', ncol=3, frameon=False)
            
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.35)
            
            graficos[municipio] = fig
            plt.close(fig)
            
        except Exception as e:
            st.warning(f"Erro ao gerar gráfico para {municipio}: {e}")
            continue
    
    return graficos

# Botão para gerar gráficos
if st.button("🚀 Gerar Gráficos", type="primary", use_container_width=True):
    if not data_input.strip():
        st.error("❌ Por favor, cole seus dados primeiro!")
    else:
        with st.spinner("⏳ Processando dados..."):
            # Processar dados
            df = processar_dados(data_input)
            
            if df is not None:
                st.success("✅ Dados processados com sucesso!")
                
                # Atualizar lista de municípios
                municipios_unicos = sorted(df['Município'].unique())
                
                # Gerar gráficos
                graficos_r2000 = None
                graficos_r4000 = None
                
                if gerar_r2000:
                    with st.spinner("⏳ Gerando gráficos R-2000..."):
                        graficos_r2000 = gerar_graficos(df, '2000', 'Monitoramento R-2000')
                
                if gerar_r4000:
                    with st.spinner("⏳ Gerando gráficos R-4000..."):
                        graficos_r4000 = gerar_graficos(df, '4000', 'Monitoramento R-4000')
                
                # Armazenar em session state
                st.session_state.graficos_r2000 = graficos_r2000
                st.session_state.graficos_r4000 = graficos_r4000
                st.session_state.df = df
                st.session_state.municipios = municipios_unicos
                
                st.success("✅ Gráficos gerados com sucesso!")

# Exibir gráficos gerados
if 'graficos_r2000' in st.session_state or 'graficos_r4000' in st.session_state:
    st.divider()
    st.header("📊 Gráficos Gerados")
    
    # Abas para cada série
    tab_r2000, tab_r4000 = st.tabs(["R-2000", "R-4000"])
    
    with tab_r2000:
        if 'graficos_r2000' in st.session_state and st.session_state.graficos_r2000:
            municipios_r2000 = list(st.session_state.graficos_r2000.keys())
            municipio_selecionado = st.selectbox("Selecione um município (R-2000):", municipios_r2000)
            
            if municipio_selecionado:
                fig = st.session_state.graficos_r2000[municipio_selecionado]
                st.pyplot(fig)
    
    with tab_r4000:
        if 'graficos_r4000' in st.session_state and st.session_state.graficos_r4000:
            municipios_r4000 = list(st.session_state.graficos_r4000.keys())
            municipio_selecionado = st.selectbox("Selecione um município (R-4000):", municipios_r4000)
            
            if municipio_selecionado:
                fig = st.session_state.graficos_r4000[municipio_selecionado]
                st.pyplot(fig)
    
    # Seção de downloads
    st.divider()
    st.header("📥 Downloads")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Baixar Word (DOCX)", use_container_width=True):
            with st.spinner("⏳ Gerando arquivo Word..."):
                try:
                    # Gerar arquivo Word
                    exportador = ExportadorWord("Relatório de Monitoramento GO")
                    
                    if 'graficos_r2000' in st.session_state and st.session_state.graficos_r2000:
                        for municipio, fig in st.session_state.graficos_r2000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-2000")
                    
                    if 'graficos_r4000' in st.session_state and st.session_state.graficos_r4000:
                        for municipio, fig in st.session_state.graficos_r4000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-4000")
                    
                    # Salvar em arquivo temporário
                    temp_word = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
                    exportador.salvar(temp_word.name)
                    
                    # Ler arquivo para download
                    with open(temp_word.name, 'rb') as f:
                        st.download_button(
                            label="Clique aqui para baixar",
                            data=f.read(),
                            file_name="Relatorio_Graficos.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    
                    st.success("✅ Arquivo Word gerado com sucesso!")
                    os.unlink(temp_word.name)
                except Exception as e:
                    st.error(f"❌ Erro ao gerar arquivo Word: {e}")
    
    with col2:
        if st.button("🖼️ Baixar PNGs", use_container_width=True):
            with st.spinner("⏳ Gerando arquivo ZIP com PNGs..."):
                try:
                    # Gerar arquivo ZIP com PNGs
                    exportador = ExportadorPNG()
                    
                    if 'graficos_r2000' in st.session_state and st.session_state.graficos_r2000:
                        for municipio, fig in st.session_state.graficos_r2000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-2000")
                    
                    if 'graficos_r4000' in st.session_state and st.session_state.graficos_r4000:
                        for municipio, fig in st.session_state.graficos_r4000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-4000")
                    
                    # Salvar em arquivo temporário
                    temp_zip = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
                    exportador.salvar(temp_zip.name)
                    
                    # Ler arquivo para download
                    with open(temp_zip.name, 'rb') as f:
                        st.download_button(
                            label="Clique aqui para baixar",
                            data=f.read(),
                            file_name="Graficos_PNG.zip",
                            mime="application/zip"
                        )
                    
                    st.success("✅ Arquivo ZIP gerado com sucesso!")
                    os.unlink(temp_zip.name)
                except Exception as e:
                    st.error(f"❌ Erro ao gerar arquivo ZIP: {e}")
    
    with col3:
        if st.button("📑 Baixar PDF", use_container_width=True):
            with st.spinner("⏳ Gerando arquivo PDF..."):
                try:
                    # Gerar arquivo PDF
                    exportador = ExportadorPDF("Relatório de Monitoramento GO")
                    
                    if 'graficos_r2000' in st.session_state and st.session_state.graficos_r2000:
                        for municipio, fig in st.session_state.graficos_r2000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-2000")
                    
                    if 'graficos_r4000' in st.session_state and st.session_state.graficos_r4000:
                        for municipio, fig in st.session_state.graficos_r4000.items():
                            exportador.adicionar_grafico(fig, municipio, "R-4000")
                    
                    # Salvar em arquivo temporário
                    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
                    exportador.salvar(temp_pdf.name)
                    
                    # Ler arquivo para download
                    with open(temp_pdf.name, 'rb') as f:
                        st.download_button(
                            label="Clique aqui para baixar",
                            data=f.read(),
                            file_name="Relatorio_Graficos.pdf",
                            mime="application/pdf"
                        )
                    
                    st.success("✅ Arquivo PDF gerado com sucesso!")
                    os.unlink(temp_pdf.name)
                except Exception as e:
                    st.error(f"❌ Erro ao gerar arquivo PDF: {e}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem; margin-top: 2rem;">
        <p>Gerador de Gráficos GO v1.0 | Desenvolvido com Streamlit</p>
    </div>
""", unsafe_allow_html=True)
