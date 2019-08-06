import os

import pandas as pd

from collections import defaultdict

from utils import CHARACTERS, remove_parentheticals, clean_punct, get_first_name


statements = defaultdict(lambda: [])


transcripts = os.listdir('transcripts')
all_lines = []
for transcript in transcripts:
    with open('transcripts/{}'.format(transcript), 'r') as transcript_file:
        lines = transcript_file.read()
    lines = lines.split('\n')
    all_lines.append(lines)
all_lines = sum(all_lines, [])

for line in all_lines:
    for character in CHARACTERS:
        alias = get_first_name(character)
        character_string = '{}: '.format(character)
        alias_string = '{}: '.format(alias)
        line = remove_parentheticals(line)
        if character_string in line or alias_string in line:
            statement = line.replace(character_string, '')
            statement = statement.replace(alias_string, '')
            statement = clean_punct(statement)
            statements[character].append(statement)

for character in CHARACTERS:
    statements[character] = [s for s in statements[character] if s != '']

# Manually append some famous lines that didn't appear in transcripts,
# so as to not dissapoint the crowd...
statements['Fred Jones'].append('lets split up gang')
statements['Fred Jones'].append('hold the phone')
statements['Fred Jones'].append('light it up')
statements['Velma Dinkley'].append('my glasses i cant see without my glasses')
statements['Velma Dinkley'].append('i cant find my glasses')

# Add more weight on these examples to patch the model a bit more
statements['Fred Jones'].append('lets split up')
statements['Fred Jones'].append('hold the phone')

with open('scooby_doo_lines.csv', 'w') as outfile:
    outfile.write('character,line\n')
    for character in CHARACTERS:
        for statement in statements[character]:
            outfile.write('{},{}\n'.format(character, statement))

lines = pd.read_csv('scooby_doo_lines.csv')
print('Have {} lines...'.format(lines.shape[0]))
print(lines['character'].value_counts())
