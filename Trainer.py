# LSTM and CNN for sequence classification in the IMDB dataset
import numpy as np
import os
import csv
from scipy.io.wavfile import read
from keras.models import Sequential
from keras.models import Model
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Input
from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.backend import set_image_dim_ordering
from scipy.signal.wavelets import wavedec
#from random import shuffle
import random
from Crypto.Random.random import randint

"""def dataFeed( audioDataFile, outputsFile ):
    outputs = np.loadtxt( outputsFile, delimiter = "," )
    while( True ):
        with open( audioDataFile ) as csvFile:
            audioData = csv.reader( csvFile )
            for audio, output in zip( audioData, outputs ):"""
                
            

# fix random seed for reproducibility
np.random.seed( 7 )
random.seed( 7 )

# convert output
def convertOutput( batchSize, flatOutputs, outputShape ):
    outputs = []
    
    # create output shape
    for outputLen in outputShape:
        outputs.append( np.zeros( ( batchSize, outputLen ) ) )
    
    for sample, sampleNum in zip( flatOutputs, range( len( flatOutputs ) ) ):
        flatOutputList = sample.tolist()
        for outputLen, i in zip( outputShape, range( len( outputShape ) ) ):
            output = []
            for _ in range( outputLen ):
                output.append( flatOutputList.pop(0) )
            outputs[i][sampleNum] = np.array( output )
    return outputs

# loads batches of paired inputs and outputs
def dataFeed( batchSize, audioSegmentLength, outputLength, outputShape ):
    # variables
    rootdir = '/home/jacob/Speakers/processed wav files/converted/'
    paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
    newOutput = [] #np.zeros( ( batchSize, outputLength ) )
    sampleCount = 0
    outputs = np.loadtxt( "outputs.csv", delimiter = "," )
    speakerOrder = []
    with open( "order.csv", 'rb' ) as csvFile:
        speakerOrder = list( csv.reader( csvFile ) )[0]
    speakerList = []
    for speaker, output in zip( speakerOrder, outputs ):
        speakerList.append( ( speaker, output ) )
    # begin infinite loop through data, shuffling each time
    while True:
        random.shuffle( speakerList )
        # begin current pass through shuffled data
        for speaker, output in speakerList:
            wav = read( rootdir + speaker + ".wav" )
            # check if mono or stereo
            if len( wav[1].shape ) == 1:
                wavData = np.array( wav[1], dtype = float )
            else:
                wavData = wav[1].astype(float).sum( axis = 1 ) / 2.0
            # begin loop through current audio file
            dataCount = max( 0, randint( -1 * audioSegmentLength, audioSegmentLength ) )
            maxClipLength = audioSegmentLength - dataCount
            clipPoint = audioSegmentLength - max( 0, randint( -1 * maxClipLength, maxClipLength ) )
            for amplitude in wavData:
                # build sample
                paddedWavData[sampleCount][dataCount][0] = amplitude / (2.**15)
                dataCount += 1
                if dataCount == clipPoint:
                    # pair sample with output
                    dataCount = max( 0, randint( -1 * audioSegmentLength, audioSegmentLength ) )
                    maxClipLength = audioSegmentLength - dataCount
                    clipPoint = audioSegmentLength - max( 0, randint( -1 * maxClipLength, maxClipLength ) )
                    newOutput.append( output )
                    sampleCount += 1
                    if sampleCount == batchSize:
                        sampleCount = 0
                        yield( paddedWavData, convertOutput( batchSize, newOutput, outputShape ) )
                        paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                        newOutput = []#np.zeros( ( batchSize, outputLength ) )
            # out of wav data in this audio file, yield current clip
            newOutput.append( output )
            sampleCount += 1
            if sampleCount == batchSize:
                sampleCount = 0
                yield( paddedWavData, convertOutput( batchSize, newOutput, outputShape ) )
                paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                newOutput = []#np.zeros( ( batchSize, outputLength ) )

# definitions
batchSize = 5
audioSegmentLength = 5 * 16000
outputLength = 526
outputShape = ( 1, 1, 1, 1, 6, 179, 122, 215 )
priorityResource = 'cpu'

'''myDataFeed = dataFeed( batchSize, audioSegmentLength, outputLength, outputShape )
while True:
    next( myDataFeed )'''

