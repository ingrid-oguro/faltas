import streamlit as st
import altair as alt
import pandas as pd 
#import pip
#pip.main(["install", "openpyxl"])
falta = pd.read_excel('faltas_20222.xlsx')
rank = pd.read_excel('Ranking de faltas.xlsx')
faltas_20222 = falta.fillna(method="ffill")

#Para definir as configurações da aba e da página:
PAGE_CONFIG = {"page_title": "ESEG - Apoio ao aluno", "page_icon": ":globe_with_meridians:", "layout": "wide"}

#Para configurar a aba e a posição da página no navegador:
st.set_page_config(**PAGE_CONFIG)

st.header('TOTAL DE FALTAS NA SEMANA/ANO - 20222')
st.write('Atualizado em 17/10/2022')

col1, col2,col3 = st.columns((1,1,3))
with col1:
    opcoes_nome = sorted(faltas_20222.NOME.unique())  # sorted = em ordem alfabetica
    nome_selecionado = st.selectbox('Nome', opcoes_nome)
    base = faltas_20222.query('NOME	 == @nome_selecionado  ')
with col2:
    opcoes_disci = sorted(base.DISCIPLINA.unique())  # sorted = em ordem alfabetica
    disci_selecionado = st.selectbox('Disciplina', opcoes_disci)
    abc = base.query('DISCIPLINA == @disci_selecionado ')

#st.table(abc)

a= alt.Chart(abc).mark_bar(size=50).encode(
    x='SEMANA/ANO',
    y='TOTAL_FALTA'
).properties(width=1000, height=340)

st.altair_chart(a, use_container_width=True)

st.header('RANKING DE FALTAS - 20222')
st.write('Atualizado em 17/10/2022')

col01, col02,col03 = st.columns((1,1,3))

with col01:
    opcoes_curso = sorted(rank.CURSO.unique())  # sorted = em ordem alfabetica
    curso_selecionado = st.selectbox('Graduação', opcoes_curso)
    base_rank = rank.query('CURSO	 == @curso_selecionado  ')




bars = alt.Chart(base_rank).mark_bar().encode(
   alt.Y('NOME:N', sort='-x'),
   alt.X('DATA'),tooltip=[alt.Tooltip('DATA', title='FALTA')])



st.altair_chart(bars , use_container_width=True )


