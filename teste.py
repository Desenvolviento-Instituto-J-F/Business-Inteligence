import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_resource
@st.cache_resource
def conectar():
    engine = create_engine(
        f"postgresql+psycopg2://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}"
        f"@{st.secrets['DB_HOST_NAME']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}",
        pool_pre_ping=True
    )
    return engine

st.set_page_config(
    page_title="",
    layout="wide"
)
conn = conectar()


id_turma = st.number_input("ID da turma", min_value=1, value=1)

query = """
SELECT n.valor
FROM nota n
JOIN aluno a ON a.id_aluno = n.id_aluno
WHERE a.id_turma = %s;
"""

df = pd.read_sql(query, conn, params=(id_turma,))

if df.empty:
    st.warning("Sem dados para essa turma.")
    st.stop()

df["nota_int"] = df["valor"].round().astype(int)

# conta alunos por nota
contagem = df["nota_int"].value_counts().sort_index()

# garante índices 1–10
todos_indices = pd.Series(0, index=range(1, 11))
contagem = todos_indices.add(contagem, fill_value=0)

grafico_df = contagem.reset_index()
grafico_df.columns = ["nota", "quantidade"]

def classificar(nota):
    if 9 <= nota <= 10:
        return "Acima da média da turma"
    elif 6 <= nota <= 8:
        return "Na média da turma"
    else:
        return "Abaixo da média da turma"

grafico_df["classificacao"] = grafico_df["nota"].apply(classificar)

cores = {
    "Abaixo da média da turma": "#D16F6F",
    "Na média da turma": "#A6B1D9",
    "Acima da média da turma": "#8FCF92"
}

fig = px.bar(
    grafico_df,
    x="nota",
    y="quantidade",
    color="classificacao",
    color_discrete_map=cores,
    category_orders={"nota": list(range(1, 11))}
)

fig.update_layout(
    xaxis_title="Nota",
    yaxis_title="Quantidade de alunos",
    legend_title=""
)

st.plotly_chart(fig, use_container_width=True)
#p fazer deploy do dash
#pip install kaleido
import plotly.io as pio

grafico_html = pio.to_html(
    fig,
    full_html=False,        
    include_plotlyjs='cdn'  
)