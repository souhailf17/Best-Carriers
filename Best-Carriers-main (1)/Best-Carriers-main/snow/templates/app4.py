from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionnaire de données 
carriers = {
  "Casablanca": {"CTM": [0,1,2,3,4,5], "SDTM": [0,1,2,3,4,5]},
  # etc...
}

def trouver_meilleur(ville, jour):

  if ville not in carriers:
    return None

  for t, jours in carriers[ville].items():  
    if jour in jours:
      return t

  return None

@app.route('/', methods=['GET','POST'])
def index():

  if request.method == 'POST':
    ville = request.form['ville']
    jour = int(request.form['jour'])

    transporteur = trouver_meilleur(ville, jour)

  return render_template('index.html', transporteur=transporteur) 

if __name__ == '__main__':
  app.run(debug=True)