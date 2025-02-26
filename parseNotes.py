## Script to calculate pitch frequencies for a given piano score

import music21
from music21 import *
import os
import pandas as pd

os.chdir(r'C:\Users\m3lo4\OneDrive\GitHub\music-visualization')

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
    if(('B#' in note) or ('E#' in note)):
        shiftedNote = note.replace('#', '')
        return sciPitchRange.index(shiftedNote) + 1
    elif(('C-' in note) or ('F-' in note)):
        shiftedNote = note.replace('-', '')
        return sciPitchRange.index(shiftedNote) - 1
    elif('##' in note):
        shiftedNote = note.replace('##', '')
        return sciPitchRange.index(shiftedNote) + 2
    elif('--' in note):
        shiftedNote = note.replace('--', '')
        return sciPitchRange.index(shiftedNote) - 2
    elif('-' in note):
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
    #score.plot('histogram', 'pitch', title = score.metadata.title)
    nameOctaveCount = analysis.pitchAnalysis.pitchAttributeCount(score, 'nameWithOctave')
    nameOctaveCount_list = [[i, nameOctaveCount[i]] for i in nameOctaveCount]

    nameOctaveCount_df = pd.DataFrame(nameOctaveCount_list, columns=colnames)
    nameOctaveCount_df['Pitch'] = nameOctaveCount_df['Note_w_octave'].str.extract(r'([A-G])')
    nameOctaveCount_df['Octave'] = nameOctaveCount_df['Note_w_octave'].str.extract(r'(\d)')
    nameOctaveCount_df['Accidental'] = nameOctaveCount_df['Note_w_octave'].str.extract(r'([\#\-]+)')
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
    movementName = score.metadata.movementName
    composer = score.metadata.composer
    keySignature = score.analyze('key').name
    print(score.metadata.all())
    
    df = countPitches(score)
    if((title == 'Rachmaninoff - Piano Concerto No. 2 in C minor (Op. 18)') | (title == 'Sonata I ') | ('Bach-WTC' in title)):
        df['Title'] = movementName
    else:
        df['Title'] = title
    df['Composer'] = composer
    df['Key_signature'] = keySignature
    df['Piano_key_num'] = df['Note_w_octave'].apply(noteToKey)

    return df

elegy = converter.parse(r'.\music_scores\Elegy I.xml')
elegy_df = makeDataframe(elegy)

marionette = converter.parse(r'.\music_scores\To Give a Marionette Life.xml')
marionette_df = makeDataframe(marionette)

# fur_elise = converter.parse(r'.\scores\Beethoven-Fur_Elise.mxl')
# fur_elise_df = makeDataframe(fur_elise)

# moonlight_sonata = converter.parse(r'.\scores\Beethoven-Moonlight_Sonata.mxl')
# moonlight_sonata_df = makeDataframe(moonlight_sonata)

# moonlight_sonata_1 = converter.parse(r'.\scores\Beethoven-Moonlight_Sonata_1st_Movement.mxl')
# moonlight_sonata_1_df = makeDataframe(moonlight_sonata_1)
# moonlight_sonata_2 = converter.parse(r'.\scores\Beethoven-Moonlight_Sonata_2nd_Movement.mxl')
# moonlight_sonata_2_df = makeDataframe(moonlight_sonata_2)
# moonlight_sonata_3 = converter.parse(r'.\scores\Beethoven-Moonlight_Sonata_3rd_Movement.mxl')
# moonlight_sonata_3_df = makeDataframe(moonlight_sonata_3)

# clair_de_lune = converter.parse(r'.\scores\Debussy-Clair_de_Lune.mxl')
# clair_df = makeDataframe(clair_de_lune)  # the key signature is incorrect - should be D- Major, not C# Major

# chopin_nocturne = converter.parse(r'.\scores\Chopin-Nocturne_Op_9_No_2.mxl')
# nocturne_df = makeDataframe(chopin_nocturne)

