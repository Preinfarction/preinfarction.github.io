import math
import matplotlib.pyplot as plt
from fractions import Fraction as F

def plot_dissonance_curve(intervals, dissonances):
	ticks = []
	for numerator in range(1, 15):
		for denominator in range(1, 13):
			ratio = F(numerator, denominator)
			if ratio >= 1 and ratio <= 2 and numerator + denominator < 21:
				ticks.append(ratio)
	plt.xticks([float(i) for i in ticks], [str(i) for i in ticks])
	xs = intervals
	ys = dissonances
	plt.plot(xs, ys)
	plt.grid()
	plt.show()

def calculate_dissonance_curve(num_partials, frequencies_of_partials, amplitudes_of_partials):
	d_star = 0.24
	s1 = 0.0207
	s2 = 18.96
	c1 = 5
	c2 = -5
	a1 = -3.51
	a2 = -5.75
	index = 0
	low_interval = 1
	high_interval = 2.1
	increment = 0.002
	num_samples = int((high_interval - low_interval) / increment)
	dissonances = [0 for i in range(num_samples + 1)]
	intervals = [0 for i in range(num_samples + 1)]
	all_partials_at_interval = [0 for i in range(num_partials)]
	interval = low_interval
	while interval < high_interval:
		interval += increment
		dissonance = 0
		for k in range(1, num_partials):
			all_partials_at_interval[k] = interval * frequencies_of_partials[k]
		# Calculate the dissonance between frequencies_of_partials[] and interval * frequencies_of_partials[].
		for i in range(1, num_partials):
			for j in range(1, num_partials):
				freq_min = min(all_partials_at_interval[j], frequencies_of_partials[i])
				s = d_star / (s1 * freq_min + s2)
				freq_diff = abs(all_partials_at_interval[j] - frequencies_of_partials[i])
				exp1 = math.e ** (a1 * s * freq_diff)
				exp2 = math.e ** (a2 * s * freq_diff)
				if (amplitudes_of_partials[i] < amplitudes_of_partials[j]):
					dissonance_component = amplitudes_of_partials[i] * (c1 * exp1 + c2 * exp2)
				else:
					dissonance_component = amplitudes_of_partials[j] * (c1 * exp1 + c2 * exp2)
				dissonance += dissonance_component
		dissonances[index] = dissonance
		intervals[index] = interval
		index += 1
	return (intervals, dissonances)

num_partials = 10
frequencies_of_partials = [440 * i for i in range(1, num_partials + 1)]
amplitudes_of_partials = [1 / (1 + i) for i in range(1, num_partials + 1)]
intervals, dissonances = calculate_dissonance_curve(num_partials, frequencies_of_partials, amplitudes_of_partials)
plot_dissonance_curve(intervals, dissonances)
