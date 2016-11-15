'''
Created on Nov 08, 2016

@author: Jacob Morris
'''

from scipy.io.wavfile import read

a = read( "wavfile.wav" )
wavData = numpy.array( a[1], dtype = float )

for i in wavData:
    print i