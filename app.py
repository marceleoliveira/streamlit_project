import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

def download_excel_from_drive(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

file_id = "1TuIjVvkydNFPjAieusMEZMQeJBQOUkZW" 
output_file = "dados.xlsx"

download_excel_from_drive(file_id, output_file)

df = pd.read_excel(output_file)

for col in df.columns[1:]:  
    try:
        df.rename(columns={col: pd.to_datetime(col).strftime("%b/%y")}, inplace=True)
    except Exception:
        pass  

st.title("Análise de Coleta de Resíduos")

st.sidebar.header("Filtros")
meses = st.sidebar.multiselect("Selecione o(s) mês(es):", options=df.columns[1:], default=df.columns[1:])
residuos = st.sidebar.multiselect("Selecione o(s) tipo(s) de resíduo:", options=df["Tipo de resíduo - Toneladas"], default=df["Tipo de resíduo - Toneladas"])

dados_filtrados = df[df["Tipo de resíduo - Toneladas"].isin(residuos)]
dados_filtrados = dados_filtrados[["Tipo de resíduo - Toneladas"] + meses]

st.dataframe(dados_filtrados)

dados_longos = dados_filtrados.melt(id_vars=["Tipo de resíduo - Toneladas"], var_name="Mês", value_name="Toneladas")

if not dados_longos.empty:
    st.subheader("Gráfico Interativo")
    fig = px.bar(dados_longos, x="Tipo de resíduo - Toneladas", y="Toneladas", color="Mês", barmode="group", title="Consumo por Resíduo, Tonelada e Mês")
    st.plotly_chart(fig)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")
