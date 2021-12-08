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
        elif(chord == "ii" or chord == "iidim"):
            root = tonic + 2
        elif(chord == "III"):
            root = tonic + 3
        elif(chord == "iii"):
            root = tonic + 4
        elif(chord == "IV" or chord == "iv"):
            root = tonic + 5
        elif(chord == "V" or chord == "v"):
            root = tonic - 5
        elif(chord == "VI"):
            root = tonic - 4
        elif(chord == "vi"):
            root = tonic - 3
        elif(chord == "bVII"):
            root = tonic - 2
        elif(chord == "viidim"):
            root = tonic - 1
            

        if(chord == "iidim" or chord == "viidim"): # Rare instance in which diminished chord is used
            third = root + 3
            fifth = root + 6
        elif(chord.islower()): # If the chord is lowercase, use a minor third
            third = root + 3
            fifth = root + 7
        else:
            third = root + 4 # major third otherwise
            fifth = root + 7

        chord_progression.append((root, third, fifth))

    return chord_progression


# Determines the scale to use based on user-defined parameters
def generate_scale(key, is_major):

    scale = []

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

    
    if(is_major == 0): # minor key
        scale.append(tonic)
        scale.append(tonic + 2)
        scale.append(tonic + 3)
        scale.append(tonic + 5)
        scale.append(tonic + 7)
        scale.append(tonic + 8)
        scale.append(tonic + 10)
    else: # major key
        scale.append(tonic)
        scale.append(tonic + 2)
        scale.append(tonic + 4)
        scale.append(tonic + 5)
        scale.append(tonic + 7)
        scale.append(tonic + 9)
        scale.append(tonic + 11)

    return scale


# Creates 'hook' - or basic melody that can be repeated and modified throughout.
def create_hook(chord_progression, scale):

    hook = []
    OCTAVE = 12

    for chord in chord_progression:
            beats_remaining = 4
            potential_values = [4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5]
            note = 0
            while (beats_remaining > 0):
                value = random.choice(potential_values)
                if(beats_remaining - value >= 0):
                    if(len(hook) < 2): # If the melody has just began or the underlying chord is a dominant major 5th
                        note = random.choice(chord) + OCTAVE
                    elif(scale[0] + 10 == scale[6] and (hook[-1][0] == scale[6] + 1 + OCTAVE or hook[-1][0] == scale[6] + 1)): # Handles leading tone in minor key
                        note = hook[-1][0] + 1
                    elif(scale[0] + 11 == scale[6] and (hook[-1][0] == scale[6] + OCTAVE or hook[-1][0] == scale[6])): # Handles leading tone in major key
                        note = hook[-1][0] + 1
                    else:
                        if(hook[-2][0] - hook[-1][0] <= -4): # If there is a leap upwards
                            if((((hook[-1][0] - 1 - OCTAVE) in scale) or (hook[-1][0] - 1) in scale) or (((hook[-1][0] - 1 - OCTAVE) in chord) or (hook[-1][0] - 1) in chord)):
                                note = hook[-1][0] - 1
                            else:
                                note = hook[-1][0] - 2
                        elif(hook[-2][0] - hook[-1][0] >= 4): # If there is a leap downwards
                            if((((hook[-1][0] + 1 - OCTAVE) in scale) or (hook[-1][0] + 1) in scale) or (((hook[-1][0] + 1 - OCTAVE) in chord) or (hook[-1][0] + 1) in chord)):
                                note = hook[-1][0] + 1
                            else:
                                note = hook[-1][0] + 2
                        else:
                            note = random.choice(chord) + OCTAVE
                    beats_remaining = beats_remaining - value
                    hook.append((note, value))
    return hook


# Adds the created hook to the melody
def add_hook_to_melody(melody, hook):
    for hook_element in hook:
        melody.append(hook_element)



