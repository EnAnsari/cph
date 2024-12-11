# Competitive Programming Helper
I have developed this program for the convenience and speed of competitive programmers, including Codeforces programmers, ICPC and IOI contestants, and enthusiasts of this world. Hoping for high scores and single-digit ranks for all of you ;)

## Prerequisites
1. Python 3.6 or later installed on your system.
2. `pip` (Python's package manager) installed. (some package installed by rcph)
3. Access to a terminal/command prompt.
4. Administrator/root access. (for globlizing)

## Installation
We're going to go through a multi-step installation here. First, we'll download and install the prerequisites, then we'll try to make things easier by installing the global version of the program. Finally, we'll explain how to uninstall it.

**1. Clone the Repository**
First, clone this repository to your local machine:
```bash
git clone https://github.com/enansari/cph
cd chp
```

**2. install our package**
```bash
pip install .
```

<details><summary><strong>using vitural environment</strong></summary><br>

### ubuntu
1. Ensure Python's venv module is installed:
  ```bash
  sudo apt update
  sudo apt install python3-venv
  ```
2. Create a virtual environment:
  ```bash
  python3 -m venv env
  ```
3. Activate the virtual environment:
  ```bash
  source env/bin/activate
  ```
### windows
1. Open Command Prompt or PowerShell.
2. Create a virtual environment:
  ```bash
  python -m venv env
  ```
3. Activate the virtual environment:
  ```bash
  env\Scripts\activate
  ```
***hint: To deactivate the virtual environment:***
  ```bash
  deactivate
  ```
</details><br>

***hint: if you want install requirements from `requirements.txt` file***
```bash
pip install -r requirements.txt
```

## Usage
I have written explanations for each switch [here +](./docs/commands.md). You can also get a deeper understanding of the switches by studying the code. I tried to develop the code in the simplest way possible (even if it is not the most optimal).

I put a structure of the project in the contributing section. In general, I tried to make it very easy and portable by converting the program into a pip package and easily use it anywhere on the system without having to add it to the PATH. I also kept the general settings of the program in a separate [config file](./data/config/contest.json) so that changes to some aspects of the program can be changed.

I also used [constant.py](./rcph/config/constant.py) to put most of the frequently used variables, including some frequently used commands, here so that changes can be easily applied to the entire program at once.

## More Feautres
To use the [codeforces](https://codeforces.com) switch (a powerful parser for Codeforces competitions), you must also install the [chrome driver](https://googlechromelabs.github.io/chrome-for-testing/) and put its address in the [config file](./data/config/contest.json).


## Future Works
- using a Chrome or Firefox extension to parse different contests or problems
- using a vscode (or sublime text or ...) for managing contest instead of CLI and switches
- using databases instead of `json` files
- using a graphical program for better managing and adding notes
- anything you think would make this project better (fiery heart)

## Contributing
We welcome contributions to this project! I tried to make this project as modular and easy to develop as possible.

<details><summary><strong>folder strucure</strong></summary>

#### this is main source code structure:
```bash
.
├── commands # Modules related to various switches
│   ├── asset # using prepared codes
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   ├── launch.py # launch a code
│   │   ├── save.py # save a new code to assets
│   │   └── utils.py
│   ├── cf # codeforces parser (parsing by link and magic ;)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── cp # copy files from data/template (useful files)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── globall # explore in past contests
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── info # showing information about contest (like num of problems, status of they and ...)
│   │   ├── db.py # information about connection of current contest by database (contests saved before)
│   │   ├── edit.py # editing information
│   │   ├── handler.py
│   │   ├── info.py # showing information
│   │   ├── __init__.py
│   │   ├── parent.py # parents of contest
│   │   └── status.py # status of problems
│   ├── init # starting switch: creating a contest
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── judge # make a judgement according to saved test cases
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── make # make a empty template (easy function)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── question # adding or deleting problems (quesitons)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── readme # create readme file (according to local config)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── resign # re-signing of codes (because adding some information about contest or problem)
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── search # search in past contests and test case bank by many things
│   │   ├── handler.py
│   │   ├── __init__.py
│   │   └── utils.py
│   └── tca # for adding test cases
│       ├── handler.py
│       ├── __init__.py
│       └── utils.py
├── config
│   ├── constant.py # global constants
│   ├── data.py # connection of program by data folder
│   ├── __init__.py
│   ├── make.py # make local config
├── core
│   ├── __init__.py
│   └── parser.py # Connecting all switches
├── __init__.py
├── main.py # start point
└── utils # most used functions
    ├── imports.py # imports of external packages
    ├── __init__.py
    ├── launcher # external files business
    │   ├── get.py
    │   ├── __init__.py
    │   └── set.py
    └── tools
        ├── clear.py # clear termial in asset and global
        ├── color.py # create colized terminal output
        ├── hello.py # say hello
        ├── __init__.py
        ├── quote.py # creating quote of legends
        ├── script.py # creating script
        └── sign.py # creating sign
```
</details>

## License
This project is licensed under the [MIT License](/LICENSE). Please don't remove rcph links generators in readme and signature madule.