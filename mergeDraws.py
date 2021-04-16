import os
import json

directory = "./draws_examples"
draws = {}
for filename in os.listdir(directory):
    with open(os.path.join(directory,filename),"r") as f:
        draw = json.load(f)
        draws.update(draw)

with open(os.path.join(directory,"draws.json"),"w") as f:
    f.write(json.dumps(draws,sort_keys=True, indent=4, separators=(',', ': ')))