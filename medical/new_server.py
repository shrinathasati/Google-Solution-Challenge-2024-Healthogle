from flask import Flask, request, jsonify
import os
import fitz
import tabula
import pandas as pd
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ''
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text()
    pdf_document.close()
    return text

def pdf_to_csv(pdf_path):
    data = tabula.read_pdf(pdf_path, pages='all')
    if isinstance(data, list):
        data = pd.concat(data)
    csv_output_path = "output.csv"
    data = data[['Test Name', 'Results (IU/L or\rmg/dL)']]
    data = data.drop(6)
    data = data.drop(7)
    data = data.drop(8)
    data = data.drop(9)
    data = data.drop(10)
    data = data.drop(11)
    # data.to_csv(csv_output_path, index=False)
    json_data = data.to_json()
    return json_data

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
    json_data = pdf_to_csv(resume_path)

    return jsonify({"message": "Resume uploaded successfully.", "extracted_text": extracted_text, "data": json.loads(json_data)})



if __name__ == '__main__':
    app.run(debug=True, port=80)