# pathetique_1 = converter.parse(r'.\scores\Beethoven_Sonate-Pathetique-1st-Movement.mxl')
# pathetique_1_df = makeDataframe(pathetique_1)
# pathetique_2 = converter.parse(r'.\scores\Beethoven_Sonate-Pathetique-2nd-Movement.mxl')
# pathetique_2_df = makeDataframe(pathetique_2)
# pathetique_3 = converter.parse(r'.\scores\Beethoven_Sonate-Pathetique-3rd-Movement.mxl')
# pathetique_3_df = makeDataframe(pathetique_3)

# campanella = converter.parse(r'.\scores\Liszt_La-Campanella.mxl')
# campanella_df = makeDataframe(campanella)

# rach_1 = converter.parse(r'.\scores\Rachmaninoff_Piano-Concerto-No-2-Op18-1st-Movement.mxl')
# rach_1_df = makeDataframe(rach_1)
# rach_2 = converter.parse(r'.\scores\Rachmaninoff_Piano-Concerto-No-2-Op18-2nd-Movement.mxl')
# rach_2_df = makeDataframe(rach_2)
# rach_3 = converter.parse(r'.\scores\Rachmaninoff_Piano-Concerto-No-2-Op18-3rd-Movement.mxl')
# rach_3_df = makeDataframe(rach_3)

# mozart_1 = converter.parse(r'.\scores\Mozart_Piano-Sonata-No-11-K331-1st-Movement.mxl')
# mozart_1_df = makeDataframe(mozart_1)
# mozart_2 = converter.parse(r'.\scores\Mozart_Piano-Sonata-No-11-K331-2nd-Movement.mxl')
# mozart_2_df = makeDataframe(mozart_2)
# mozart_3 = converter.parse(r'.\scores\Mozart_Piano-Sonata-No-11-K331-3rd-Movement.mxl')
# mozart_3_df = makeDataframe(mozart_3)

# liebestraum = converter.parse(r'.\scores\Liszt_Liebestraum.mxl')
# liebestraum_df = makeDataframe(liebestraum)

# minute_waltz = converter.parse(r'.\scores\Chopin_Minute-Waltz.mxl')
# minute_waltz_df = makeDataframe(minute_waltz)

# gymnopedie = converter.parse(r'.\scores\Satie_Gymnopdie-No-1.mxl')
# gymnopedie_df = makeDataframe(gymnopedie)

# wtc_prelude_c_major = converter.parse(r'.\scores\Bach-WTC_Prelude_C_Major.mxl')
# wtc_prelude_c_major_df = makeDataframe(wtc_prelude_c_major)
# wtc_fugue_c_major = converter.parse(r'.\scores\Bach-WTC_Fugue_C_Major.mxl')
# wtc_fugue_c_major_df = makeDataframe(wtc_fugue_c_major)
# wtc_prelude_c_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_C_Minor.mxl')
# wtc_prelude_c_minor_df = makeDataframe(wtc_prelude_c_minor)
# wtc_fugue_c_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_C_Minor.mxl')
# wtc_fugue_c_minor_df = makeDataframe(wtc_fugue_c_minor)

# wtc_prelude_csharp_major = converter.parse(r'.\scores\Bach-WTC_Prelude_Csharp_Major.mxl')
# wtc_prelude_csharp_major_df = makeDataframe(wtc_prelude_csharp_major)
# wtc_fugue_csharp_major = converter.parse(r'.\scores\Bach-WTC_Fugue_Csharp_Major.mxl')
# wtc_fugue_csharp_major_df = makeDataframe(wtc_fugue_csharp_major)
# wtc_prelude_csharp_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_Csharp_Minor.mxl')
# wtc_prelude_csharp_minor_df = makeDataframe(wtc_prelude_csharp_minor)
# wtc_fugue_csharp_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_Csharp_Minor.mxl')
# wtc_fugue_csharp_minor_df = makeDataframe(wtc_fugue_csharp_minor)

