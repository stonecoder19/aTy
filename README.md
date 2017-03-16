## About 

🇯🇲

aTy (pronounced ay-tee/eighty) stands for “autonomous Twitter yaadie”, and is a bot that tweets Jamaican things (things Jamaicans care about). 
The name is also a permutation of [Microsoft’s "Tay"](https://en.wikipedia.org/wiki/Tay_(bot)) which was a completely autonomous 
Twitter chatterbot built in 2016. 

### Technical Details

aTy uses python 3, and a few dependencies installed via pip. 

#### Installation 

Clone the repository: `$ git clone git@github.com:ANich/aTy.git your-directory`

Create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/): `$ virtualenv -p python3 VENV`

Install the dependencies: `$ pip install -r requirements.txt`

And run  `$ python bot.py > log.file &`

(& is used to run as a background process, to close: use `$ fg` to bring it to the foreground, then Ctrl-C. Alternatively you can use `$ kill pid`)

#### Style Guide

For consistency, the pep8 standard is used to format the code. For that reason [autopep8](https://pypi.python.org/pypi/autopep8) is a dependency
and will be installed after you `pip install`

To format your code: `$ autopep8 --in-place --aggressive --aggressive *.py`

### TBA
- Roadmap
- Link to account
