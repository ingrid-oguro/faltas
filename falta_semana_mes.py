import streamlit as st
import pandas as pd
import altair as alt
import datetime
import pip
pip.main(["install", "openpyxl"])

df_falta = pd.read_excel('Acompanhamento de faltas (extr. 28.10.2022).xlsx')
freq_aprov = pd.read_excel('Notas e Faltas - 28.10.22.xlsx')


#Para definir as configurações da aba e da página:
PAGE_CONFIG = {"page_title": "ESEG - Apoio ao aluno", "page_icon": ":globe_with_meridians:", "layout": "wide"}
st.set_page_config(**PAGE_CONFIG)

st.header('TOTAL DE FALTAS NA SEMANA/ANO - 20222')


#filtrando Cursando
sit_matr = sorted(df_falta.SIT_MAT.unique())
sit_mat = 'Cursando'

df_falta = df_falta.query('SIT_MAT == @sit_mat ')

df_falta = df_falta.drop(labels=['CODPERLET','FILIAL','TURNO','CODTURMA','CODDISC','SIT_MAT'], axis=1)

def week_number_of_month(date_value):
     return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

df_falta["SEMANA_DO_MES"] = df_falta["DATA"].apply(week_number_of_month)

df_falta['MES'] = pd.DatetimeIndex(df_falta['DATA']).month

MesDict2 = {8:"8.2022",
            9:"9.2022",
            10:"10.2022"}

df_falta["MES3"] = df_falta["MES"].apply(lambda x: MesDict2 [x])

base_semana = df_falta.groupby(['NOME','RA','CURSO','DISCIPLINA','MES','MES3','SEMANA_DO_MES'])['AULA'].count().reset_index()
base_semana.rename(columns = {'AULA':'FALTAS'}, inplace = True)

base_semana['TOTAL_FALTA'] = base_semana.groupby(['DISCIPLINA','MES'])['FALTAS'].cumsum()

col1, col2,col3 = st.columns((1,1,1))
with col1:
    st.write('Atualizado em 28/10/2022')

with col2:
    opcoes_nome = sorted(base_semana.NOME.unique())  # sorted = em ordem alfabetica
    nome_selecionado = st.selectbox('Nome', opcoes_nome)
    nome = base_semana.query('NOME	 == @nome_selecionado  ')
with col3:
    opcoes_disci = sorted(nome.DISCIPLINA.unique())  # sorted = em ordem alfabetica
    disci_selecionado = st.selectbox('Disciplina', opcoes_disci)
    base_aluno = nome.query('DISCIPLINA == @disci_selecionado ')

base_aluno.sort_values(by=['MES'])
st.markdown('#### CUMULATIVO DE FALTAS POR SEMANA',unsafe_allow_html=True)
st.markdown('##### O gráfico a seguir mostra o total de faltas acumulado por semana em uma disciplina. Considerando que cada falta se refere ao horário de uma aula.',unsafe_allow_html=True)
st.markdown('##### Ex: Uma disciplina pode ter 4 horários em 1 dia.',unsafe_allow_html=True)
st.markdown('##### A linha vermelha marca o limite de aprovação',unsafe_allow_html=True)
bar = alt.Chart(base_aluno).mark_bar(size=15).encode(
        y=alt.Y('TOTAL_FALTA', title = None, axis=alt.Axis(tickMinStep=1)),
        x=alt.X('SEMANA_DO_MES', title = None, axis=alt.Axis(tickMinStep=1)),
        )

        
base3 = freq_aprov.query('NOME	 == @nome_selecionado  ')
base_alunof = base3.query('DISCIPLINA == @disci_selecionado ')

rule = alt.Chart(base_alunof).mark_rule(color='red').encode(
    y='FREQ_APROV:Q'
)
#st.altair_chart(rule , use_container_width=True )
combined = bar + rule
#st.altair_chart(combined.facet("MES3:N", data=base_aluno ), use_container_width=True)

st.altair_chart(combined.facet(column=alt.Column('MES3', title = None, sort=alt.SortField(field='count', order='descending')), data=base_aluno), use_container_width=True)



with st.expander("Ver mais."):
    st.write("""
        Base.
    """)
    st.table(base_aluno)

base_mes = df_falta.groupby(['NOME','RA','CURSO','DISCIPLINA','MES','MES3'])['AULA'].count().reset_index()
base_mes.rename(columns = {'AULA':'FALTAS'}, inplace = True)

base_mes['MES_FALTA'] = base_mes.groupby(['DISCIPLINA'])['FALTAS'].cumsum()

base2 = base_mes.query('NOME	 == @nome_selecionado  ')
base_aluno2 = base2.query('DISCIPLINA == @disci_selecionado ')
st.markdown('#### CUMULATIVO DE FALTAS POR MES',unsafe_allow_html=True)
st.markdown('##### O gráfico a seguir mostra o total de faltas acumulado por mês em uma disciplina. ',unsafe_allow_html=True)

freq = str(base_alunof.FREQ.unique())

#with col1:
    #st.metric(label="Frequencia", value= freq, delta="1.2 °F")
    #st.write(str(freq))
   
g2 = alt.Chart(base_aluno2).mark_bar(size=30).encode(
        y=alt.Y('MES_FALTA',title='FALTAS', axis=alt.Axis(tickMinStep=1)),
        x=alt.X('MES3', title = None, axis=alt.Axis(tickMinStep=1),sort=alt.SortField(field='count', order='ascending'))
        ).interactive()
combined2 = g2 + rule
#,sort=alt.SortField(field='count', order='ascending')
st.altair_chart(combined2,  use_container_width=True )

with st.expander("Ver mais."):
    st.write("""
        Base.
    """)
    st.table(base_aluno2)
