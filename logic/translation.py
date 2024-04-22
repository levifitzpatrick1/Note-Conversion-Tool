from enum import Enum
import tkinter as tk
from tkinter import filedialog


def select_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select Input File",
                                           filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_path


class GuitarType(Enum):
    GUITAR = 1
    BASS = 2


def generate_note(guitar_type: GuitarType, string_number: int, fret: int,
                  capo: int = 0) -> list:
    if guitar_type == GuitarType.GUITAR and (string_number < 1 or string_number > 6):
        raise ValueError("String number for GUITAR must be between 1 and 6")

    if guitar_type == GuitarType.BASS and (string_number < 1 or string_number > 4):
        raise ValueError("String number for BASS must be between 1 and 4")

    if fret < 0 or fret > 24:
        raise ValueError("Frequency must be between 0 and 24")

    #         0    1     2    3     4    5    6     7    8     9    10    11
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    string_offsets = {
        GuitarType.GUITAR: [[4, 9, 2, 7, 11, 4], [12, 7, 2, 9, 5, 12]],  # EADGBE
        GuitarType.BASS: [[4, 9, 2, 7], [12, 7, 2, 9]],  # EADG
    }

    if guitar_type not in string_offsets:
        raise ValueError("Guitar type must be either GUITAR or BASS")

    root_note_index = string_offsets[guitar_type][0][string_number - 1]

    fretted_note_index = (root_note_index + fret + capo) % 12

    note_name = notes[fretted_note_index]

    octave = 0
    if guitar_type == GuitarType.GUITAR:
        if string_number < 4:
            root_octave = 0
        elif string_number < 6:
            root_octave = 1
        else:
            root_octave = 2

    else:
        if string_number < 4:
            root_octave = 0
        else:
            root_octave = 1

    if string_offsets[guitar_type][0][string_number - 1] < fret:
        octave = root_octave + (2 if (fret - string_offsets[guitar_type][0][string_number - 1]) >= 12 else 1)
    else:
        octave = root_octave

    return [note_name, octave]


def get_note_position(note: str, octave: int, target_instrument: GuitarType) -> list:
    if target_instrument == GuitarType.GUITAR:
        num_strings = 6
    else:
        num_strings = 4

    alternative_notes = []

    for string_number in range(1, num_strings + 1):
        for fret in range(25):
            gen_note, gen_octave = generate_note(target_instrument, string_number, fret)
            if gen_note == note and gen_octave == octave:
                alternative_notes.append([gen_note, gen_octave, string_number, fret])

    return alternative_notes


def process_file(input_file: str, input_guitar_type: GuitarType, export_guitar_type: GuitarType) -> list:
    with open(input_file, "r") as file:
        lines = file.readlines()

    note_list = []

    for line in lines:
        string_number, fret = map(int, line.strip().split(','))
        note, octave = generate_note(input_guitar_type, string_number, fret, capo=3)
        note_list.append([note, octave])

    output = []
    prev_index = None
    prev_fret = None

    for index, note in enumerate(note_list):
        new_notes = get_note_position(note[0], note[1], export_guitar_type)
        for new_note in new_notes:
            output.append([index + 1, new_note])

    return output


final = process_file(select_file(), GuitarType.GUITAR, GuitarType.BASS)

for item in final:
    print(item)