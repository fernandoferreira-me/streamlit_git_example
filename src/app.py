import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time 

from sklearn.datasets import load_iris



def scope():
    """
    1. Utilizar elementos de formulários: Botões, Seletores (radio, checkbox,
    dropdowns, selects) 
    2. Desenvolver um serviço de download de arquivos com Streamlit
    3. Utilizar os elementos barra de progresso e spinners em aplicações de
    Streamlit 
    4. Utilizar elementos de formulários: text box, textarea, campos para senhas,
    campos para números, data, hora e color picker
    """
    pass

def main():
    """ Main function of the App
    """
    background_color = st.selectbox("Escolha uma cor de fundo", ["white", "gray", "purple", "magenta"])
    
    colormap = {
        "magenta": "#FF00FF",
        "purple": "#800080",
        "gray": "#808080",
        "white": "#FFFFFF",
    }
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colormap[background_color]};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    
    st.title("My Streamlit App")
    st.write("This is a simple Streamlit app that loads the Iris dataset.")

    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    target = pd.Series(iris.target)
    
    if st.button("Mostrar resumo dos dados do DataFrame"):
        st.write(df.describe())
        
    select_target = st.radio("Escolha uma classe alvo", target.unique())
    if st.checkbox("Mostrar Dados?"):
        st.write(df[target == select_target].describe())
        with sns.axes_style("whitegrid"):
            sns.set_context("paper")
            fig, axes = plt.subplots(1, df.shape[1], sharey=True)
            for idx, ax in enumerate(axes.flatten()):
                column = df.columns[idx]
                xmin = df[column].min()
                xmax = df[column].max()
                df.loc[target == select_target, column].plot(kind="kde", ax=ax)
                ax.set_title(column)
                ax.set_xlim([xmin, xmax])
                ax.set_ylim([0, 5.5])
            fig.tight_layout()
            st.write(fig)
        
    select_box = st.selectbox("Selecione uma coluna para exibir", df.columns)
    with sns.axes_style("whitegrid"):
        fig, ax = plt.subplots()
        df[select_box].plot(kind="kde", ax=ax)
        st.write(fig)
        
    selected_boxes = st.multiselect("Selecione colunas para exibir", df.columns)
    st.write(df[selected_boxes])

    text_input = st.text_input("Filtro: (valores menores que ...)")
    if text_input:
        with st.spinner("Filtrando dados..."):
            time.sleep(5)
            filtered_data = df[df.iloc[:, 0] < float(text_input)]
            st.metric("Quantidade de registros",
                      filtered_data.shape[0])
            csv = filtered_data.to_csv(index=False)
            st.download_button(label="Baixar Dados",
                               data=csv,
                               file_name="filtered_data.csv",
                               mime="text/csv")
    
        

if __name__ == "__main__":
    main()