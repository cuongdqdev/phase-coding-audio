import os
import json
import numpy as np
import scipy as sp
import scipy.io.wavfile
import gc, re, string
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['wav'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode(fname, msg):
    rate, channels = sp.io.wavfile.read(fname)
    channels = channels.copy()

    msglen = 8 * len(msg)

    seglen = int(2 * 2**np.ceil(np.log2(2*msglen)))
    segnum = int(np.ceil(channels.shape[0]/seglen))

    if len(channels.shape) == 1:
        channels.resize(segnum*seglen, refcheck=False)
        channels = channels[np.newaxis]
    else:
        channels.resize((segnum*seglen, channels.shape[1]), refcheck=False)
        channels = channels.T

    msgbin = np.ravel([[int(y) for y in format(ord(x), '08b')] for x in msg])
    msgPi = msgbin.copy()
    msgPi[msgPi == 0] = -1
    msgPi = msgPi * -np.pi/2

    segs = channels[0].reshape((segnum,seglen))

    segs = np.fft.fft(segs)
    M = np.abs(segs)
    P = np.angle(segs)

    dP = np.diff(P, axis=0)

    segmid = seglen // 2
    P[0,-msglen+segmid:segmid] = msgPi
    P[0,segmid+1:segmid+1+msglen] = -msgPi[::-1]
    for i in range(1, len(P)): P[i] = P[i-1] + dP[i-1]

    segs = (M * np.exp(1j * P))
    segs = np.fft.ifft(segs).real
    channels[0] = segs.ravel().astype(np.int16)
    sp.io.wavfile.write('steg_'+fname, rate, channels.T)
    return 'steg_'+fname

def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

def decode(fname, msgLength):
    resultList = []
    rate, channels = sp.io.wavfile.read(fname)
    channels = channels.copy()
    rate, channels.shape
    flag = 0
    while flag == 0:
        y = int(msgLength)
        for i in range(3,y):
            msglen = 8*i
            seglen = 2*int(2**np.ceil(np.log2(2*msglen)))
            segmid = seglen // 2

            if len(channels.shape) == 1:
                x = channels[:seglen]
            else:
                x = channels[:seglen,0]

            x = (np.angle(np.fft.fft(x))[segmid-msglen:segmid] < 0).astype(np.int8)
            x = x.reshape((-1,8)).dot(1 << np.arange(8 - 1, -1, -1))
            text = ''.join(np.char.mod('%c',x))

            if is_alpha(text[0]):
                text = re.sub(r'[^a-zA-Z0-9,._ ]', r'', text)
                resultList.append(text);
            else:
                gc.collect()

        break    
    return resultList   


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
        newAudioName = 'encodingAudio.wav'
        audioFile.save(newAudioName)
        if os.path.exists("steg_encodingAudio.wav"):
            os.remove("steg_encodingAudio.wav") 
        encode(newAudioName, secretMsg) 
        os.remove(newAudioName)
        return jsonify(
            error=False,
            data='steg_encodingAudio.wav'
        )

@app.route('/handleDecode', methods = ['POST'])  
def handleDecode():  
    if request.method == 'POST':  
        audioFile = request.files['file']  
        secretLength = request.form['secret']
        
        newAudioName = 'decodingAudio.wav'
        if os.path.exists(newAudioName):
            os.remove(newAudioName) 

        audioFile.save(newAudioName)
        data = decode(newAudioName, secretLength)
        os.remove(newAudioName)
        return jsonify(
            error=False,
            data=data
        )


@app.route('/downloadFile/<filename>')
def downloadFile(filename):
    file_path = filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
  app.run()