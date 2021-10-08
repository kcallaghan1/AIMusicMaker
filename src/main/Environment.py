from mido import Message, MetaMessage, MidiFile, MidiTrack
import os
import re

def output_to_midi(mid):
    print("Enter a name for the output file:")
    name = input()

    mid.save("midi/" + name + ".mid")