# Generates a random melody based on the chord progression
def create_melody(chord_progression, scale, loops):

    # Melodies are stored as tuples, such as (note, beats).
    # Beat values can be 4, 3, 2, 1, or 0.5
    melody = []

    OCTAVE = 12 # All melodic information is 12 semitones (one octave) above the harmony

    hook = create_hook(chord_progression, scale)

    add_hook_to_melody(melody, hook)
    if(loops > 4):
        add_hook_to_melody(melody, hook)  

    loops_completed = 2
    while(loops_completed < loops - 2):
        for chord in chord_progression:
            beats_remaining = 4
            potential_values = [4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5]
            note = 0
            while (beats_remaining > 0):
                value = random.choice(potential_values)
                if(beats_remaining - value >= 0):
                    if(len(melody) < 2 or (chord[0] == scale[4] and chord[1] == scale[4] + 4)): # If the melody has just began or the underlying chord is a dominant major 5th
                        note = random.choice(chord) + OCTAVE
                    elif(scale[0] + 10 == scale[6] and (melody[-1][0] == scale[6] + 1 + OCTAVE or melody[-1][0] == scale[6] + 1)): # Handles leading tone in minor key
                        note = melody[-1][0] + 1
                    elif(scale[0] + 11 == scale[6] and (melody[-1][0] == scale[6] + OCTAVE or melody[-1][0] == scale[6])): # Handles leading tone in major key
                        note = melody[-1][0] + 1
                    else:
                        if(melody[-2][0] - melody[-1][0] <= -4): # If there is a leap upwards
                            if((((melody[-1][0] - 1 - OCTAVE) in scale) or (melody[-1][0] - 1 in scale)) or (((melody[-1][0] - 1 - OCTAVE) in chord) or (melody[-1][0] - 1 in chord))):
                                note = melody[-1][0] - 1
                            else:
                                note = melody[-1][0] - 2
                        elif(melody[-2][0] - melody[-1][0] >= 4): # If there is a leap downwards
                            if(((melody[-1][0] + 1 - OCTAVE) in scale) or (melody[-1][0] + 1 in scale)):
                                note = melody[-1][0] + 1
                            else:
                                note = melody[-1][0] + 2
                        else:
                            note = random.choice(chord) + OCTAVE
                    beats_remaining = beats_remaining - value
                    melody.append((note, value))
        loops_completed = loops_completed + 1
    add_hook_to_melody(melody, hook)
    if(loops > 4):
        add_hook_to_melody(melody, hook)                                                      
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
            value = value
        elif(pair[1] == 3.5):
            value = int(value * (7/8))
        elif(pair[1] == 3):
            value = int(value * (3/4))
        elif(pair[1] == 2.5):
            value = int(value * (5/8))
        elif(pair[1] == 2):
            value = int(value / 2)
        elif(pair[1] == 1.5):
            value = int(value * (3/8))
        elif(pair[1] == 1):
            value = int(value / 4)
        else:
            value = int(value / 8)

        track2.append(Message('note_on', channel=0, note=note, velocity = 50, time=0))
        track2.append(Message('note_off', channel=0, note=note, velocity = 50, time=int(value)))
    
    track2.append(MetaMessage('end_of_track', time=0))

    return mid


def random_chord_progression(measures, is_major):

    progression = []

    if(is_major == 0):
        # These lists hold possible values that could follow a certain Roman Numeral
        from1 = ["iidim", "III", "iv", "v", "V", "VI", "bVII"]
        from2 = ["i", "III"]
        from3 = ["i", "iv", "VI"]
        from4 = ["i", "v", "V"]
        from5 = ["i", "V", "VI"]
        from6 = ["i", "III", "v", "V", "bVII"]
        from7 = ["i", "v", "VI"]
        from5_2 = ["i"] # Used in rare instances

        # Choose a random chord to start at
        chord = "i"

        for i in range(measures):
            if(chord == "i"):
                progression.append("i")
                chord = random.choice(from1)
            elif(chord == "iidim"):
                progression.append("iidim")
                chord = random.choice(from2)
            elif(chord == "III"):
                progression.append("III")
                chord = random.choice(from3)
            elif(chord == "iv"):
                progression.append("iv")
                chord = random.choice(from4)
            elif(chord == "v"):
                progression.append("v")
                chord = random.choice(from5)
            elif(chord == "V"):
                progression.append("V")
                chord = random.choice(from5_2)
            elif(chord == "VI"):
                progression.append("VI")
                chord = random.choice(from6)
            elif(chord == "bVII"):
                progression.append("bVII")
                chord = random.choice(from7)
            elif(chord == "viidim"):
                progression.append("viidim")
                chord = random.choice(from7)
    else:
        # These lists hold possible values that could follow a certain Roman Numeral
        from1 = ["ii", "iii", "IV", "V", "vi", "VII", "viidim"]
        from2 = ["V"]
        from3 = ["IV", "vi"]
        from4 = ["I", "ii", "V"]
        from5 = ["I", "iii", "vi"]
        from6 = ["ii", "IV"]
        from7 = ["I"]

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
            elif(chord == "bVII"):
                progression.append("bVII")
                chord = random.choice(from7)
            elif(chord == "viidim"):
                progression.append("viidim")
                chord = random.choice(from7)
            
    return progression