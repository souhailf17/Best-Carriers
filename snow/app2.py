import csv
from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)

carriers = {}

def load_data_from_csv(file_path):
    with open(file_path, 'r', newline='', encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == 'CTM':
                dest = row[1]
                days = [i for i, day in enumerate(row[2:]) if day == 'X']
                carriers[dest] = {'CTM': days}
            elif row[0] == 'SDTM':
                dest = row[1]
                days = [i for i, day in enumerate(row[2:]) if day == 'X']
                if dest in carriers:
                    carriers[dest]['SDTM'] = days
                else:
                    carriers[dest] = {'SDTM': days}
            elif row[0] == 'LA VOIE EXPRESS':
                dest = row[1]
                days = [i for i, day in enumerate(row[2:]) if day == 'X']
                if dest in carriers:
                    carriers[dest]['LA VOIE EXPRESS'] = days
                else:
                    carriers[dest] = {'LA VOIE EXPRESS': days}

# ... (autres fonctions et routes)
@app.route('/')
def home():
    return render_template('app.html')

@app.route('/traiter', methods=['POST'])
def traiter():
  Ville = request.form['ville'] 
  Jour = request.form['jour']
  # appeler fonction pour récupérer données CSV
  data = get_data(ville, jour) 
  return render_template('app.html', data=data)



if __name__ == '__main__':
    file1_path = 'file1.csv'
    file2_path = 'file2.csv'
    file3_path = 'file3.csv'
    
    load_data_from_csv(file1_path)
    load_data_from_csv(file2_path)
    load_data_from_csv(file3_path)

    app.run(debug=True)
