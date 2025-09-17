import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import fitz
import docx

st.markdown(
    """
    <div style="background-color:#4CAF50;padding:12px;border-radius:10px;">
        <h2 style="color:white;text-align:center;">Dhora's App - Word Cloud Generator</h2>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload a PDF, TXT, or DOCX file", type=["pdf", "txt", "docx"])

text = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

if not text:
    text = st.text_area("Or you can  enter your text here:", 
        "Streamlit makes it easy to create apps for data science and machine learning."
    )

max_words = st.slider("Max Words", 10, 200, 100)
background_color = st.color_picker("Pick a background color", "#ffffff")

if st.button("Generate Word Cloud"):
    if text.strip() == "":
        st.warning("Please provide text (upload a file or type manually).")
    else:
        wc = WordCloud(width=800, height=400,
                       max_words=max_words,
                       background_color=background_color).generate(text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
