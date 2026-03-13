# 📊 Gerador de Gráficos GO

Aplicativo Streamlit para gerar gráficos de monitoramento R-2000 e R-4000 a partir de dados tabulares, com exportação em Word, PNG e PDF.

## 🚀 Funcionalidades

- ✅ **Interface intuitiva** para colar dados
- ✅ **Geração automática** de heatmaps para R-2000 e R-4000
- ✅ **Exportação em múltiplos formatos**:
  - 📄 Word (DOCX) com gráficos incorporados
  - 🖼️ PNG em arquivo ZIP
  - 📑 PDF com todos os gráficos
- ✅ **Paleta de cores acessível** para daltônicos
- ✅ **Processamento automático** de dados

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- python-docx
- reportlab

## 🔧 Instalação Local

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/graficos-go-app.git
cd graficos-go-app
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o aplicativo
```bash
streamlit run app.py
```

O aplicativo será aberto em `http://localhost:8501`

## 🌐 Deploy no Streamlit Cloud

### 1. Prepare seu repositório GitHub

```bash
# Inicialize git (se ainda não fez)
git init

# Adicione os arquivos
git add .
git commit -m "Initial commit: Gerador de Gráficos GO"

# Crie um repositório no GitHub e faça push
git remote add origin https://github.com/seu-usuario/graficos-go-app.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em "New app"
3. Selecione seu repositório GitHub
4. Configure:
   - **Repository**: seu-usuario/graficos-go-app
   - **Branch**: main
   - **Main file path**: app.py
5. Clique em "Deploy"

Seu aplicativo estará disponível em: `https://seu-usuario-graficos-go.streamlit.app`

## 📖 Como Usar

### Passo 1: Prepare seus dados

Seus dados devem estar em formato tabular com as seguintes colunas:
- `Município` - Nome do município
- `Inscrição` - CNPJ ou código de inscrição
- `Descrição / Órgão` - Nome do órgão declarante
- `Série` - R-2000 ou R-4000
- `01/2025` a `12/2025` - Status para cada mês

### Passo 2: Cole os dados

1. Abra o aplicativo
2. Cole seus dados na área de texto (formato Tab-separated ou CSV)
3. Clique em "Gerar Gráficos"

### Passo 3: Baixe os gráficos

Após a geração, você pode baixar:
- **Word (DOCX)**: Relatório completo com todos os gráficos
- **PNG**: Arquivo ZIP com imagens individuais
- **PDF**: Documento PDF com todos os gráficos

## 📊 Formatos de Status Aceitos

| Status | Significado |
|--------|------------|
| `C/ MOV` | Com Movimento |
| `SEM MOVIMENTO` | Sem Movimento |
| `-` | Não Declarado |
| `EM ANDAMENTO` | Em Andamento (ignorado) |
| `SEM PROCURAÇÃO` | Sem Procuração (ignorado) |

## 🎨 Paleta de Cores

A aplicação usa uma paleta de cores acessível para daltônicos:

- 🔵 **Azul Escuro** (#0072B2) - Com Movimento
- 🔵 **Azul Claro** (#56B4E9) - Sem Movimento
- 🟠 **Laranja** (#D55E00) - Não Declarado
- ⚪ **Branco** (#FFFFFF) - Ignorado

## 📁 Estrutura do Projeto

```
graficos-go-app/
├── app.py                 # Aplicativo principal Streamlit
├── exporters.py          # Módulo de exportação (Word, PDF, PNG)
├── requirements.txt      # Dependências Python
├── .streamlit/
│   └── config.toml      # Configuração do Streamlit
├── README.md            # Este arquivo
└── .gitignore           # Arquivos a ignorar no Git
```

## 🐛 Troubleshooting

### Erro ao processar dados
- Verifique se os dados estão em formato tabular correto
- Certifique-se de que as colunas de mês estão no formato `MM/YYYY`
- Tente usar Tab-separated ou CSV

### Gráficos não aparecem
- Verifique se há dados para a série selecionada (R-2000 ou R-4000)
- Certifique-se de que a coluna "Série" contém "2000" ou "4000"

### Erro ao exportar
- Verifique se há espaço em disco
- Tente gerar novamente
- Verifique os logs do Streamlit

## 📝 Exemplo de Dados

```
Município	Inscrição	Descrição	Série	01/2025	02/2025	03/2025
Amaralina	14756596000169	FMAS	R-2000	SEM MOVIMENTO	SEM MOVIMENTO	SEM MOVIMENTO
Amaralina	14756596000169	FMAS	R-4000	C/ MOV	C/ MOV	C/ MOV
Baliza	14769746000179	FMAS	R-2000	SEM MOVIMENTO	SEM MOVIMENTO	SEM MOVIMENTO
Baliza	14769746000179	FMAS	R-4000	-	C/ MOV	C/ MOV
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório GitHub.

---

**Desenvolvido com ❤️ usando Streamlit**
