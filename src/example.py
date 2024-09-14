import streamlit as st
import pandas as pd
import time
from numerize.numerize import numerize
import matplotlib.pyplot as plt
import seaborn as sns
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.monospace"] = ["FreeMono"]

if 'plot_y_label' not in st.session_state:
    st.session_state["plot_y_label"] = "totalCases"

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv.gz"
    data = pd.read_csv(url, compression='gzip')
    return data

# Configurar containers, expanders, sidebars, tabs, grid e colunas
# Utilizar diferentes temas na aplicação Streamlit
# Criar uma aplicação com múltiplas páginas e menu de navegação

st.set_page_config(page_title="Análise de dados de COVID-19 no Brasil",
                   page_icon="🦠",
                   layout="wide")


st.title("Análise de dados de COVID-19 no Brasil")
start = time.time()
data = load_data()
end = time.time()
st.write(f"Time to load title: {end - start:.02f} s")

st.sidebar.header("Configurações")
state = st.sidebar.selectbox("Selecione o estado",
                             sorted(data.state.unique()))

y_label_options = ["totalCases", "deaths"]
st.session_state["plot_y_label"] = st.sidebar.selectbox("Selecione o dado para o eixo Y",
                                                        y_label_options)

page = st.sidebar.radio("Navegação", ["Análise Dados", "Sobre"])

def analyze(data):
    with st.container():
        st.subheader("Visão Geral dos Dados")
        st.write(f"Dados do estado escolhido: {state}")
        st.dataframe(data.head())
        

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Casos Totais")
        
        total_cases = data.groupby("date").totalCases.sum().sort_index().iloc[-1]
        st.metric(label="Total de casos", value=numerize(int(total_cases)))
        
    with col2:
        st.subheader("Óbitos Totais")
        total_deaths = data.groupby("date").deaths.sum().sort_index().iloc[-1]
        st.metric(label="Total de óbitos", value=f"{total_deaths:n}")

    sns.set(style="ticks", context="talk")
    plt.style.use("dark_background")    
    fig, ax = plt.subplots()
    attr_by_date = data.groupby("date")[st.session_state["plot_y_label"]].sum().reset_index()
    attr_by_date['date'] = pd.to_datetime(attr_by_date['date'])
    sns.set_style("dark")
    if state == "TOTAL":
        ax.set_title("Total de casos de COVID-19 no Brasil")
    else:
        ax.set_title(f"Total de casos de COVID-19 no estado {state}")
    sns.lineplot(x="date", y=st.session_state["plot_y_label"],
                data=attr_by_date, ax=ax, color='limegreen')
    plt.xticks(rotation=45)
    ax.yaxis.grid(True, ls="--")
    plt.tight_layout()
    st.pyplot(fig)

    with st.expander("Ver dados brutos"):
        st.dataframe(data_state)
        
        

data_state = data.query(f"state == '{state}'")


if page == "Análise Dados":
    tab1, tab2 = st.tabs(["Análise por estado", "Análise por município"])

    with tab1:
        analyze(data_state)
        
    with tab2:
        city = st.selectbox("Selecione o município", sorted(data_state.city.unique()))
        data_city = data_state.query(f"city == '{city}'")
        analyze(data_city)
        
elif page == "Sobre":
    st.write("Por favor, selecione a aba 'Análise Dados' para visualizar os dados de COVID-19 no Brasil.")
    st.write("Este é um exemplo de aplicação Streamlit para análise de dados de COVID-19 no Brasil.")
    st.write("Por hoje é só, pessoal! Até a próxima!")
    st.image("https://img.elo7.com.br/product/zoom/3EF316C/placa-decorativa-that-s-all-folks-infantil.jpg")