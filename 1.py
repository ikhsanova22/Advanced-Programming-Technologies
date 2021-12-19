import os
from music21 import *
import numpy as np

def read_midi(file):
    
    print("Loading Music File:",file)
    
    notes=[]
    notes_to_parse = None
    
    midi = converter.parse(file)
    s2 = instrument.partitionByInstrument(midi)

    for part in s2.parts:
        if 'Piano' in str(part): 
            notes_to_parse = part.recurse() 
      
            for element in notes_to_parse:    
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    return np.array(notes)

path='schubert/'

files=[i for i in os.listdir(path) if i.endswith(".mid")]

notes_array = np.array([read_midi(path+i) for i in files]) 

notes_ = [element for note_ in notes_array for element in note_]

unique_notes = list(set(notes_))
print(len(unique_notes))

from collections import Counter

freq = dict(Counter(notes_))
import matplotlib.pyplot as plt
no=[count for _,count in freq.items()]

plt.figure(figsize=(5,5))
plt.hist(no)


new_music=[]

for notes in notes_array:
    temp=[]
    for note_ in notes:
        if note_ in frequent_notes:
            temp.append(note_)            
    new_music.append(temp)
    
new_music = np.array(new_music)

no_of_timesteps = 32
x = []
y = []

for note_ in new_music:
    for i in range(0, len(note_) - no_of_timesteps, 1):
        
        input_ = note_[i:i + no_of_timesteps]
        output = note_[i + no_of_timesteps]
        
        x.append(input_)
        y.append(output)
        
x=np.array(x)
y=np.array(y)

x_seq=[]
for i in x:
    temp=[]
    for j in i:
        temp.append(x_note_to_int[j])
    x_seq.append(temp)
    
x_seq = np.array(x_seq)

def lstm():
  model = Sequential()
  model.add(LSTM(128,return_sequences=True))
  model.add(LSTM(128))
  model.add(Dense(256))
  model.add(Activation('relu'))
  model.add(Dense(n_vocab))
  model.add(Activation('softmax'))
  model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
  return model