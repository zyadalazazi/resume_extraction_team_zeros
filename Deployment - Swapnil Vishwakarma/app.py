import os
import spacy
import pickle
import PyPDF2
import json
import pandas as pd
import numpy as np
from docx import Document
from werkzeug.utils import secure_filename
# from flask_restful import Resource, Api
from flask import Flask, render_template, request, jsonify, redirect

# Loading the model
model = pickle.load(open('ner_model.pkl', 'rb'))

# Loading the test file
test_data = pickle.load(open('testFile.pkl', 'rb'))

import re
import spacy
import random


ALLOWED_EXTENSIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\uploads\\'
# DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\downloads\\'


# Extracting Mobile Nnumber
def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def resumeData(text,model):
    doc = model(text)
    # result = {}
    # for ent in doc.ents:
    #     result.update({f'{ent.label_.upper()}': ent.text})
    # ph_number = extract_mobile_number(text)
    # if ph_number:
    #     result.update({'PHONE NUMBER': ph_number})
    # return result

    company = [ee for ee in doc.ents if ee.label_ == 'COMPANY']
    name = [ee for ee in doc.ents if ee.label_ == 'NAME']
    designation = [ee for ee in doc.ents if ee.label_ == 'DESIG']
    degree = [ee for ee in doc.ents if ee.label_ == 'DEG']
    graduationYear = [ee for ee in doc.ents if ee.label_ == 'GRADYEAR']
    skills = [ee for ee in doc.ents if ee.label_ == 'SKILLS']
    collegeName = [ee for ee in doc.ents if ee.label_ == 'CLG']
    location = [ee for ee in doc.ents if ee.label_ == 'LOC']
    email = [ee for ee in doc.ents if ee.label_ == 'EMAIL']
    phoneNumber = [ee for ee in doc.ents if ee.label_ == 'PHONE NUMBER']

    data={"company":company,
            "name":name,
            "designation":designation,
            "degree":degree,
            "graduationYear":graduationYear,
            "skills":skills,
            "collegeName":collegeName,
            "location":location,
            "email": email,
            "phone": phoneNumber
            }
    return data


# Reading text from PDF
def read_PDF(filename):
    with open(filename,'rb') as pdf_file:
        content = ""
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = read_pdf.getPage(page_number)
            page_content = page.extractText()
            content += page_content
    return content

# text = read_PDF('resume sample.pdf')
# print(text)

# Reading text from docx
def read_DOCX(filename):
    document = Document(filename)
    content = ""
    for para in document.paragraphs:
        content += para.text
    return content

# text = read_DOCX('resume sample.docx')
# print(text)





# text = "Alice Clark  AI / Machine Learning    Delhi, India Email me on Indeed  •  20+ years of experience in data handling, design, and development  •  Data Warehouse: Data analysis, star/snow flake scema data modelling and design specific to  data warehousing and business intelligence  •  Database: Experience in database designing, scalability, back-up and recovery, writing and  optimizing SQL code and Stored Procedures, creating functions, views, triggers and indexes.  Cloud platform: Worked on Microsoft Azure cloud services like Document DB, SQL Azure,  Stream Analytics, Event hub, Power BI, Web Job, Web App, Power BI, Azure data lake  analytics(U-SQL)  Willing to relocate anywhere    WORK EXPERIENCE  Software Engineer  Microsoft – Bangalore, Karnataka  January 2000 to Present  1. Microsoft Rewards Live dashboards:  Description: - Microsoft rewards is loyalty program that rewards Users for browsing and shopping  online. Microsoft Rewards members can earn points when searching with Bing, browsing with  Microsoft Edge and making purchases at the Xbox Store, the Windows Store and the Microsoft  Store. Plus, user can pick up bonus points for taking daily quizzes and tours on the Microsoft  rewards website. Rewards live dashboards gives a live picture of usage world-wide and by  markets like US, Canada, Australia, new user registration count, top/bottom performing rewards  offers, orders stats and weekly trends of user activities, orders and new user registrations. the  PBI tiles gets refreshed in different frequencies starting from 5 seconds to 30 minutes.  Technology/Tools used    EDUCATION  Indian Institute of Technology – Mumbai  2001    SKILLS  Machine Learning, Natural Language Processing, and Big Data Handling    ADDITIONAL INFORMATION  Professional Skills  • Excellent analytical, problem solving, communication, knowledge transfer and interpersonal  skills with ability to interact with individuals at all the levels  • Quick learner and maintains cordial relationship with project manager and team members and  good performer both in team and independent job environments  • Positive attitude towards superiors &amp; peers  • Supervised junior developers throughout project lifecycle and provided technical assistance"
# text = "Akash Gulhane Microsoft Certified System Engineer  Amravati, Maharashtra - Email me on Indeed: indeed.com/r/Akash- Gulhane/8b86faac48268d09  I want to work with a progressive organization where I can utilize my knowledge and skills for the benefit of the company.  WORK EXPERIENCE  Microsoft Certified System Engineer  -  2012 to 2012  Technical Skills: CCNA (Cisco Certified Network Associate)  Database: MS-Access Other: Hardware & Networking, Core Java, C, C++  Operating Systems: Windows server O.S 2012, Windows XP/7/8 User Level Final Year Project: Two factor data access control with efficient revocation for Name of Project: multy-authority Cloud Storage System Team Size: 3 My Role: Software Developer .net Front End Tool: Database: SQL Server 2000  Environment: JRE (Java Runtime Environment) Objective:  Personal  Narsamma -  Amravati, Maharashtra -  2010 to 2010  53 College  Ramkrishna krida High -  Amravati, Maharashtra -  https://www.indeed.com/r/Akash-Gulhane/8b86faac48268d09?isid=rex-download&ikw=download-top&co=IN https://www.indeed.com/r/Akash-Gulhane/8b86faac48268d09?isid=rex-download&ikw=download-top&co=IN   2008 to 2008  63 School  Computer Skills:"
text = test_data['content'][187] # 186
# print(text)
res = resumeData(text, model)
print(res)

