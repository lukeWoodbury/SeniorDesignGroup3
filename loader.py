import csv
import numpy as np
from scipy.io.wavfile import read
#from pip.req.req_file import process_line

textCategories = { "natural language": set(),
                   "country": set(),
                   "english residence": set(),
                   "learning style": set() }
outputKey = { "male": 0,
              "female": 1,
              "age": 2,
              "onset age": 3,
              "LOR": 4 }
speakerOutputs = []
speakerOrder = []

# create sets for each text category
with open("speakers.csv", 'rb') as csvFile:
    speakers = csv.DictReader(csvFile)
    for speaker in speakers:
        for category in textCategories:
            textCategories[category].add(speaker[category])
    
# finish filling outputKey
i = len(outputKey)
for category in textCategories:
    print category
    for label in textCategories[category]:
        outputKey[category + " - " + label] = i;
        i += 1

print( len( outputKey ) )
for category in textCategories:
    print category
    print len( textCategories[category] )
    
# fill speakerOutputs and speakerOrder
maleCount = 0
with open("speakers.csv", 'rb') as csvFile:
    speakers = csv.DictReader(csvFile)
    n = len(outputKey)
    for speaker in speakers:
        speakerOutput = [0] * n
        if speaker["gender"] == "male":
            speakerOutput[outputKey["male"]] = 1
            speakerOutput[outputKey['female']] = 0
            maleCount += 1
        else:
            speakerOutput[outputKey["male"]] = 0
            speakerOutput[outputKey['female']] = 1
        speakerOutput[outputKey["age"]] = float(speaker["age"]) / 100.0
        speakerOutput[outputKey["onset age"]] = float(speaker["onset age"]) / 100.0
        speakerOutput[outputKey["LOR"]] = float(speaker["LOR"]) / 100.0
        for category in textCategories:
            speakerOutput[outputKey[category + " - " + speaker[category]]] = 1
        speakerOutputs.append(speakerOutput)
        speakerOrder.append(speaker["natural language"] + speaker["NL #"])
print maleCount

# write speakerOutputs to csv
with open('outputs.csv', 'wb') as outputs:
    wr = csv.writer(outputs)
    wr.writerows(speakerOutputs)

# write speakerOrder to text file
with open('order.csv', 'wb') as order:
    wr = csv.writer(order)
    wr.writerow(speakerOrder)
    
# load audio
'''max_audio_length = 90 * 44100
rootdir = '/home/jacob/Speakers/processed wav files/'
with open( 'audioData.csv', 'wb' ) as audioData:
    wr = csv.writer( audioData )
    for speaker in speakerOrder:
        wav = read( rootdir + speaker + ".wav" )
        wavData = np.array( wav[1], dtype = float )
        wr.writerow( wavData )'''
    