# wtc_prelude_d_major = converter.parse(r'.\scores\Bach-WTC_Prelude_D_Major.mxl')
# wtc_prelude_d_major_df = makeDataframe(wtc_prelude_d_major)
# wtc_fugue_d_major = converter.parse(r'.\scores\Bach-WTC_Fugue_D_Major.mxl')
# wtc_fugue_d_major_df = makeDataframe(wtc_fugue_d_major)
# wtc_prelude_d_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_D_Minor.mxl')
# wtc_prelude_d_minor_df = makeDataframe(wtc_prelude_d_minor)
# wtc_fugue_d_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_D_Minor.mxl')
# wtc_fugue_d_minor_df = makeDataframe(wtc_fugue_d_minor)

# wtc_prelude_eflat_major = converter.parse(r'.\scores\Bach-WTC_Prelude_Eflat_Major.mxl')
# wtc_prelude_eflat_major_df = makeDataframe(wtc_prelude_eflat_major)
# wtc_fugue_eflat_major = converter.parse(r'.\scores\Bach-WTC_Fugue_Eflat_Major.mxl')
# wtc_fugue_eflat_major_df = makeDataframe(wtc_fugue_eflat_major)
# wtc_prelude_eflat_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_Eflat_Minor.mxl')
# wtc_prelude_eflat_minor_df = makeDataframe(wtc_prelude_eflat_minor)
# wtc_fugue_dsharp_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_Dsharp_Minor.mxl')
# wtc_fugue_dsharp_minor_df = makeDataframe(wtc_fugue_dsharp_minor)

# wtc_prelude_e_major = converter.parse(r'.\scores\Bach-WTC_Prelude_E_Major.mxl')
# wtc_prelude_e_major_df = makeDataframe(wtc_prelude_e_major)
# wtc_fugue_e_major = converter.parse(r'.\scores\Bach-WTC_Fugue_E_Major.mxl')
# wtc_fugue_e_major_df = makeDataframe(wtc_fugue_e_major)
# wtc_prelude_e_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_E_Minor.mxl')
# wtc_prelude_e_minor_df = makeDataframe(wtc_prelude_e_minor)
# wtc_fugue_e_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_E_Minor.mxl')
# wtc_fugue_e_minor_df = makeDataframe(wtc_fugue_e_minor)

# wtc_prelude_f_major = converter.parse(r'.\scores\Bach-WTC_Prelude_F_Major.mxl')
# wtc_prelude_f_major_df = makeDataframe(wtc_prelude_f_major)
# wtc_fugue_f_major = converter.parse(r'.\scores\Bach-WTC_Fugue_F_Major.mxl')
# wtc_fugue_f_major_df = makeDataframe(wtc_fugue_f_major)
# wtc_prelude_f_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_F_Minor.mxl')
# wtc_prelude_f_minor_df = makeDataframe(wtc_prelude_f_minor)
# wtc_fugue_f_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_F_Minor.mxl')
# wtc_fugue_f_minor_df = makeDataframe(wtc_fugue_f_minor)

# wtc_prelude_fsharp_major = converter.parse(r'.\scores\Bach-WTC_Prelude_Fsharp_Major.mxl')
# wtc_prelude_fsharp_major_df = makeDataframe(wtc_prelude_fsharp_major)
# wtc_fugue_fsharp_major = converter.parse(r'.\scores\Bach-WTC_Fugue_Fsharp_Major.mxl')
# wtc_fugue_fsharp_major_df = makeDataframe(wtc_fugue_fsharp_major)
# wtc_prelude_fsharp_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_Fsharp_Minor.mxl')
# wtc_prelude_fsharp_minor_df = makeDataframe(wtc_prelude_fsharp_minor)
# wtc_fugue_fsharp_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_Fsharp_Minor.mxl')
# wtc_fugue_fsharp_minor_df = makeDataframe(wtc_fugue_fsharp_minor)

