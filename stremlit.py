import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import PyPDF2
import docx
import numpy as np
from PIL import Image

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = " ".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    return text

def generate_wordcloud(text, mask_image, output_file="shape_wordcloud.png"):
    mask = np.array(Image.open(mask_image))
    stopwords = set(STOPWORDS)
    wc = WordCloud(
        width=900,
        height=500,
        background_color="white",
        stopwords=stopwords,
        colormap="viridis",
        mask=mask,
        contour_color="black",
        contour_width=2,
        max_words=250,
        max_font_size=150
    ).generate(text)
    wc.to_file(output_file)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

txt_text = extract_text_from_txt("sample.txt")
pdf_text = extract_text_from_pdf("sample.pdf")
docx_text = extract_text_from_docx("sample.docx")
all_text = txt_text + " " + pdf_text + " " + docx_text

# Example: "circle.png" should be a black circle on white background
generate_wordcloud(all_text, "circle.png", "circle_wordcloud.png")