# build model
wavInputs = Input( shape = ( audioSegmentLength, 1 ), dtype='float32', name='wavInputs')
x = LSTM( 200, return_sequences = True, consume_less = priorityResource, name = 'hidden1' )( wavInputs )
x = TimeDistributed( Dense( 200, activation = 'sigmoid', name = 'hidden2' ) )( x )
x = TimeDistributed( Dense( 200, activation = 'relu', name = 'hidden3' ) )( x )
x = LSTM( 100, return_sequences = True, consume_less = priorityResource, name = 'hidden4' )( x )
x = TimeDistributed( Dense( 100, activation = 'sigmoid', name = 'hidden5' ) )( x )
x = TimeDistributed( Dense( 100, activation = 'relu', name = 'hidden6' ) )( x )
x = LSTM( 50, consume_less = priorityResource, name = 'hidden7' )( x )
x = Dense( 50, activation = 'sigmoid', name = 'hidden8' )( x )
x = Dense( 50, activation = 'relu', name = 'hidden9' )( x )
gender = Dense( 100, activation = 'sigmoid', name = 'hidden10' )( x )
gender = Dense( 100, activation = 'relu', name = 'hidden11' )( gender )
gender = Dense( 1, activation = 'sigmoid', name = 'gender' )( gender )
age = Dense( 100, activation = 'sigmoid', name = 'hidden12' )( x )
age = Dense( 100, activation = 'relu', name = 'hidden13' )( age )
age = Dense( 1, activation = 'linear', name = 'age' )( age )
onsetAge = Dense( 100, activation = 'sigmoid', name = 'hidden14' )( x )
onsetAge = Dense( 100, activation = 'relu', name = 'hidden15' )( onsetAge )
onsetAge = Dense( 1, activation = 'linear', name = 'onsetAge' )( onsetAge )
LOR = Dense( 100, activation = 'sigmoid', name = 'hidden16' )( x )
LOR = Dense( 100, activation = 'relu', name = 'hidden17' )( LOR )
LOR = Dense( 1, activation = 'linear', name = 'LOR' )( LOR )
LS = Dense( 100, activation = 'sigmoid', name = 'hidden18' )( x )
LS = Dense( 100, activation = 'relu', name = 'hidden19' )( LS )
LS = Dense( 6, activation = 'softmax', name = 'LS' )( LS )
country = Dense( 100, activation = 'sigmoid', name = 'hidden20' )( x )
country = Dense( 100, activation = 'relu', name = 'hidden21' )( country )
country = Dense( 179, activation = 'softmax', name = 'country' )( country )
ER = Dense( 100, activation = 'sigmoid', name = 'hidden22' )( x )
ER = Dense( 100, activation = 'relu', name = 'hidden23' )( ER )
ER = Dense( 122, activation = 'softmax', name = 'ER' )( ER )
NL = Dense( 100, activation = 'sigmoid', name = 'hidden24' )( x )
NL = Dense( 100, activation = 'relu', name = 'hidden25' )( NL )
NL = Dense( 215, activation = 'softmax', name = 'NL' )( NL )
model = Model( input = wavInputs, output = [gender, age, onsetAge, LOR, LS, country, ER, NL] )
losses = { 'gender': 'mse', 'age': 'mse', 'onsetAge': 'mse', 'LOR': 'mse', 'LS': 'categorical_crossentropy', 'country': 'categorical_crossentropy', 'ER': 'categorical_crossentropy', 'NL': 'categorical_crossentropy' }
csv_logger = CSVLogger('training.log')
checkpoint_logger = ModelCheckpoint('model.h5')
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.compile( optimizer = 'rmsprop', loss = losses, metrics = ['accuracy'] )
print( model.summary() )
model.fit_generator( dataFeed( batchSize, audioSegmentLength, outputLength, outputShape ), samples_per_epoch = 1000, nb_epoch = 30, max_q_size = 2, verbose = 1, callbacks=[csv_logger, checkpoint_logger] )
'''# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")'''
    
'''# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
myDataFeed = dataFeed( 1, audioSegmentLength, outputLength, outputShape )
X, Y = next( myDataFeed )
losses = { 'gender': 'mse', 'age': 'mse', 'onsetAge': 'mse', 'LOR': 'mse', 'LS': 'categorical_crossentropy', 'country': 'categorical_crossentropy', 'ER': 'categorical_crossentropy', 'NL': 'categorical_crossentropy' }
loaded_model.compile( optimizer = 'rmsprop', loss = losses, metrics = ['accuracy'] )
#loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print score
print "%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100)'''

'''# build model
model = Sequential()
model.add( LSTM( 32, input_dim = 1, input_length = audioSegmentLength ) )
model.add( Dense( outputLength, activation = 'sigmoid' ) )
model.compile( optimizer = 'rmsprop', loss = 'binary_crossentropy', metrics = ['accuracy'] )
print( model.summary() )
model.fit_generator( dataFeed( batchSize, audioSegmentLength, outputLength, outputShape ), samples_per_epoch = 13868, nb_epoch = 4, max_q_size = 2, verbose = 1 )'''

'''model = Sequential()
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
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit_generator( dataFeed( batchSize, audioSegmentLength, outputLength ), samples_per_epoch = 13868, nb_epoch = 4, max_q_size = 2, verbose = 1 )'''
