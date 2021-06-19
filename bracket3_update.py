import pybracket

tournament = "Roland Garros 21"
path = "docs/" + tournament
b = pybracket.Bracket()
b.loadFromFolder(path)

b.updateResults()
b.save()