import pandas as pd
import datarobot as dr

from collections import defaultdict

from utils import CHARACTERS


lines = pd.read_csv('scooby_doo_lines.csv')
projects = defaultdict(lambda: '')

for character in CHARACTERS:
    print('Building {} model...'.format(character))
    lines['target'] = (lines['character'] == character).astype(int)
    lines.drop('character', axis=1, inplace=True)
    project = dr.Project.start(lines,
                               project_name=character,
                               target='target',
                               worker_count=-1)
    project.wait_for_autopilot(timeout=2*60*60*60)
    projects[character] = project.id
import pdb
pdb.set_trace()
