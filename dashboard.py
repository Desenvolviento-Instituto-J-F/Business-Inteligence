
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def connection():
    load_dotenv()
    db_host_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT")
    return create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host_name}:{db_port}/{db_name}?sslmode=require')



def status(media):
    if media >=7:
        return 'Acima'
    elif media >=5:
        return 'Na média'
    else:
        return 'Abaixo'


dados = {
    "disciplina": [
        "Matemática", "Português", "Geografia",
        "História", "Biologia", "Física", "Inglês"
    ],
    "media": [10, 3, 10, 6.6, 6.5, 7.0, 10]
}

df = pd.DataFrame(dados)
df['status'] = df["media"].apply(status)

col1, col2, col3 = st.columns(3)

disciplinas = len(df)
media_geral = round(df["media"].mean(),2)
aprovados = (df["media"] >= 6).sum()

with col1:
    st.metric("Disciplinas", disciplinas)

with col2:
    st.metric("Média geral", media_geral)

with col3:
    st.metric("Acima da média", aprovados)


st.subheader("Nota média por disciplina")

fig = px.bar(
    df,
    x="disciplina",
    y="media",
    color="status",
    color_discrete_map={
        "Acima":"#34AD38"
        ,"Na média": "#E3E041"
,"Abaixo":"#FF4D4F"
    }
)


st.plotly_chart(fig, use_container_width=True)

