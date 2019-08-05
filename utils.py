import re


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
