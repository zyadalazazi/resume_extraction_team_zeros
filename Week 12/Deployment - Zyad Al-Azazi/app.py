from flask import Flask,render_template,url_for,request
import re
import pandas as pd
import spacy
from spacy import displacy
import pickle
import os
import docx
import sys, fitz

def getTextFromDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getTextFromPDF(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text = text + str(page.getText())

    tx = " ".join(text.split('\n'))
    return tx

#def resumeData(text,model):
#    '''
#    Data should be in the Format demonstrated in test mode 
#    
#    '''
#    nlp_model = spacy.load(open(model, 'rb'))
#    doc = nlp_model(text)
#    final_output = ""
#    for ent in doc.ents:
#        final_output += f'{ent.label_.upper():{30}}- {ent.text}\n'
#    
#    return final_output

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

ner_model = pickle.load(open("trainFile", 'rb'))

@app.route('/')
def home():
	return render_template("first_page_design.html")

@app.route('/extract', methods = ["POST"])
def extract():
    if request.method == 'POST':
        document = request.form['document']
        doc_name = os.path.basename(document)
        resume_text = ""
        
        if(doc_name.endswith(".docx")):
            resume_text = getTextFromDoc(document)
        elif(doc_name.endswith(".pdf")):
            resume_text = getTextFromPDF(document)
        elif(doc_name.endswith(".txt")):
            resume_text = document
        else:
            print("Invalid Format!\nPlease input a file of the following formats: .pdf, .docx and .txt")
        
        #rawtext = resumeData(resume_text, "trainFile")
        rawtext = ner_model[0].predict(resume_text)
        doc = nlp(rawtext)
        d = []
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=('named entity', 'output'))
            NAME_named_entity = df.loc[df['named entity'] == 'NAME']['output']
            DESIGNATION_named_entity = df.loc[df['named entity'] == 'DESIGNATION']['output']
            EMAIL_named_entity = df.loc[df['named entity'] == 'EMAIL']['output']
            LOCATION_named_entity = df.loc[df['named entity'] == 'LOCATION']['output']
            COMPANIES_named_entity = df.loc[df['named entity'] == 'COMPANIES WORKED AT']['output']
            COLLEGE_named_entity = df.loc[df['named entity'] == 'COLLEGE']['output']
            GRADUATION_named_entity = df.loc[df['named entity'] == 'GRADUATION YEAR']['output']
            PHONE_named_entity = df.loc[df['named entity'] == 'PHONE NUMBER']['output']
            SKILLS_named_entity = df.loc[df['named entity'] == 'SKILLS']['output']
            
#		if choice == 'organization':
#			results = ORG_named_entity
#			num_of_results = len(results)
#		elif choice == 'person':
#			results = PERSON_named_entity
#			num_of_results = len(results)
#		elif choice == 'geopolitical':
#			results = GPE_named_entity
#			num_of_results = len(results)
#		elif choice == 'money':
#			results = MONEY_named_entity
#			num_of_results = len(results)

        output = NAME_named_entity+", "+DESIGNATION_named_entity+", "+EMAIL_named_entity+", "+LOCATION_named_entity+", "+COMPANIES_named_entity+", "+COLLEGE_named_entity+", "+GRADUATION_named_entity+", "+PHONE_named_entity+", "+SKILLS_named_entity

        return render_template('first_page_design.html', output) #, DESIGNATION_named_entity, EMAIL_named_entity



if __name__ == '__main__':
	app.run(debug=True)