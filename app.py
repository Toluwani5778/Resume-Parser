import streamlit as st
import base64
import tempfile
from docx2pdf import convert
import functions as fn
import pythoncom
import PyPDF2 as pdf
import os

# Initialize COM
pythoncom.CoInitialize()

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<div style="display: flex; justify-content: center;"><iframe src="data:application/pdf; base64,{base64_pdf}" width="1000" height="1000" type="application/pdf"></iframe></div>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    # Set up the layout with three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # Load and display the GIF image in the left column (col1)
    gif_path = 'Graphics/Resume Parser.gif'
    with col1:
        st.image(gif_path, use_column_width=True)  # Adjust the width as needed

    # Display the text in the middle column (col2)
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 60px;'>Resume Parser</h1>", unsafe_allow_html=True)

    logo_path = 'Graphics/AI Logo.png'
    # Display the logo in the right column (col3)
    with col3:
        st.image(logo_path, use_column_width=True)  # Adjust the width as needed

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf", "docx"])
    text = "Hello"
    if pdf_file is not None:
        if pdf_file.type == 'application/pdf':
            st.write("You've uploaded a PDF file.")
            # Create a temporary PDF file path
            pdf_path = tempfile.mktemp(suffix='.pdf')
            # Save the uploaded PDF file to the temporary path
            with open(pdf_path, 'wb') as f:
                f.write(pdf_file.getbuffer())
            show_pdf(pdf_path)
            text = fn.read_text_from_pdf(pdf_path)

        elif pdf_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            st.write("You've uploaded a DOCX file.")
            doc_path = tempfile.mktemp(suffix='.docx')
            # Save the uploaded PDF file to the temporary path
            with open(doc_path, 'wb') as f:
                f.write(pdf_file.getbuffer())
            pdf_path = tempfile.mktemp(suffix='.pdf')
            convert(doc_path, pdf_path)
            show_pdf(pdf_path)
            text = fn.read_text_from_pdf(pdf_path)

            # Uninitialize COM
            pythoncom.CoUninitialize()
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>Resume Analysis</h1>", unsafe_allow_html=True)
    st.subheader("Contact Information\n")
    st.write(f"**First Name:** {fn.extract_name(fn.nlp(text)).split()[0]}\n")
    st.write(f"**Last Name:** {fn.extract_name(fn.nlp(text)).split()[1]}\n")
    st.write(f"**Email:** {fn.extract_email(text)}\n")
    st.write(f"**Phone No:** {fn.remove_square_brackets(fn.extract_phone_numbers(text))}\n")
    st.subheader("Education\n")
    ed = fn.extract_education_from_resume(text)
    if ed:
        st.write(fn.extract_education_from_resume(text)[0])
    else:
        st.write("Education not detected")
    st.subheader("Objective/Summary\n")
    sections = fn.extract_entity_sections(text)
    if "summary" in sections:
        st.write(fn.remove_square_brackets(sections["summary"]))
    else:
        st.write("Summary not detected")
    st.subheader("Experience\n")
    if "experience" in sections:
        st.write(fn.remove_square_brackets(sections["experience"]))
    else:
        st.write("Experience not detected")
    st.subheader("Projects\n")
    if "projects" in sections:
        st.write(fn.remove_square_brackets(sections["projects"]))
    else:
        st.write("Projects not detected")
    st.subheader("Honors\n")
    if "honors" in sections:
        st.write(fn.remove_square_brackets(sections["honors"]))
    else:
        st.write("Honors not detected")
    st.subheader("Certificates\n")
    if "certificates" in sections:
        st.write(fn.remove_square_brackets(sections["certificates"]))
    else:
        st.write("certificates not detected")
    st.subheader("Publications\n")
    if "publications" in sections:
        st.write(fn.remove_square_brackets(sections["publications"]))
    else:
        st.write("publications not detected")

if __name__ == "__main__":

    main()