# wtc_prelude_g_major = converter.parse(r'.\scores\Bach-WTC_Prelude_G_Major.mxl')
# wtc_prelude_g_major_df = makeDataframe(wtc_prelude_g_major)
# wtc_fugue_g_major = converter.parse(r'.\scores\Bach-WTC_Fugue_G_Major.mxl')
# wtc_fugue_g_major_df = makeDataframe(wtc_fugue_g_major)
# wtc_prelude_g_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_G_Minor.mxl')
# wtc_prelude_g_minor_df = makeDataframe(wtc_prelude_g_minor)
# wtc_fugue_g_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_G_Minor.mxl')
# wtc_fugue_g_minor_df = makeDataframe(wtc_fugue_g_minor)

# wtc_prelude_aflat_major = converter.parse(r'.\scores\Bach-WTC_Prelude_Aflat_Major.mxl')
# wtc_prelude_aflat_major_df = makeDataframe(wtc_prelude_aflat_major)
# wtc_fugue_aflat_major = converter.parse(r'.\scores\Bach-WTC_Fugue_Aflat_Major.mxl')
# wtc_fugue_aflat_major_df = makeDataframe(wtc_fugue_aflat_major)
# wtc_prelude_gsharp_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_Gsharp_Minor.mxl')
# wtc_prelude_gsharp_minor_df = makeDataframe(wtc_prelude_gsharp_minor)
# wtc_fugue_gsharp_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_Gsharp_Minor.mxl')
# wtc_fugue_gsharp_minor_df = makeDataframe(wtc_fugue_gsharp_minor)

# wtc_prelude_a_major = converter.parse(r'.\scores\Bach-WTC_Prelude_A_Major.mxl')
# wtc_prelude_a_major_df = makeDataframe(wtc_prelude_a_major)
# wtc_fugue_a_major = converter.parse(r'.\scores\Bach-WTC_Fugue_A_Major.mxl')
# wtc_fugue_a_major_df = makeDataframe(wtc_fugue_a_major)
# wtc_prelude_a_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_A_Minor.mxl')
# wtc_prelude_a_minor_df = makeDataframe(wtc_prelude_a_minor)
# wtc_fugue_a_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_A_Minor.mxl')
# wtc_fugue_a_minor_df = makeDataframe(wtc_fugue_a_minor)

# wtc_prelude_bflat_major = converter.parse(r'.\scores\Bach-WTC_Prelude_Bflat_Major.mxl')
# wtc_prelude_bflat_major_df = makeDataframe(wtc_prelude_bflat_major)
# wtc_fugue_bflat_major = converter.parse(r'.\scores\Bach-WTC_Fugue_Bflat_Major.mxl')
# wtc_fugue_bflat_major_df = makeDataframe(wtc_fugue_bflat_major)
# wtc_prelude_bflat_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_Bflat_Minor.mxl')
# wtc_prelude_bflat_minor_df = makeDataframe(wtc_prelude_bflat_minor)
# wtc_fugue_bflat_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_Bflat_Minor.mxl')
# wtc_fugue_bflat_minor_df = makeDataframe(wtc_fugue_bflat_minor)

# wtc_prelude_b_major = converter.parse(r'.\scores\Bach-WTC_Prelude_B_Major.mxl')
# wtc_prelude_b_major_df = makeDataframe(wtc_prelude_b_major)
# wtc_fugue_b_major = converter.parse(r'.\scores\Bach-WTC_Fugue_B_Major.mxl')
# wtc_fugue_b_major_df = makeDataframe(wtc_fugue_b_major)
# wtc_prelude_b_minor = converter.parse(r'.\scores\Bach-WTC_Prelude_B_Minor.mxl')
# wtc_prelude_b_minor_df = makeDataframe(wtc_prelude_b_minor)
# wtc_fugue_b_minor = converter.parse(r'.\scores\Bach-WTC_Fugue_B_Minor.mxl')
# wtc_fugue_b_minor_df = makeDataframe(wtc_fugue_b_minor)

df = pd.concat([elegy_df, marionette_df])

# sort dataframe so that keys that are pressed the most are at the
# bottom of the plot layers
df.sort_values(by=['Composer', 'Title', 'Count'],
               ascending=[True, True, False],
               inplace=True)

df.to_csv("note_counts.csv", index = False)

