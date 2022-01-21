
from music21 import *
import os
import pandas as pd

os.chdir(r'C:\Users\Alice\Documents\Other Data Viz\PianoNotes')
os.getcwd()

sciPitchRange = ["A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7", "C8"]

colnames = ['Note_w_octave', 'Count']

def noteToKey(note):
    """
    Function to convert scientific pitch notation to piano key number.
    This is needed to plot the pitches in the correct location.
    Code adapated from here: https://thejordancarroll.medium.com/solving-the-pitch-label-problems-6d829aea0d78

    Input:
    Str: scientific pitch name of the note

    Output:
    Int: piano key number corresponding to the pitch, from 1 to 88
    """
    if('-' in note):
       shiftedNote = note.replace('-', '')
       return sciPitchRange.index(shiftedNote)
    else:
       return sciPitchRange.index(note) + 1

def countPitches(score):
    """
    Function to count the number of times each pitch occurs in a given musical score.

    Input:
    score: a parsed MusicXML file (.mxl or .xml)

    Output:
    df: a dataframe with four columns (note name in scientific pitch notation, frequency, pitch, octave)
    """
    #score.plot('histogram', 'pitch')
    nameOctaveCount = analysis.pitchAnalysis.pitchAttributeCount(score, 'nameWithOctave')
    nameOctaveCount_list = [[i, nameOctaveCount[i]] for i in nameOctaveCount]
    nameOctaveCount_df = pd.DataFrame(nameOctaveCount_list, columns=colnames)
    nameOctaveCount_df['Pitch'] = nameOctaveCount_df['Note_w_octave'].str.extract(r'([A-G][\#\-]*)')
    nameOctaveCount_df['Octave'] = nameOctaveCount_df['Note_w_octave'].str.extract(r'(\d)')
    return nameOctaveCount_df

def makeDataframe(score):
    """
    Function to generate a dataframe with pitch frequency and other metadata.

    Input:
    score: a parsed MusicXML file (.mxl or .xml)

    Output:
    df: a dataframe with pitch frequency information, the title of the piece, the composer, the
        key signature, and a conversion from scientific pitch notation to piano key number
    """
    title = score.metadata.title
    composer = score.metadata.composer
    keySignature = score.analyze('key').name
    print(score.metadata.all())
    
    df = countPitches(score)
    df['Title'] = title
    df['Composer'] = composer
    df['Key_signature'] = keySignature
    df['Piano_key_num'] = df['Note_w_octave'].apply(noteToKey)

    return df

fur_elise = converter.parse(r'.\scores\Fur_Elise.mxl')
#bday.show()
df = makeDataframe(fur_elise)

print(df)

