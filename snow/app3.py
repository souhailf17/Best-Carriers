import csv 
from flask import Flask, request, render_template
import logging

app = Flask(__name__)

carriers = {}
data = """
CTM, Rabat, X, X, X, X, X, X, X, X
CTM, Casablanca, X, X, X, X, X, X, X, X  
CTM, Tangier, X, X, X, X, X, X, X, X  
CTM, Khouribga, X, X, X, X, X, X, X, X  
CTM, Nador, X, X, X, X, X, X, X, X  
CTM, Essaouira, X, X, X, X, X, X, X, X  
CTM, Errachidia, X, X, X, X, X, X, X, X  
CTM, Tetouan, X, X, X, X, X, X, X, X  
CTM, Agadir, X, X, X, X, X, X, X, X  
CTM, Midelt, X, X, X, X, X, X, X, X  
CTM, Ouarzazate, X, X, X, X, X, X, X, X  
SDTM, Rabat, X, X, X, X, X, X, X, X, X 
SDTM, Taza, X, X, X, X, X, X, X, X, X  
SDTM, Meknes, X, X, X, X, X, X, X, X, X  
SDTM, Marrakech, X, X, X, X, X, X, X, X, X  
SDTM, Safi, X, X, X, X, X, X, X, X, X  
SDTM, Taroudant, X, X, X, X, X, X, X, X, X  
SDTM, Al Hoceima, X, X, X, X, X, X, X, X, X
SDTM, Beni Mellal, X, X, X, X, X, X, X, X, X  
SDTM, K Tadla, X, X, X, X, X, X, X, X, X  
SDTM, Bouskoura, X, X, X, X, X, X, X, X, X  
SDTM, Mediouna, X, X, X, X, X, X, X, X, X 
SDTM, Had soualem, X, X, X, X, X, X, X, X, X  
SDTM, Settat, X, X, X, X, X, X, X, X, X 
SDTM, Tangier, X, , X, , X,
LA VOIE EXPRESS, Casablanca, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Khenifra, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, El Jadida, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Tiznit, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Midelt, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Meknes, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Fes, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Ait Melloul, X, X, X, X, X, X, X, X, X
LA VOIE EXPRESS, Oujda, X, X, X, X, X, X, X, X, X
"""
# Parse CTM data
rows = data.split('\n')
for row in rows:
    if row.startswith('CTM'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        carriers[dest] = {'CTM': days}
        
# Parse SDTM data
for row in rows:
    if row.startswith('SDTM'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        if dest in carriers:
            carriers[dest]['SDTM'] = days
        else:
            carriers[dest] = {'SDTM': days}
            

# Parse LA VOIE EXPRESS data            
for row in rows:
    if row.startswith('LA VOIE EXPRESS'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        if dest in carriers:
            carriers[dest]['LA VOIE EXPRESS'] = days
        else:
            carriers[dest] = {'LA VOIE EXPRESS': days}
            
@app.route('/')
def home():

    return render_template('app.html')

def trouver_meilleur(ville, jour):

  # Parcourir le dictionnaire carriers
  for transporteur, jours in carriers[ville].items():
    
    # Vérifier si le jour est dans la liste
    if jour in jours:
        
      # Retourner le nom du transporteur
      return transporteur
  
  # Transporteur non trouvé    
  return None 

@app.route('/', methods=['GET','POST'])
def home1():

  if request.method == 'POST':

    ville = request.form['ville']
    jour = request.form['jour']
    
    # Trouver meilleur transporteur    
  transporteur = trouver_meilleur(ville, int(jour))    
  return render_template('app.html', transporteur=transporteur, ville=ville)
    
    # traitement des données
    
# Get best carrier for destination     
if __name__ == "__main__":
    app.run(debug=True)