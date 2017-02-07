# LSTM and CNN for sequence classification in the IMDB dataset
import numpy as np
import os
import csv
from scipy.io.wavfile import read
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.backend import set_image_dim_ordering
from scipy.signal.wavelets import wavedec

"""def dataFeed( audioDataFile, outputsFile ):
    outputs = np.loadtxt( outputsFile, delimiter = "," )
    while( True ):
        with open( audioDataFile ) as csvFile:
            audioData = csv.reader( csvFile )
            for audio, output in zip( audioData, outputs ):"""
                
            

# fix random seed for reproducibility
np.random.seed(7)
max_audio_length = 10 * 44100

# load outputs

def dataFeed():
    while True:
        outputs = np.loadtxt( "outputs.csv", delimiter = "," )
        rootdir = '/home/jacob/Speakers/processed wav files/'
        with open( "order.csv", 'rb' ) as csvFile:
            speakerOrder = csv.reader( csvFile )
            speakerList = list( speakerOrder )[0]
            for speaker, output in zip( speakerList, outputs ):
                wav = read( rootdir + speaker + ".wav" )
                wavData = np.array( wav[1], dtype = float )
                paddedWavData = np.zeros( ( 1, max_audio_length, 1 ) )
                for val, i in zip( wavData, range( len( wavData ) ) ):
                    if i == max_audio_length:
                        break
                    paddedWavData[0][i][0] = val
                newOutput = np.zeros( ( 1, 4 ) )#len( output ) ) )
                for val, i in zip( output, range( 4 ) ):#len( output ) ) ):
                    newOutput[0][i] = val
                yield( paddedWavData, newOutput )
                
# build model
#set_image_dim_ordering('tf')
model = Sequential()
model.add(Convolution1D(nb_filter=32, filter_length=3, border_mode='same', activation='relu', input_dim = 1, input_length = max_audio_length))
model.add(MaxPooling1D(pool_length=2))
model.add(LSTM( 25 ) )
#model.add( Convolution1D( nb_filter = 32, filter_length = 3, border_mode = 'same', activation = 'relu' ) )
#model.add( MaxPooling1D( pool_length = 2 ) )
model.add(Dense( 4, activation='sigmoid' ) )
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit_generator( dataFeed(), samples_per_epoch = 10, nb_epoch = 4, nb_worker = 2, verbose = 1 )
        
# truncate and pad input sequences
#wavDatas = sequence.pad_sequences(wavDatas, maxlen=max_review_length)
#X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)