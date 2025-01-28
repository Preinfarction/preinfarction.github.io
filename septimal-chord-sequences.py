import random
import re
import math
from scamp import *
from fractions import Fraction

# TODO: fit a chromatic scale to the current chord. Perhaps require that the tonic of the next chord is found in the current chromatic scale.

def is_chord_a_fluent_departure_from_initial_chord(chord, initial_chord):
	fluent_motions = [P1, Sbm2, m2, M2, AcM2, SpM2, Sbm3, m3, M3, SpM3, P4, P5, Sbm6, m6, M6, SpM6, Sbm7, m7, M7, SpM7, P8]
	for i, tone in enumerate(chord):
		if tone - initial_chord[i] not in fluent_motions:
			if P1 - (tone - initial_chord[i]) not in fluent_motions:
				return False
	return True

def frequency_ratio_to_midi_number(frequency_ratio):
	fr_cents = 1200 * math.log2(frequency_ratio)
	midi_number = (fr_cents / 100) + 57 - 12
	return midi_number

def play_bass(bass_voice, midi_numbers):
	bass_voice.play_chord(midi_numbers, 1, 2)

def play_chord(voice, bass_voice, chord):
	midi_numbers = [frequency_ratio_to_midi_number(tone.frequency_ratio) for tone in chord]
	bass_notes = midi_numbers[:2]
	upper_chord_tones = midi_numbers[2::]
	s.fork(play_bass, args=[bass_voice, bass_notes])
	wait(1)
	voice.play_chord(upper_chord_tones, 1, 1)

def cyclic_permute_and_reduce_chord(chord):
	permuted_chord = chord[1:] + [chord[0] + P8]
	reduced_chord = [i - permuted_chord[0] for i in permuted_chord]
	return reduced_chord

def are_chords_equal(chord1, chord2):
	if len(chord1) != len(chord2):
		return False
	for i in range(len(chord1)):
		if chord1[i] != chord2[i]:
			return False
	return True

def name_chord(chord):
	tonic_reduced_chord = [tone - chord[0] for tone in chord]
	octave_reduced_chord = []
	for i in tonic_reduced_chord:
		if i.frequency_ratio < P8.frequency_ratio and i not in octave_reduced_chord:
			octave_reduced_chord.append(i)
		else:
			while i.frequency_ratio >= P8.frequency_ratio:
				i -= P8
			if i not in octave_reduced_chord:
				octave_reduced_chord.append(i)
	octave_reduced_chord = sorted(octave_reduced_chord, key=lambda x: x.frequency_ratio)
	octave_reduced_chord_copy = [i for i in octave_reduced_chord]
	for i in range(len(octave_reduced_chord)):
		octave_reduced_chord = cyclic_permute_and_reduce_chord(octave_reduced_chord)
		for chord_quality, possible_chord in chord_space.items():
			if are_chords_equal(possible_chord, octave_reduced_chord):
				tonic = octave_reduced_chord_copy[(i + 1) % len(octave_reduced_chord)] + chord[0]
				return tonic.pitch_class + "." + chord_quality

