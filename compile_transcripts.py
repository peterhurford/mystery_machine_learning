import os
import re

from collections import defaultdict

from utils import CHARACTERS


statements = defaultdict(lambda: [])


def get_first_name(character):
    return character.split('-')[0].split(' ')[0]

def clean(statement):
    statement = (statement.lower()
                          .replace('?', '')
                          .replace('.', '')
                          .replace('!', '')
                          .replace('"', '')
                          .replace('-', ' ')
                          .replace('\'', '')
                          .replace('\\', '')
                          .replace(',', ''))
    statement = (re.sub('[\(\[].*?[\)\]]', '', statement)
                 .replace('  ', ' ')
                 .strip())
    return statement


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
        if character_string in line or alias_string in line:
            statement = line.replace(character_string, '')
            statement = statement.replace(alias_string, '')
            statement = clean(statement)
            statements[character].append(statement)

for character in CHARACTERS:
    statements[character] = [s for s in statements[character] if s != '']

with open('scooby_doo_lines.csv', 'w') as outfile:
    outfile.write('character,line\n')
    for character in CHARACTERS:
        for statement in statements[character]:
            outfile.write('{},{}\n'.format(character, statement))
