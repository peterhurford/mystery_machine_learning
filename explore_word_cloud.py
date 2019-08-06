import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud


def plot_character_words(character):
	lines = pd.read_csv('scooby_doo_lines.csv')
	lines = lines[lines['character'] == character]  # Filter to character
	lines = lines['line']                           # Get the text data
	lines = [l.split(' ') for l in lines]           # Split each line into individual words
	lines = sum(lines, [])                          # Turn into single list of words
	lines = ' '.join(lines)                         # Convert into string for wordcloud
	wordcloud = WordCloud().generate(lines)         # Make word cloud
	plt.imshow(wordcloud, interpolation='bilinear') # Plot
	plt.axis('off')
	plt.show()

plot_character_words('Scooby-Doo')

import pdb
pdb.set_trace()
