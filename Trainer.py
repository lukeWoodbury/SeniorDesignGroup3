# LSTM and CNN for sequence classification in the IMDB dataset
import numpy as np
import os
import csv
from scipy.io.wavfile import read
from keras.optimizers import RMSprop
from keras.layers import Input, Embedding, LSTM, Dense, merge
from keras.models import Sequential
from keras.models import Model
from keras.models import model_from_json
from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.backend import set_image_dim_ordering
from scipy.signal.wavelets import wavedec
from scipy.fftpack import rfft
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
    freqData = []
    newOutput = []
    sampleCount = 0
    outputs = np.loadtxt( "outputs.csv", delimiter = "," )
    speakerOrder = []
    with open( "order.csv", 'rb' ) as csvFile:
        speakerOrder = list( csv.reader( csvFile ) )[0]
    speakerList = []
    cutoff = 0
    for speaker, output in zip( speakerOrder, outputs ):
        speakerList.append( ( speaker, output ) )
        #cutoff += 1
        #if cutoff >= 2:
            #break
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
                wavData = wav[1].astype( float ).sum( axis = 1 ) / 2.0
            # begin loop through current audio file
            startPoint = randint( 0, len( wavData ) - ( audioSegmentLength * batchSize ) - 1 )
            dataCount = 0
            #freqData.append( rfft( wavData ).tolist() )
            for amplitude in wavData:
                # build sample
                if startPoint <= 0 :
                    paddedWavData[sampleCount][dataCount][0] = amplitude / (2.**15)
                    dataCount += 1
                    if dataCount == audioSegmentLength:
                        # pair sample with output
                        dataCount = 0
                        newOutput.append( output )
                        freqData.append( rfft( paddedWavData[sampleCount].T ) )
                        sampleCount += 1
                        if sampleCount == batchSize:
                            sampleCount = 0
                            yield( [ paddedWavData, np.asarray( freqData ) ], convertOutput( batchSize, newOutput, outputShape ) )
                            #yield( paddedWavData, convertOutput( batchSize, newOutput, outputShape ) )
                            paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                            newOutput = []
                            freqData = []
                            break
                else :
                    startPoint -= 1
            '''# out of wav data in this audio file, yield current clip
            newOutput.append( output )
            freqData.append( rfft( paddedWavData[sampleCount].T ) )
            sampleCount += 1
            if sampleCount == batchSize:
                sampleCount = 0
                #yield( [ paddedWavData, np.asarray( freqData ) ], convertOutput( batchSize, newOutput, outputShape ) )
                yield( paddedWavData, convertOutput( batchSize, newOutput, outputShape ) )
                paddedWavData = np.zeros( ( batchSize, audioSegmentLength, 1 ) )
                newOutput = []
                freqData = []'''

# definitions
batchSize = 400
audioSegmentLength = 441
outputLength = 529
outputShape = ( 2, 1, 1, 1, 6, 179, 122, 215 )
priorityResource = 'gpu'

'''myDataFeed = dataFeed( batchSize, audioSegmentLength, outputLength, outputShape )
while True:
    next( myDataFeed )'''
    

