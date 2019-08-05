import pandas as pd
import datarobot as dr

from pprint import pprint
from collections import defaultdict

from utils import CHARACTERS


lines = pd.read_csv('scooby_doo_lines.csv')
projects = defaultdict(lambda: '')


def is_desired_model(model):
    return (any([p == 'Matrix of word-grams occurrences' for p in model.processes]) and
            any(['Elastic-Net' in p for p in model.processes]))


for character in CHARACTERS:
    print('Initializing {} model...'.format(character))
    lines_for_character = lines.copy()
    lines_for_character['target'] = (lines_for_character['character'] == character).astype(int)
    lines_for_character.drop('character', axis=1, inplace=True)
    partition = dr.partitioning_methods.RandomCV(reps=5, holdout_pct=0)
    project = dr.Project.start(lines_for_character,
                               project_name=character,
                               target='target',
                               autopilot_on=False,
                               partitioning_method=partition,
                               worker_count=-1)
    models = project.get_blueprints()
    desired_model = [m for m in models if is_desired_model(m)][0]
    print('Building {} model...'.format(character))
    project.train(desired_model,
                  sample_pct=80,
                  scoring_type=dr.SCORING_TYPE.cross_validation)
    projects[character] = project.id

pprint(sorted([(p[0], dr.Project.get(p[1]).get_models()[0].metrics['AUC']['crossValidation']) for p in list(projects.items())[:-1]], key=lambda x: x[1], reverse=True))
# [('Scooby-Doo', 0.9677279999999999),
#  ('Shaggy Rogers', 0.828508),
#  ('Velma Dinkley', 0.737328),
#  ('Daphne Blake', 0.671656),
#  ('Fred Jones', 0.643386)]

import pdb
pdb.set_trace()
