import numpy as np
import scipy as sp
import scipy.io.wavfile
import gc, re, string

fname = 'steg_file_example_WAV_5MG.wav'

rate, channels = sp.io.wavfile.read(fname)
channels = channels.copy()
rate, channels.shape

flag = 0

def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

while flag == 0:
    y = int(input("Input maximum letter(s): "))
    for i in range(3,y):
        # msglen = int(input("Input message length: "))
        msglen = 8*i
        seglen = 2*int(2**np.ceil(np.log2(2*msglen)))
        # print(seglen.bit_length())
        # print(type(seglen))
        segmid = seglen // 2

        if len(channels.shape) == 1:
            x = channels[:seglen]
        else:
            x = channels[:seglen,0]

        # print(x)

        x = (np.angle(np.fft.fft(x))[segmid-msglen:segmid] < 0).astype(np.int8)
        x = x.reshape((-1,8)).dot(1 << np.arange(8 - 1, -1, -1))
        # print(x, type(x))
        text = ''.join(np.char.mod('%c',x))
        # print(text, type(text))
        # print(''.join(np.char.mod('%c',x)))

        if is_alpha(text[0]):
            text = re.sub(r'[^a-zA-Z0-9,._ ]', r'', text)
            print(text, '\n')
            # break
        else:
            gc.collect()

    choice = str(input("Do you want to try again? (Y/y) or (N/n): "))
    if choice in ("Y","y"):
        flag == 0
    else:
        break       

        
