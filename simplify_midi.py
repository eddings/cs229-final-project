from music21 import converter, instrument, note, chord, stream
import glob
import sys
import numpy as np
import os

def simplify_midi():
    """ Write a simplified MIDI file """

    notes = {}
    for file in glob.glob('songs/*.mid'):
        test_file = file.replace('songs/', 'simplified_songs/')
        test_file = test_file.replace('.', '_simple.')
        if not os.path.isfile(test_file):
            notes = get_notes(file)
            create_midi(notes, file)


def get_notes(filename):
    """ Get all the notes and highest note from each cord from the midi files in the ./midi_songs directory """

    midi = converter.parse(filename)
    notes_i = []

    print("Parsing %s" % filename)

    notes_to_parse = None

    try: # file has instrument parts
        notes_to_parse = midi[0].recurse()
    except: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes_i.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes_i.append(str(element.pitches[-1])) # take the note with the highest octave? This is a modification
        
    # trim out the excess to standardize the length of the musical piece
    desired_length = len(notes_i) - (len(notes_i) % 50) # 50 will be our input length

    return notes_i[0:desired_length]
    #return notes

def create_midi(melody, filename):
    """ create a midi file from the notes """

    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in melody:
        # pattern is a note
        try:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

            # increase offset each iteration so that notes do not stack
            offset += 0.5
        except:
            print('Exception thrown, note not appended')

    midi_stream = stream.Stream(output_notes)

    filename = filename.replace('songs/','')
    midi_stream.write('midi', fp='simplified_songs/'+filename[:-4]+'_simple.mid')

if __name__ == '__main__':
    simplify_midi()


