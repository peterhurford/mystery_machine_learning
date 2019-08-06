# NOTE: Sign up on developers.datarobot.com
#       Use invite code received at conference and get API key

import os
from datarobotai.client import DataRobotAIClient

dr = DataRobotAIClient.create(key=os.environ['AI_API_KEY'])
ai = dr.create_ai('Mystery Machine Learning')
ai.learn('character', 'scooby_doo_lines.csv')
