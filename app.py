# Instalação das bibliotecas
# pip install streamlit pandas plotly gdown

import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Função para baixar o arquivo do Google Drive
def download_excel_from_drive(file_id, output):
    """
    Baixa o arquivo Excel do Google Drive.
    :param file_id: ID do arquivo no Google Drive.
    :param output: Caminho de saída para salvar o arquivo.
    """
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

# ID do arquivo no Google Drive
file_id = "1TuIjVvkydNFPjAieusMEZMQeJBQOUkZW"  # Substitua pelo seu ID do Google Drive
output_file = "dados.xlsx"

# Baixar o arquivo Excel do Google Drive
download_excel_from_drive(file_id, output_file)

# Ler os dados do Excel
df = pd.read_excel(output_file)

# Ajustar o formato das colunas de meses para "MMM/YY"
# Para garantir que as colunas que representam meses sejam formatadas corretamente
for col in df.columns[1:]:  # Ignora a primeira coluna que é 'Tipos de comida'
    try:
        # Verifica se a coluna é uma data e formata
        df.rename(columns={col: pd.to_datetime(col).strftime("%b/%y")}, inplace=True)
    except Exception:
        pass  # Se a coluna não for uma data, ignora

# Configurar o título do app
st.title("Análise de Coleta de Resíduos")

# Criar filtros na barra lateral
st.sidebar.header("Filtros")
meses = st.sidebar.multiselect("Selecione o(s) mês(es):", options=df.columns[1:], default=df.columns[1:])
residuos = st.sidebar.multiselect("Selecione o(s) tipo(s) de resíduo:", options=df["Tipo de resíduo - Toneladas"], default=df["Tipo de resíduo - Toneladas"])

# Filtrar os dados
dados_filtrados = df[df["Tipo de resíduo - Toneladas"].isin(residuos)]
dados_filtrados = dados_filtrados[["Tipo de resíduo - Toneladas"] + meses]

# Mostrar tabela filtrada

st.dataframe(dados_filtrados)

# Transformar os dados para formato longo (para facilitar a criação de gráficos)
dados_longos = dados_filtrados.melt(id_vars=["Tipo de resíduo - Toneladas"], var_name="Mês", value_name="Toneladas")

# Criar o gráfico
if not dados_longos.empty:
    st.subheader("Gráfico Interativo")
    fig = px.bar(dados_longos, x="Tipo de resíduo - Toneladas", y="Toneladas", color="Mês", barmode="group", title="Consumo por Resíduo, Tonelada e Mês")
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
