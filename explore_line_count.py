import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

lines = pd.read_csv('scooby_doo_lines.csv')

character_counts = lines['character'].value_counts()
y_pos = np.arange(len(character_counts))

labels = character_counts.keys()
y_pos = np.arange(len(labels))
counts = character_counts.values

plt.bar(y_pos, counts, align='center', alpha=0.5)
plt.xticks(y_pos, labels)
plt.ylabel('Total lines said')

plt.show()
