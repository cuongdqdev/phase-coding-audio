import numpy as np
import scipy as sp
import scipy.io.wavfile

fname = 'file_example_WAV_5MG.wav'
msg = 'Dang Quoc Cuong testing'


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

encode(fname, msg)