# app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/resume')
def resume():
    # res = resumeData(text, model)
    # return jsonify(res)

    resume_data = resumeData(text, model)
    df = pd.DataFrame.from_dict(resume_data, orient='index')
    df = df.transpose()
    df.to_csv('resume_datam.csv')
    data = pd.read_csv('resume_datam.csv')
    data.replace(to_replace = ':', value=" ", regex=True, inplace=True)
    data.replace(to_replace = '"', value=" " ,regex=True, inplace=True)
    data.replace(to_replace = "'", value=" ", regex=True, inplace=True)
    data.replace(to_replace = np.NaN, value=" ", regex=True, inplace=True)
    data.to_json('resume_datam.json')
    jsonnewdata = open('resume_datam.json')
    jsonnewdata = json.load(jsonnewdata)

    return (jsonnewdata)

# Get details from the test data randomly
@app.route('/testdata')
def test():
    s = random.randint(180, 199)
    text = test_data['content'][s]
    resume_data = resumeData(text, model)
    df = pd.DataFrame.from_dict(resume_data, orient='index')
    df = df.transpose()
    df.to_csv('resume_datam.csv')
    data = pd.read_csv('resume_datam.csv')
    data.replace(to_replace = ':', value=" ", regex=True, inplace=True)
    data.replace(to_replace = '"', value=" " ,regex=True, inplace=True)
    data.replace(to_replace = "'", value=" ", regex=True, inplace=True)
    data.replace(to_replace = np.NaN, value=" ", regex=True, inplace=True)
    data.to_json('resume_datam.json')
    jsonnewdata = open('resume_datam.json')
    jsonnewdata = json.load(jsonnewdata)

    return jsonnewdata

@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # return filename
            filename = filename.replace("_", " ")
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if filename.endswith(".pdf"):
                text = read_PDF(filename)
            else:
                text = read_DOCX(filename)

            resume_data = resumeData(text, model)
            df = pd.DataFrame.from_dict(resume_data, orient='index')
            df = df.transpose()
            df.to_csv('resume_datam.csv')
            data = pd.read_csv('resume_datam.csv')
            data.replace(to_replace = ':', value=" ", regex=True, inplace=True)
            data.replace(to_replace = '"', value=" " ,regex=True, inplace=True)
            data.replace(to_replace = "'", value=" ", regex=True, inplace=True)
            data.replace(to_replace = np.NaN, value=" ", regex=True, inplace=True)
            data.to_json('resume_datam.json')
            jsonnewdata = open('resume_datam.json')
            jsonnewdata = json.load(jsonnewdata)
            return jsonnewdata
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            # return redirect(url_for('uploaded_file', filename=filename))

    return render_template('file.html')

if __name__ == "__main__":
    app.run(debug=True)