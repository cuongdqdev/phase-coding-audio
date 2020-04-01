import os
from flask import Flask, render_template, request


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showDemo')
def showSignUp():
   return render_template('demo.html')

@app.route('/uploadAudio', methods = ['POST'])  
def uploadAudio():  
    if request.method == 'POST':  
        audioFile = request.files['file']  
        secretMsg = request.form['secret']
        print(audioFile)
        print(secretMsg)
        return render_template("demo.html")  
if __name__ == "__main__":
  app.run()