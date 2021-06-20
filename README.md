# tennis-bracket

I created this project to play tennis bracket challenges. It allows to create static websites that display the results of tennis bracket challenges.

To make the standings and results available to all participants, I am using the github page of this repository to display the results and allow participants to create their bracket. You can check out some of the challenges I have played with my family at <https://tennis-aa.github.io/tennis-bracket/>. The source code of the website is in the [docs](./docs) folder.

## Installation
I created a python package (pybracket) to help me render the html from jinja templates and scrape the ATP website to obtain players and results. The python dependencies are listed in [requirements.txt](./requirements.txt). It also requires to have [geckodriver](https://github.com/mozilla/geckodriver/releases) installed to be able to scrape some information.

The [docs/js](docs/js) folder contains the javascript functions that read the data in the json files to be displayed in the website.

## Workflow

To make the challenge for an upcoming tournament I follow these steps:

1. Create website: I create a new folder with the html files to display the brackets and standings, and json files that contain the information about the tournament's players and results using the [bracket1_create.py](./bracket1_create.py) script. I then add a link to this folder in [docs/index.html](./docs/index.html).

2. Fill out brackets: I put the website online and ask participants to fill out their bracket. Because so far this project is a static website, the participants download a json file that needs to be emailed to me. I save all the json files in the same folder where I created the website for the tournament. I merge the brackets into a single file with the appropriate name for the website to work with the [bracket2_merge.py](./bracket2_merge.py) script.

3. Update results: I can update the results of the tournament in two different ways. The first one is by using the websites tab to report results. I manually input the results and optionally the scores and then download the json file with the updated results which I place in the websites folder. The second option is to scrape the results from the ATP website using the [bracket3_update.py](./bracket3_update.py) script.

Note: All the scripts require updating the name of the tournament (or any additional info about the tournament).