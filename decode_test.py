import numpy as np
import scipy as sp
import scipy.io.wavfile
import gc, re, string

fname = 'steg_encodingAudio.wav'
msgLength = 200

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
                print(text, '\n')
                resultList.append(text);
            else:
                gc.collect()

        break    
    return resultList   


print(decode(fname, msgLength))      