class Interval:
	def coordinate_difference(self, i1, i2):
		return tuple(i1[x] - i2[x] for x in range(len(i1)))
	
	def coordinate_sum(self, i1, i2):
		return tuple(i1[x] + i2[x] for x in range(len(i1)))
	
	def find_pitch_and_pitch_class(self, coords):
		a, b, c, d = coords
		coords_to_natural_pitch_class = {
			(0, 0, 0, 0): "C",
			(0, 2, 1, 0): "D",
			(1, 4, 2, 0): "E",
			(1, 5, 3, 0): "F",
			(2, 7, 4, 0): "G",
			(2, 9, 5, 0): "A",
			(3, 11, 6, 0): "B",
		}
		P8 = (3, 12, 7, 0)
		octave_counter = 2
		while coords[2] < 0:
			coords = self.coordinate_sum(coords, (3, 12, 7, 0))
			octave_counter -= 1
		while coords[2] > 6:
			coords = self.coordinate_difference(coords, (3, 12, 7, 0))
			octave_counter += 1
		if coords in coords_to_natural_pitch_class:
			pitch_class = coords_to_natural_pitch_class[coords]
			pitch = pitch_class + str(octave_counter)
			return  (pitch, pitch_class)
		pitch_letter = "CDEFGAB"[coords[2]]
		d2_to_natural_interval_coords = {
			0: (0, 0, 0, 0), # P1
			1: (0, 2, 1, 0), # M2
			2: (1, 4, 2, 0), # M3
			3: (1, 5, 3, 0), # P4
			4: (2, 7, 4, 0), # P5
			5: (2, 9, 5, 0), # M6
			6: (3, 11, 6, 0), # M7
		}
		natural_interval = d2_to_natural_interval_coords[coords[2]]
		accidental_string = ""
		acuteness_difference = coords[1] - natural_interval[1]
		septimal_difference = coords[3]
		if acuteness_difference > 0:
			accidental_string += "#" * acuteness_difference
		if acuteness_difference < 0:
			accidental_string += "b" * abs(acuteness_difference)
		gravity_difference = coords[0] - natural_interval[0]
		if gravity_difference > 0:
			accidental_string += "+" * gravity_difference
		if gravity_difference < 0:
			accidental_string += "-" * abs(gravity_difference)
		if septimal_difference > 0:
			accidental_string += u"\u2077" * septimal_difference
		if septimal_difference < 0:
			accidental_string += u"\u2087" * abs(septimal_difference)
		pitch_class = pitch_letter + accidental_string
		pitch = pitch_class + str(octave_counter)
		return (pitch, pitch_class)
	
	def pprint(self, interval_string):
		interval_string = re.sub(r"dP", r"d", interval_string)
		interval_string = re.sub(r"AP", r"A", interval_string)
		interval_string = re.sub(r"SbP", r"Sb", interval_string)
		interval_string = re.sub(r"SpP", r"Sp", interval_string)
		interval_string = re.sub(r"GrP", r"Gr", interval_string)
		interval_string = re.sub(r"AcP", r"Ac", interval_string)
		interval_string = re.sub(r"dm", r"d", interval_string)
		interval_string = re.sub(r"AM", r"A", interval_string)
		return interval_string
	
	def interval_to_quality(self, coords):
		interval = coords
		a, b, c, d = interval
		if c >= 7:
			return self.interval_to_quality(self.coordinate_difference((a, b, c, d), (3, 12, 7, 0)))
		if c < 0:
			return self.interval_to_quality(self.coordinate_sum((a, b, c, d), (3, 12, 7, 0)))
		base_interval_to_quality = {
			(0, 0, 0, 0): "P",
			(0, 1, 1, 0): "m",
			(0, 2, 1, 0): "M",
			(1, 3, 2, 0): "m",
			(1, 4, 2, 0): "M",
			(1, 5, 3, 0): "P",
			(2, 7, 4, 0): "P",
			(2, 8, 5, 0): "m",
			(2, 9, 5, 0): "M",
			(3, 10, 6, 0): "m",
			(3, 11, 6, 0): "M",
		}
		c_to_natural_gravity = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3}
		if interval in base_interval_to_quality:
			return base_interval_to_quality[interval]
		if d < 0:
			return "Sb" + self.interval_to_quality((a, b, c, d + 1))
		if d > 0:
			return "Sp" + self.interval_to_quality((a, b, c, d - 1))
		natural_gravity = c_to_natural_gravity[c]
		gravity_difference = a - natural_gravity
		if gravity_difference < 0:
			return "Gr" * abs(gravity_difference) + self.interval_to_quality((a - gravity_difference, b, c, d))
		if gravity_difference > 0:
			return "Ac" * gravity_difference + self.interval_to_quality((a - gravity_difference, b, c, d))
		if c == 0:
			if b < 0:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 0:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 1:
			if b < 1:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 2:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 2:
			if b < 3:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 4:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 3:
			if b < 5:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 5:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 4:
			if b < 7:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 7:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 5:
			if b < 8:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 9:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
		if c == 6:
			if b < 10:
				return "d" + self.interval_to_quality((a, b + 1, c, d))
			if b > 11:
				return "A" + self.interval_to_quality((a, b - 1, c, d))
	
	def get_interval_name(self):
		(a, b, c, d) = self.coords
		self.ordinal = self.coords[2] + 1
		self.quality = self.pprint(self.interval_to_quality(self.coords))
		name = self.quality + str(self.ordinal)
		return name
	
	def __init__(self, coords):
		self.coords = coords
		self.name = self.get_interval_name()
		self.frequency_ratio = self.get_frequency_ratio()
		self.pitch, self.pitch_class = self.find_pitch_and_pitch_class(self.coords)
	def __add__(self, other):
		new_coords = tuple(self.coords[x] + other.coords[x] for x in range(len(self.coords)))
		return Interval(new_coords)
	def __sub__(self, other):
		new_coords = tuple(self.coords[x] - other.coords[x] for x in range(len(self.coords)))
		return Interval(new_coords)
	def __mul__(self, scalar):
		new_coords = tuple(self.coords[x] * scalar for x in range(len(self.coords)))
		return Interval(new_coords)
	def __eq__(self, other):
		return self.coords == other.coords
	def get_frequency_ratio(self):
		a, b, c, d = self.coords
		fr = Fraction(81, 80) ** a * Fraction(25, 24) ** b * Fraction(128, 125) ** c * Fraction(36, 35) ** d
		return fr

def is_chord_sorted(chord):
	for i, tone1 in enumerate(chord):
		if i < len(chord) - 1:
			tone2 = chord[i + 1]
			if tone2.frequency_ratio <= tone1.frequency_ratio:
				return False
	return True

