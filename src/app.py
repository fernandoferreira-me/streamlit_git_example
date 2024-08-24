import streamlit as st
import pandas as pd

from sklearn.datasets import load_iris


def main():
    """ Main function of the App
    """
    st.title("My Streamlit App")
    st.write("This is a simple Streamlit app that loads the Iris dataset.")

    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["target"] = iris.target

    st.write(df)
    
    
if __name__ == "__main__":
    main()