import numpy as np
import scipy as sp
import scipy.io.wavfile

fname = 'steg_file_example_WAV_5MG.wav'

rate, channels = sp.io.wavfile.read(fname)
channels = channels.copy()
rate, channels.shape

msglen = 8 * 4
seglen = 2*int(2**np.ceil(np.log2(2*msglen)))
segmid = seglen // 2

if len(channels.shape) == 1:
    x = channels[:seglen]
else:
    x = channels[:seglen,0]
x = (np.angle(np.fft.fft(x))[segmid-msglen:segmid] < 0).astype(np.int8)
x = x.reshape((-1,8)).dot(1 << np.arange(8 - 1, -1, -1))
''.join(np.char.mod('%c',x))

print(''.join(np.char.mod('%c',x)))