def add_chord(previous_chord, initial_chord):
	consonant_steps = [P1, Sp1, Sbm2, SpM2, Sbm3, m3, M3, SpM3, P4, P5]
	for i in range(900):
		chord_candidate = [tone + random.choice(consonant_steps) * random.choice([-1, 1]) for tone in previous_chord]
		if chord_candidate[-1].frequency_ratio < Fraction(8) and chord_candidate[0].frequency_ratio > Fraction(2, 3):
			if is_chord_sorted(chord_candidate):
				if is_chord_a_fluent_departure_from_initial_chord(chord_candidate, initial_chord):
					chord_quality = name_chord(chord_candidate)
					if chord_quality != None:
						#print(i)
						name = name_chord(chord_candidate)
						#print(name, ":", " ".join([tone.pitch for tone in chord_candidate]))
						return chord_candidate

P1 = Interval((0, 0, 0, 0)) # 1/1
Sp1 = Interval((0, 0, 0, 1)) # 36/35
Sbm2 = Interval((0, 1, 1, -1)) # 28/27
m2 = Interval((0, 1, 1, 0)) # 16/15
M2 = Interval((0, 2, 1, 0)) # 10/9
AcM2 = Interval((1, 2, 1, 0)) # 9/8
SpA1 = Interval((0, 1, 0, 1)) # 15/14
SpM2 = Interval((0, 2, 1, 1)) # 8/7
Sbm3 = Interval((1, 3, 2, -1)) # 7/6
m3 = Interval((1, 3, 2, 0)) # 6/5
M3 = Interval((1, 4, 2, 0)) # 5/4
SpM3 = Interval((1, 4, 2, 1)) # 9/7
P4 = Interval((1, 5, 3, 0)) # 4/3
Sbd5 = Interval((2, 6, 4, -1)) # 7/5
SpA4 = Interval((1, 6, 3, 1)) # 10/7
P5 = Interval((2, 7, 4, 0)) # 3/2
Sbm6 = Interval((2, 8, 5, -1)) # 14/9
m6 = Interval((2, 8, 5, 0)) # 8/5
M6 = Interval((2, 9, 5, 0)) # 5/3
SpM6 = Interval((2, 9, 5, 1)) # 12/7
Sbd7 = Interval((3, 9, 6, -1)) # 42/25
Sbm7 = Interval((3, 10, 6, -1)) # 7/4
m7 = Interval((3, 10, 6, 0)) # 
M7 = Interval((3, 11, 6, 0)) # 
SpM7 = Interval((3, 11, 6, 1)) # 27/14
P8 = Interval((3, 12, 7, 0)) # 2/1
Sbm10 = P8 + Sbm3
SpM10 = P8 + SpM3
P12 = P8 + P5
P15 = P8 + P8

chord_space = {
	#"m": [P1, m3, P5],
	#"maj": [P1, M3, P5],
	"Sbm3": [P1, Sbm3, P5],
	"SpM3": [P1, SpM3, P5],
	"Sbm3,Sbm7": [P1, Sbm3, P5, Sbm7],
	"SpM3,Sbm7": [P1, SpM3, P5, Sbm7],
	#"Sbm3,SpM7": [P1, Sbm3, P5, SpM7],
	"SpM3,SpM7": [P1, SpM3, P5, SpM7],
	#"Sbm3,SpM6": [P1, Sbm3, P5, SpM6],
	"SpM3,SpM6": [P1, SpM3, P5, SpM6],
	#"Sb3dim": [P1, Sbm3, Sbd5],
	#"SbdimSbm7": [P1, Sbm3, Sbd5, Sbm7],
	#"SbdimSpM7": [P1, Sbm3, Sbd5, SpM7],
	#"SbmSbd7": [P1, Sbm3, P5, Sbd7],
	#"SbdimSbd7": [P1, Sbm3, Sbd5, Sbd7],
}

s = Session()
s.tempo = 170
bass = "clarinet"
default = "clarinet"
voice = s.new_part(default)
bass_voice = s.new_part(bass)
#starting_chord = [P1, P5, Sbm10, P12, P15] # 5 notes, two hand piano voicing
starting_chord = [P1, P5, SpM10, P12, P15] # 5 notes, two hand piano voicing
#starting_chord = [Sbm3, P5, Sbm7] # 3 notes, root position
#starting_chord = [Sbm3, P5, Sbm7, Sbm10] # 4 notes, root position
chord_sequence = [starting_chord]
while len(chord_sequence) < 16:
	new_chord = add_chord(chord_sequence[-1], starting_chord)
	if new_chord != None and not are_chords_equal(new_chord, chord_sequence[-1]):
		wait(1)
		chord_name = name_chord(new_chord)
		print('Accept this chord?:', chord_name)
		play_chord(voice, bass_voice, chord_sequence[-1])
		play_chord(voice, bass_voice, new_chord)
		x = input()
		if x in "yY":
			chord_sequence.append(new_chord)
for chord in chord_sequence:
	chord_name = name_chord(chord)
	print([tone.coords for tone in chord], ", #", chord_name)
	play_chord(voice, bass_voice, chord)
