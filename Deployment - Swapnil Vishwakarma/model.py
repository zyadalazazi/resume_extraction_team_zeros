import spacy
from spacy.util import decaying
import pickle
import random
import pandas as pd
import datetime


model_file="ner_model"
iterations=29
dropout = decaying(base_rate=0.6, decay=0.2, t=1e-4)

df = pd.read_json('Resume.json', lines=True)

# Splitting the df into train and test data
train_data = df[:180]
test_data = df[180:]

# Personal Custom Tags Dictionary
entity_dict = {
    'Name': 'NAME', 
    'College Name': 'CLG',
    'Degree': 'DEG',
    'Graduation Year': 'GRADYEAR',
    'Years of Experience': 'YOE',
    'Companies worked at': 'COMPANY',
    'Designation': 'DESIG',
    'Skills': 'SKILLS',
    'Location': 'LOC',
    'Email Address': 'EMAIL'
    }

def mergeIntervals(intervals):
    sorted_by_lower_bound = sorted(intervals, key=lambda tup: tup[0])
    merged = []
# lower and higher represent the bounds of the current run of merges
    for higher in sorted_by_lower_bound:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # test for intersection between lower and higher:
            if higher[0] <= lower[1]: # new interval overlaps current run
                if lower[2] is higher[2]:
                    upper_bound = max(lower[1], higher[1]) # merge with the current run
                    merged[-1] = (lower[0], upper_bound, lower[2]) # replace by merged interval
                else:
                    if lower[1] > higher[1]:
                        merged[-1] = lower
                    else:
                        merged[-1] = (lower[0], higher[1], higher[2])
            else:
                merged.append(higher)

    return merged

def get_entities(train_data):
    
    entities = []
    
    for i in range(len(train_data)):
        entity = []
    
        for annot in train_data['annotation'][i]:
            try:
                ent = entity_dict[annot['label'][0]]
                start = annot['points'][0]['start']
                end = annot['points'][0]['end'] + 1
                entity.append((start, end, ent))
            except:
                pass
    
        entity = mergeIntervals(entity)
        entities.append(entity)
    
    return entities

train_data['entities'] = get_entities(train_data)

a = []
for i in range(len(train_data)):
    a.append((train_data['content'][i],{'entities':train_data['entities'][i]}))

import re


def trim_entity_spans(data: list) -> list:
    """Removes leading and trailing white spaces from entity spans.

    Args:
        data (list): The data to be cleaned in spaCy JSON format.

    Returns:
        list: The cleaned data.
    """
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data

a = trim_entity_spans(a)

nlp = spacy.blank('en')  
print("Created blank NLP model")

# Create NLP Pipeline
if 'ner' not in nlp.pipe_names:
    ner_pipe = nlp.add_pipe('ner')
else:
    ner_pipe = nlp.get_pipe('ner')

# Add entities labels to the ner pipeline
for text, annotations in a:
    for entity in annotations.get('entities'):
        ner_pipe.add_label(entity[2].upper())

from spacy.training.example import Example
# get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

### START
start = datetime.datetime.now()

# train NER Model
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.initialize()
    for itn in range(iterations):
        print("Iteration Number:" + str(itn))
        random.shuffle(a)
        losses = {}
        for text, annotations in a:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer,losses=losses, drop=next(dropout, -1))
            print("losses", losses)

nlp.to_disk('nlp_ner_model')
nlp_model = spacy.load('nlp_ner_model')

# Pickling nlp model
pickle.dump(nlp_model, open('ner_model.pkl', 'wb'))

# Pickling test data
pickle.dump(test_data, open('testFile.pkl', 'wb'))



#### END
print(f"\n\n\n\n Total time taken for training: \n {datetime.datetime.now() - start}")
