import re

from datetime import datetime


CHARACTERS = ['Shaggy Rogers', 'Scooby-Doo', 'Fred Jones', 'Daphne Blake', 'Velma Dinkley']


def remove_parentheticals(statement):
    statement = (re.sub('[\(\[].*?[\)\]]', '', statement)
                 .replace('  ', ' ')
                 .replace(' :', ':')
                 .strip())
    return statement

def clean_punct(statement):
    statement = (statement.lower()
                          .replace('?', '')
                          .replace('.', '')
                          .replace('!', '')
                          .replace('"', '')
                          .replace('-', ' ')
                          .replace('\'', '')
                          .replace('\\', '')
                          .replace(',', ''))
    return statement

def get_first_name(character):
    return character.split('-')[0].split(' ')[0]

def print_step(step):
    print('[{}]'.format(datetime.now()) + ' ' + step)
