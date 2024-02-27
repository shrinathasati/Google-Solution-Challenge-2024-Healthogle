from flask import Flask, render_template, request, redirect, url_for
import os
import fitz  # PyMuPDF
from docx import Document
import smtplib
import ssl
from twilio.rest import Client
from email.message import EmailMessage
import tabula
from tabula.io import read_pdf
import pandas as pd
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file selected.", 400

    resume_file = request.files['resume']

    if resume_file.filename == '' or not allowed_file(resume_file.filename):
        return "Invalid file.", 400

    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes')
    os.makedirs(upload_folder, exist_ok=True)
    resume_path = os.path.join(upload_folder, resume_file.filename)
    resume_file.save(resume_path)

    extracted_text = pdf_to_text(resume_path)
    pdf_to_csv(resume_path)
    print(type(extracted_text))

    # output_file_path = os.path.join(upload_folder, 'output.txt')
    # with open(output_file_path, 'w', encoding='utf-8') as output_file:
    #     output_file.write(extracted_text)


    return {"message": "Resume uploaded successfully.", "extracted_text": extracted_text}


def pdf_to_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ''
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text()
    pdf_document.close()
    return text


def pdf_to_csv(pdf_path):
    df = tabula.io.read_pdf(pdf_path, pages='all')
    if isinstance(df, list):
        df = pd.concat(df)
    csv_output_path = "output.csv"
    df.to_csv(csv_output_path, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)

        resume_file = request.files['resume']

        if resume_file.filename == '' or not allowed_file(resume_file.filename):
            return redirect(request.url)

        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes')
        os.makedirs(upload_folder, exist_ok=True)
        resume_path = os.path.join(upload_folder, resume_file.filename)
        resume_file.save(resume_path)

        extracted_text = pdf_to_text(resume_path)

        # match(extracted_text)

        print(type(extracted_text))

        return render_template('success.html', extracted_text=extracted_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=80)
