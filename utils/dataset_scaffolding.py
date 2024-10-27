import json
import os

completions = json.load(open(os.path.join('data', 'completions.json')))

for completion in completions:
    completion['label'] = None