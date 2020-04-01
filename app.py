import os
import json
from flask import Flask, render_template, request


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showEncode')
def showEncode():
   return render_template('encode.html')

@app.route('/showDecode')
def showDecode():
   return render_template('decode.html')

@app.route('/handleEncode', methods = ['POST'])  
def handleEncode():  
    if request.method == 'POST':  
        audioFile = request.files['file']  
        secretMsg = request.form['secret']
        print(audioFile)
        print(secretMsg)
        return json.dumps({
            'data': 'Encoding successfully'
        })  

@app.route('/handleDecode', methods = ['POST'])  
def handleDecode():  
    if request.method == 'POST':  
        audioFile = request.files['file']  
        print(audioFile)
        return json.dumps({
            'data': 'Decoding successfully'
        })  

if __name__ == "__main__":
  app.run()