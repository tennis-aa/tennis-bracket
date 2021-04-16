import os
import json

directory = "./brackets_examples"
brackets = {}
for filename in os.listdir(directory):
    with open(os.path.join(directory,filename),"r") as f:
        bracket = json.load(f)
        brackets.update(bracket)

with open(os.path.join(directory,"brackets.json"),"w") as f:
    f.write(json.dumps(brackets,sort_keys=True, indent=4, separators=(',', ': ')))