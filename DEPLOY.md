# 🚀 Guia de Deploy no Streamlit Cloud

Este guia mostra como fazer deploy do aplicativo Gerador de Gráficos GO no Streamlit Cloud.

## Pré-requisitos

- Conta no GitHub (já criada)
- Conta no Streamlit Cloud (gratuita em [share.streamlit.io](https://share.streamlit.io))
- Repositório GitHub com o código (já criado em `samuelalper8/graficos-go-app`)

## Passo 1: Preparar o Repositório

O repositório já foi criado e enviado para GitHub. Você pode verificar em:
```
https://github.com/samuelalper8/graficos-go-app
```

## Passo 2: Deploy no Streamlit Cloud

### Opção A: Deploy Automático (Recomendado)

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"New app"**
3. Selecione sua conta GitHub (samuelalper8)
4. Escolha o repositório: **graficos-go-app**
5. Configure:
   - **Branch**: master (ou main)
   - **Main file path**: app.py
6. Clique em **"Deploy"**

O Streamlit Cloud irá:
- Clonar o repositório
- Instalar dependências do `requirements.txt`
- Executar `streamlit run app.py`
- Gerar uma URL pública

### Opção B: Deploy Manual

Se preferir fazer deploy manualmente:

```bash
# 1. Clone o repositório
git clone https://github.com/samuelalper8/graficos-go-app.git
cd graficos-go-app

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
streamlit run app.py
```

## Passo 3: Acessar o Aplicativo

Após o deploy, você terá uma URL como:
```
https://seu-usuario-graficos-go.streamlit.app
```

Compartilhe esta URL com seus colegas!

## Configurações Recomendadas

### Secrets (Opcional)

Se precisar adicionar variáveis secretas (como chaves de API), crie um arquivo `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
api_key = "sua-chave-aqui"
```

**Importante**: Não faça commit de `secrets.toml` no GitHub!

### Limites do Streamlit Cloud (Plano Gratuito)

- ✅ Aplicativos públicos ilimitados
- ✅ Até 3 GB de armazenamento
- ✅ Até 1 GB de memória por aplicativo
- ⚠️ Aplicativos inativos por 7 dias são pausados
- ⚠️ Limite de CPU compartilhada

Para aplicativos com uso intensivo, considere um plano pago.

## Troubleshooting

### Erro: "ModuleNotFoundError"

**Solução**: Verifique se todas as dependências estão em `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### Aplicativo carregando lentamente

**Solução**: 
- Reduza o tamanho dos gráficos
- Implemente cache com `@st.cache_data`
- Considere um plano pago do Streamlit Cloud

### Erro ao processar dados

**Solução**:
- Verifique o formato dos dados (Tab-separated ou CSV)
- Veja os logs no Streamlit Cloud (aba "Logs")

## Atualizações

Para atualizar o aplicativo:

```bash
# 1. Faça as alterações localmente
# 2. Commit e push para GitHub
git add .
git commit -m "Descrição das alterações"
git push origin master

# 3. O Streamlit Cloud irá fazer deploy automaticamente!
```

## Monitoramento

No painel do Streamlit Cloud, você pode:
- Ver logs em tempo real
- Verificar uso de recursos
- Reiniciar a aplicação
- Deletar a aplicação

## Suporte

Para problemas com Streamlit Cloud:
- Documentação: [docs.streamlit.io](https://docs.streamlit.io)
- Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Issues: [github.com/streamlit/streamlit/issues](https://github.com/streamlit/streamlit/issues)

---

**Seu aplicativo está pronto para o mundo!** 🎉
