import re
from collections import defaultdict


CHARACTERS = ['Shaggy Rogers', 'Scooby-Doo', 'Fred Jones', 'Daphne Blake', 'Velma Dinkley']
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


with open('transcripts/scooby_doo_and_the_witches_ghost.txt', 'r') as transcript_file:
    lines = transcript_file.read()
lines = lines.split('\n')

for line in lines:
    for character in CHARACTERS:
        alias = get_first_name(character)
        if character in line or alias in line:
            statement = line.replace('{}: '.format(character), '')
            statement = statement.replace('{}: '.format(alias), '')
            statement = clean(statement)
            statements[character].append(statement)

for character in CHARACTERS:
    statements[character] = [s for s in statements[character] if s != '']

with open('scooby_doo_lines.csv', 'w') as outfile:
    outfile.write('character,line\n')
    for character in CHARACTERS:
        for statement in statements[character]:
            outfile.write('{},{}\n'.format(character, statement))