# build model
wavInputs = Input( shape = ( audioSegmentLength, 1 ), dtype='float32', name='wavInputs')
x = LSTM( 400, return_sequences = True, consume_less = priorityResource, name = 'hidden1' )( wavInputs )
x = TimeDistributed( Dense( 400, activation = 'sigmoid', name = 'hidden2' ) )( x )
x = TimeDistributed( Dense( 200, activation = 'relu', name = 'hidden3' ) )( x )
x = LSTM( 200, return_sequences = True, consume_less = priorityResource, name = 'hidden4' )( x )
x = TimeDistributed( Dense( 200, activation = 'sigmoid', name = 'hidden5' ) )( x )
x = TimeDistributed( Dense( 100, activation = 'relu', name = 'hidden6' ) )( x )
x = LSTM( 100, consume_less = priorityResource, name = 'hidden7' )( x )
x = Dense( 100, activation = 'sigmoid', name = 'hidden8' )( x )
x = Dense( 50, activation = 'relu', name = 'hidden9' )( x )
freqInputs = Input( shape = ( 1, audioSegmentLength ), dtype = 'float32', name = 'freqInputs' )
y = LSTM( 400, return_sequences = True, consume_less = priorityResource, name = 'hidden10' )( freqInputs )
y = TimeDistributed( Dense( 400, activation = 'sigmoid', name = 'hidden11' ) )( y )
y = TimeDistributed( Dense( 200, activation = 'relu', name = 'hidden12' ) )( y )
y = LSTM( 200, return_sequences = True, consume_less = priorityResource, name = 'hidden13' )( y )
y = TimeDistributed( Dense( 200, activation = 'sigmoid', name = 'hidden14' ) )( y )
y = TimeDistributed( Dense( 100, activation = 'relu', name = 'hidden15' ) )( y )
y = LSTM( 100, consume_less = priorityResource, name = 'hidden16' )( y )
y = Dense( 100, activation = 'sigmoid', name = 'hidden17' )( y )
y = Dense( 50, activation = 'relu', name = 'hidden18' )( y )
x = merge([x, y], mode='concat')
x = Dense( 100, activation = 'sigmoid', name = 'hidden19' )( x )
x = Dense( 50, activation = 'relu', name = 'hidden20' )( x )
gender = Dense( 50, activation = 'sigmoid', name = 'hidden21' )( x )
gender = Dense( 50, activation = 'relu', name = 'hidden22' )( gender )
gender = Dense( 2, activation = 'softmax', name = 'gender' )( gender )
age = Dense( 1, activation = 'linear', name = 'age' )( x )
onsetAge = Dense( 1, activation = 'linear', name = 'onsetAge' )( x )
LOR = Dense( 1, activation = 'linear', name = 'LOR' )( x )
LS = Dense( 50, activation = 'sigmoid', name = 'hidden23' )( x )
LS = Dense( 50, activation = 'relu', name = 'hidden24' )( LS )
LS = Dense( 6, activation = 'softmax', name = 'LS' )( LS )
country = Dense( 100, activation = 'sigmoid', name = 'hidden25' )( x )
country = Dense( 100, activation = 'relu', name = 'hidden26' )( country )
country = Dense( 179, activation = 'softmax', name = 'country' )( country )
ER = Dense( 100, activation = 'sigmoid', name = 'hidden27' )( x )
ER = Dense( 100, activation = 'relu', name = 'hidden28' )( ER )
ER = Dense( 122, activation = 'softmax', name = 'ER' )( ER )
NL = Dense( 100, activation = 'sigmoid', name = 'hidden29' )( x )
NL = Dense( 100, activation = 'relu', name = 'hidden30' )( NL )
NL = Dense( 215, activation = 'softmax', name = 'NL' )( NL )
model = Model( input = [ wavInputs, freqInputs ], output = [ gender, age, onsetAge, LOR, LS, country, ER, NL] )
losses = { 'gender': 'categorical_crossentropy', 'age': 'mse', 'onsetAge': 'mse', 'LOR': 'mse', 'LS': 'categorical_crossentropy', 'country': 'categorical_crossentropy', 'ER': 'categorical_crossentropy', 'NL': 'categorical_crossentropy' }
csv_logger = CSVLogger( 'training.log' )
checkpoint_logger = ModelCheckpoint('model.h5')
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.compile( optimizer = RMSprop( lr = .00001 ), loss = losses, loss_weights = [ 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0 ], metrics = ['accuracy'] )
print( model.summary() )
trainDataFeed = dataFeed( batchSize, audioSegmentLength, outputLength, outputShape )
testDataFeed = dataFeed( batchSize, audioSegmentLength, outputLength, outputShape )
model.fit_generator( trainDataFeed, samples_per_epoch = 60000, nb_epoch = 1000, validation_data = testDataFeed, nb_val_samples = 4000, max_q_size = 2, verbose = 1, callbacks = [csv_logger, checkpoint_logger] )
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
