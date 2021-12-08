from Agent import create_progression, create_melody, create_song, generate_scale, random_chord_progression
from Environment import output_to_midi

def main():
    print("-----------------------------------")
    print("Welcome to the AI Music Generator!!")
    print("-----------------------------------")


    print("How would you like to begin? (choose #)")
    print("1. From existing chord progression\n2. Input chord progression\n3. Random chord progression\n4. Quit")
    song_choice = int(input())

    is_major = -1 # Variable determines whether or not progression is in a major or minor key, will have an effect on the scale choice in the melody function

    if(song_choice == 1):
        print("Select a chord progression from the list below:")
        print("1. I-I-IV-V")
        print("2. I-V-vi-IV")
        print("3. ii-V-I-I")
        print("4. I-vi-IV-V")
        print("5. I-bVII-I-bVII")
        print("6. I-I-bVII-bVII")
        print("7. i-bVII-VI-V")
        print("8. i-bVII-VI-bVII")
        print("9. 12 Bar Blues")
        print("10. Canon")
        print("11. Quit")
        progression_choice = int(input())
        progression = []

        if(progression_choice == 1):
            progression = ["I", "I", "IV", "V"]
        elif(progression_choice == 2):
            progression = ["I", "V", "vi", "IV"]
        elif(progression_choice == 3):
            progression = ["ii", "V", "I", "I"]
        elif(progression_choice == 4):
            progression = ["I", "vi", "IV", "V"]
        elif(progression_choice == 5):
            progression = ["I", "bVII", "I", "bVII"]
        elif(progression_choice == 6):
            progression = ["I", "I", "bVII", "bVII"]
        elif(progression_choice == 7):
            progression = ["i", "bVII", "VI", "V"]
        elif(progression_choice == 8):
            progression = ["i", "bVII", "VI", "bVII"]
        elif(progression_choice == 9):
            progression = ["I", "IV", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"]
        elif(progression_choice == 10):
            progression = ["I", "V", "vi", "iii", "IV", "I", "IV", "V"]            
        elif(progression_choice == 11):
            exit()


        # Determines the quality of the scale to use based on the progression
        if(progression_choice < 7 or progression_choice > 8):
            is_major = 1
        elif(progression_choice == 7 or progression_choice == 8):
            is_major = 0



        waiting_for_key = 1
        while(waiting_for_key == 1):
            print("Enter the key (eg. A, C#, etc.,) or 'q' to quit:")
            key_choice = input()
            
            acceptable_keys = ["a", "ab", "a#", "b", "bb", "b#", "c", "cb", "c#", "d", "db", "d#", "e", "eb", "e#", "f", "fb", "f#", "g", "gb", "g#"]

            if(key_choice.lower() in acceptable_keys):
                progression = create_progression(progression, key_choice.lower())
                waiting_for_key = 0
            else:
                print("Key center not recognized, please enter a proper key.")


        print("How many times should the progression be looped?")
        loops = int(input())

        scale = generate_scale(key_choice.lower(), is_major)

        melody = create_melody(progression, scale, loops)

        #print("Enter BPM:")
        #bpm = int(input())

        mid = create_song(progression, melody, loops)

        output_to_midi(mid)

    elif(song_choice == 2):
        progression = []
        print("Enter Roman Numerals for the chord progression, 'X' to finish, or 'Q' to quit.")
        chord = input()
        keepGoing = 1
        while(keepGoing == 1):
            if(chord == "I"):
                is_major = 1
            elif(chord == "i"):
                is_major = 0
            elif(chord.lower() == "q"):
                exit()
            elif(chord.lower() == "x"):
                keepGoing = 0
                break
            else:
                progression.append(chord)
                chord = input()

        print("Enter the key (eg. A, C#, etc.,) or 'q' to quit:")
        key_choice = input()
        
        acceptable_keys = ["a", "ab", "a#", "b", "bb", "b#", "c", "cb", "c#", "d", "db", "d#", "e", "eb", "e#", "f", "fb", "f#", "g", "gb", "g#"]

        if(key_choice.lower() in acceptable_keys):
            progression = create_progression(progression, key_choice.lower())
        else:
            exit()

        print("How many times should the progression be looped?")
        loops = int(input())

        scale = generate_scale(key_choice.lower(), is_major)

        melody = create_melody(progression, scale, loops)

        mid = create_song(progression, melody, loops)

        output_to_midi(mid)


    elif(song_choice == 3):
        print("How many measures for the progression?")
        measures = int(input())

        waiting_for_quality = 1
        while(waiting_for_quality == 1):
            print("Should the progression be in a major or minor key?")
            quality_choice = input()
            
            if(quality_choice == "major"):
                is_major = 1
                waiting_for_quality = 0
            elif(quality_choice == "minor"):
                is_major = 0
                waiting_for_quality = 0
            else:
                print("Quality not recognized, please enter \"major\" or \"minor\"")
        
        progression = random_chord_progression(measures, is_major)
     

        waiting_for_key = 1
        while(waiting_for_key == 1):
            print("Enter the key (eg. A, C#, etc.,) or 'q' to quit:")
            key_choice = input()
            
            acceptable_keys = ["a", "ab", "a#", "b", "bb", "b#", "c", "cb", "c#", "d", "db", "d#", "e", "eb", "e#", "f", "fb", "f#", "g", "gb", "g#"]

            if(key_choice.lower() in acceptable_keys):
                progression = create_progression(progression, key_choice.lower())
                waiting_for_key = 0
            else:
                print("Key center not recognized, please enter a proper key.")

        print("How many times should the progression be looped?")
        loops = int(input())

        scale = generate_scale(key_choice.lower(), is_major)

        melody = create_melody(progression, scale, loops)

        mid = create_song(progression, melody, loops)

        output_to_midi(mid)

    else:
        exit()

        



if __name__ == "__main__":
    main()