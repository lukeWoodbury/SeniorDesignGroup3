# LSTM and CNN for sequence classification in the IMDB dataset
import numpy as np
import os
import csv
from scipy.io.wavfile import read
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.backend import set_image_dim_ordering
from scipy.signal.wavelets import wavedec
from random import shuffle

"""def dataFeed( audioDataFile, outputsFile ):
    outputs = np.loadtxt( outputsFile, delimiter = "," )
    while( True ):
        with open( audioDataFile ) as csvFile:
            audioData = csv.reader( csvFile )
            for audio, output in zip( audioData, outputs ):"""
                
            

# fix random seed for reproducibility
np.random.seed(7)
#max_audio_length = 10 * 44100

# load outputs

# loads batches of paired inputs and outputs
def dataFeed( batchSize, audioSegmentLength, outputLength ):
    outputs = np.loadtxt( "outputs.csv", delimiter = "," )
    rootdir = '/home/jacob/Speakers/processed wav files/'
    paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
    newOutput = np.zeros( ( batchSize, outputLength ) )
    batchCount = 0
    speakerList = []
    sampleCount = 0
    with open( "order.csv", 'rb' ) as csvFile:
        speakerOrder = csv.reader( csvFile )
        speakerList = list( speakerOrder )[0]
    while True:
        shuffle( speakerList )
        for speaker, output in zip( speakerList, outputs ):
            wav = read( rootdir + speaker + ".wav" )
            if len( wav[1].shape ) == 1:
                wavData = np.array( wav[1], dtype = float )
            else:
                wavData = wav[1].astype(float).sum( axis = 1 ) / 2.0
            dataCount = 0
            for val in wavData:
                paddedWavData[batchCount][dataCount][0] = val
                dataCount += 1
                if dataCount == audioSegmentLength:
                    dataCount = 0
                    for val, i in zip( output, range( len( output ) ) ):
                        newOutput[batchCount][i] = val
                    batchCount += 1
                    sampleCount += 1
                    if batchCount == batchSize:
                        batchCount = 0
                        yield( paddedWavData, newOutput )
                        paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                        newOutput = np.zeros( ( batchSize, outputLength ) )
            batchCount += 1
            sampleCount += 1
            if batchCount == batchSize:
                batchCount = 0
                yield( paddedWavData, newOutput )
                paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                newOutput = np.zeros( ( batchSize, outputLength ) )
        print sampleCount

# definitions
batchSize = 2
audioSegmentLength = 5 * 44100
outputLength = 526

#myDataFeed = dataFeed( batchSize, audioSegmentLength, outputLength )
#while True:
    #next( myDataFeed )

# build model
model = Sequential()
model.add(Convolution1D(nb_filter=200, filter_length=3, border_mode='same', activation='relu', input_dim = 1, input_length = audioSegmentLength ) )
#model.add( Convolution1D( nb_filter = 100, filter_length = 3, border_mode = 'same' ) )
model.add( LSTM( 100, return_sequences = True ) )
model.add( TimeDistributed( Dense( 200, activation = 'sigmoid' ) ) )
model.add( TimeDistributed( Dense( 200, activation = 'relu' ) ) )
model.add( Convolution1D( nb_filter = 100, filter_length = 3, border_mode = 'same' ) )
model.add( LSTM( 50 ) )
#model.add( Convolution1D( nb_filter = 50, filter_length = 3, border_mode = 'same', activation = 'relu' ) )
model.add( Dense( 100, activation = 'relu') )
#model.add( MaxPooling1D( pool_length = 2 ) )
model.add(Dense( outputLength, activation='sigmoid' ) )
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit_generator( dataFeed( batchSize, audioSegmentLength, outputLength ), samples_per_epoch = 13868, nb_epoch = 4, max_q_size = 2, verbose = 1 )
        
#cpu time: 277k