#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import glob
import pandas as pd

def parse_medical_file(file_path):
    patient_id = os.path.basename(file_path).split('_')[0]
    data = {'id' : patient_id}
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    text_element = root.find('TEXT')
    data['text'] = text_element.text

    search_fields = ['cad', 'hypertension', 'diabetes']
    for sf in search_fields:
        mention = False
        for tag in root.iter(sf.upper()):
            if tag.get('indicator') == 'mention':
                mention = True
        data[sf] = mention

    return data

def xml_to_csv(out_file: str = 'summarized_heart_data.csv'):
    all_data = []
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xml')
    for file_path in glob.glob(os.path.join(data_dir, '*.xml')):
        data = parse_medical_file(file_path)
        all_data.append(data)
    
    df = pd.DataFrame(all_data)
    df.set_index('id', inplace=True)
    df.to_csv(os.path.join(data_dir, out_file))

if __name__ == '__main__':
    xml_to_csv()