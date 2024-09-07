
import streamlit as st 
import docx2txt
import pdfplumber

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os.path
import pandas as pd


def upload_docx():
    """
    Uploads a .docx file and returns the text content of the file
    """
    st.title("Upload your .docx file")
    text_file = st.file_uploader("Upload a .docx file", type=["docx", "txt"])
    details = st.button("Show details")
    if details and text_file:
        doc_details = {
            "File Name": text_file.name,
            "File Type": text_file.type,
            "File Size": text_file.size
        }
        if text_file.type == "text/plain":
            doc_details["Content"] = str(text_file.read())
            st.write(doc_details['Content'])
        else:
            docx_text = docx2txt.process(text_file)
            doc_details["Content"] = docx_text





def upload_pdf():
    """
    Upload pdf file and return the text content of the file
    """
    with open("stopwords.txt") as stopwords:
        stopwords = stopwords.read().split("\n")
        stopwords += ['projeto', "bloco", "disciplina", "competência",
                      "enunciado", "competências", "etapa", "aplicação",
                      "utilizando", "desenvolvimento", "aluno", "objetivo"] 
    st.write("Upload your .pdf file")
    pdf_file = st.file_uploader("Upload a .pdf file", type=["pdf"])
    details = st.button("Show details")
    if details and pdf_file:
        pdf_details = {
            "File Name": pdf_file.name,
            "File Type": pdf_file.type,
            "File Size": pdf_file.size
        }
        with pdfplumber.open(pdf_file) as pdf:
            d = os.path.dirname(__file__) 
            mask = np.array(Image.open(os.path.join(d, "silhueta-da-arvore.png")))

            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
            pdf_details["Content"] = pdf_text
            wordcloud = WordCloud(stopwords=stopwords,
                                  background_color="white",
                                  mask=mask,
                                  contour_width=3,
                                  contour_color='steelblue').generate(
                                      pdf_details["Content"].lower())
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.figure()
            plt.axis("off")

            st.write(fig)
        st.write(pdf_details)
    
def upload_csv():
    """
    Upload csv file and return the content of the file
    """
    st.write("Upload your .csv file")
    csv_file = st.file_uploader("Upload a .csv file", type=["csv"])
    details = st.button("Show details")
    if details and csv_file:
        csv_details = {
            "File Name": csv_file.name,
            "File Type": csv_file.type,
            "File Size": csv_file.size
        }
        csv_details["Content"] = pd.read_csv(csv_file)
        st.write(csv_details)
        st.dataframe(csv_details["Content"])
        
    
if __name__ == "__main__":
    #upload_docx()
    #upload_pdf()
    upload_csv()