# Competitive Programming Helper

## Prerequisites
1. Python 3.6 or later installed on your system.
2. `pip` (Python's package manager) installed.
3. Access to a terminal/command prompt.
4. Administrator/root access. (for globlizing)

## Installation
We're going to go through a multi-step installation here. First, we'll download and install the prerequisites, then we'll try to make things easier by installing the global version of the program. Finally, we'll explain how to uninstall it.
<details><summary><strong>local Installation</strong></summary><br>

**1. Clone the Repository**
First, clone this repository to your local machine:
```bash
git clone https://github.com/enansari/cph
cd chp
```

**2. Set Up the Virtual Environment**
#### ubuntu
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
4. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
#### windows
1. Open Command Prompt or PowerShell.
2. Create a virtual environment:
  ```bash
  python -m venv env
  ```
3. Activate the virtual environment:
  ```bash
  env\Scripts\activate
  ```
4. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

***hint: To deactivate the virtual environment:***
  ```bash
  deactivate
  ```

</details><br>


# TODO list
- [ ] Create a professional README
  - [ ] features
  - [ ] documentations (in docs folder)
  - [ ] installation (should use requirement file)
  - [ ] usage (how to use)
  - [ ] how to contribute
  - [ ] future works
- [ ] Creating a powerful and scalable and simple structure
- [ ] Create a `gateway` to the program through each match (create a `shortcut` or `globalize` the program)
- [ ] Create a process to add `test cases` (all simple - give suggestion from gpt)
- [ ] Create a `judge` button to test tests (without time)
- [ ] Creating a process for using ready-made code or `asset`
- [ ] Create a process to `connect different matches` to the main parser (add match address to a specific file)
- [ ] Creating a parser for `quera` matches
- [ ] Creating a parser for `codeforces` matches
- [ ] Auxiliary facilities
  - [ ] Adding `Python` code to the code
  - [ ] Adding `signatures` to codes
  - [ ] Adding `wise sayings` to the code

## Contributing
We welcome contributions to this project!
<!-- (You can include specific guidelines for how people can contribute,  e.g.,  bug reports, feature requests, pull requests). -->

## License
This project is licensed under the [MIT License](/LICENSE).
