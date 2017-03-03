## Sneaky Snake

A aggressive / defensive Battlesnake implementation. Written by Phil Denhoff, Daniel Frankcom, Eric Showers, Kyle Thorpe, and Alex Welsh-Piedrahita.

Current feature list is in the `.docx` file. 

### Running / Installing

Install the Microsoft Visual C++ compiler for Python 2.7 from [aka.ms/vcpython27](http://aka.ms/vcpython27).

The required Python packages are listed in `requirements.txt`. They can be batch installed, as an administrator (use sudo), with

```
pip install -r requirements.txt
```

and python-igraph can be installed by following instructions at
[python-igraph install](http://igraph.org/python/#pyinstall). For Windows, use Christoph Gohlke's unofficial installers (pick *-cp27), and

```
python -m pip install /path/to/igraph.whl
```

 ---

Dependencies should be visually confirmed to be installed with
```
pip list
```

## battlesnake-python

A simple [BattleSnake AI](http://battlesnake.io) written in Python.

Visit [battlesnake.io/readme](http://battlesnake.io/readme) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/sendwithus/battlesnake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:username/battlesnake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Test client in your browser: [http://localhost:8080](http://localhost:8080).

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```

## Questions?

Email [phildenhoff@gmail.com](mailto:phildenhoff@gmail.com).
