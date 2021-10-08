from mido import Message, MetaMessage, MidiFile, MidiTrack
import random

def create_progression(progression, key):

    chords = []

    tonic = 0

    # Set the tonic to the desired note
    if(key == "e" or key == "fb"):
        tonic = 52
    elif(key == "e#" or key == "f"):
        tonic = 53
    elif(key == "f#" or key == "gb"):
        tonic = 54
    elif(key == "g"):
        tonic = 55
    elif(key == "g#" or key == "ab"):
        tonic = 56
    elif(key == "a"):
        tonic = 57
    elif(key == "a#" or key == "bb"):
        tonic = 58
    elif(key == "b" or key == "cb"):
        tonic = 59
    elif(key == "c" or key == "b#"):
        tonic = 60
    elif(key == "c#" or key == "db"):
        tonic = 61
    elif(key == "d"):
        tonic = 62
    elif(key == "d#" or key == "eb"):
        tonic = 63

    chord_progression = [] # holds the MIDI information for the chord progression
    
    # Reads through the Roman Numerals and turns it into usable MIDI data 
    for chord in progression:

        root = 0
        third = 0
        fifth = 7

        if(chord == "I" or chord == "i"):
            root = tonic
        elif(chord == "ii"):
            root = tonic + 2
        elif(chord == "iii"):
            root = tonic + 4
        elif(chord == "IV"):
            root = tonic + 5
        elif(chord == "V"):
            root = tonic - 5
        elif(chord == "VI"):
            root = tonic - 4
        elif(chord == "vi"):
            root = tonic - 3
        elif(chord == "bVII"):
            root = tonic - 2
            

        if(chord.islower()): # If the chord is lowercase, use a minor third
            third = root + 3
        else:
            third = root + 4 # major third otherwise

        fifth = root + 7

        chord_progression.append((root, third, fifth))

    return chord_progression


# Generates a random melody based on the chord progression
def create_melody(chord_progression, loops):

    # Melodies are stored as tuples, such as (note, beats).
    # Beat values can be 4, 3, 2, 1, or 0.5
    melody = []    

    for i in range(loops):
        for chord in chord_progression:
            beats_remaining = 4
            potential_values = [4, 3, 2, 1, 0.5]
            while (beats_remaining > 0):
                value = random.choice(potential_values)
                if(beats_remaining - value >= 0):
                    note = random.choice(chord) + 12 # Melody is an octave above the harmony
                    beats_remaining = beats_remaining - value
                    melody.append((note, value))
    return melody


# Combines the chord progression with the melody
def create_song(progression, melody, loops):
    mid = MidiFile()
    
    # Holds song's meta information
    track0 = MidiTrack()
    mid.tracks.append(track0)
    track0.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    track0.append(MetaMessage('set_tempo', tempo = 833333, time=0))
    track0.append(MetaMessage('end_of_track', time=0))

    # Holds song's harmony
    track1 = MidiTrack()
    mid.tracks.append(track1)
    track1.append(MetaMessage('track_name', name='Harmony', time=0))
    track1.append(Message('program_change', channel=0, program=80, time=0))
    for i in range(loops):
        for chord in progression:
            track1.append(Message('note_on', channel=0, note=chord[0], velocity = 50, time=0))
            track1.append(Message('note_on', channel=0, note=chord[1], velocity = 50, time=0))
            track1.append(Message('note_on', channel=0, note=chord[2], velocity = 50, time=0))
            track1.append(Message('note_off', channel=0, note=chord[0], velocity = 50, time=768))
            track1.append(Message('note_off', channel=0, note=chord[1], velocity = 50, time=0))
            track1.append(Message('note_off', channel=0, note=chord[2], velocity = 50, time=0))
    
    track1.append(MetaMessage('end_of_track', time=0))

    # Holds song's melody 
    track2 = MidiTrack()
    mid.tracks.append(track2)
    track2.append(MetaMessage('track_name', name='Melody', time=0))
    track2.append(Message('program_change', channel=0, program=80, time=0))
    for pair in melody:
        note = pair[0]
        value = 768 # arbitrary value
        if(pair[1] == 4):
            value = 768
        elif(pair[1] == 3):
            value = 576 # 3/4 of 768
        elif(pair[1] == 2):
            value = 384
        elif(pair[1] == 1):
            value = 192
        else:
            value = 96

        track2.append(Message('note_on', channel=0, note=note, velocity = 50, time=0))
        track2.append(Message('note_off', channel=0, note=note, velocity = 50, time=int(value)))
    
    track2.append(MetaMessage('end_of_track', time=0))

    return mid


def random_chord_progression(measures):

    progression = []

    # These lists hold possible values that could follow a certain Roman Numeral
    from1 = ["I", "ii", "iii", "IV", "V", "vi"]
    from2 = ["V"]
    from3 = ["IV", "vi"]
    from4 = ["I", "ii", "V"]
    from5 = ["I", "iii", "vi"]
    from6 = ["ii", "IV"]

    # Choose a random chord to start at
    chord = random.choice(from1)

    for i in range(measures):
        if(chord == "I"):
            progression.append("I")
            chord = random.choice(from1)
        elif(chord == "ii"):
            progression.append("ii")
            chord = random.choice(from2)
        elif(chord == "iii"):
            progression.append("iii")
            chord = random.choice(from3)
        elif(chord == "IV"):
            progression.append("IV")
            chord = random.choice(from4)
        elif(chord == "V"):
            progression.append("V")
            chord = random.choice(from5)
        elif(chord == "vi"):
            progression.append("vi")
            chord = random.choice(from6)
            
    return progression