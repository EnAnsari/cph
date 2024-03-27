# COMMAND HINT PAGE
On this page, an attempt has been made to deal with parser commands in a classified manner.

## basic definations
- **FILE_ADDRESS**: address of `main.py` in `cp-parser` folder.


## list of commands
- initializing
  - [initializing a contest](#initializing-a-contest)
  - [initializing a question](#initializing-a-question)
- test case
  - [updating test case](#updating-test-case)
  - adding test case
- judge
  - normal judge and test
  - just run
  - just compile
  - removing execution files
- information
  - about contest/question
- assets


### initializing a contest
by parser folder:
```bash
python3 [FILE_ADDRESS] -initialize contest [CONTEST_NAME] -problemnum [NUMBER_OF_PROBLEM]
```

without parser folder:
```bash
python3 [FILE_ADDRESS] -initialize contest [CONTEST_NAME] -problemnum [NUMBER_OF_PROBLEM] -env=off
```

by customize question names:
```bash
python3 [FILE_ADDRESS] -initialize contest [CONTEST_NAME] -problemcustom "A B C D E1 E2 F1 F2 E" 
```
----

### initializing a question
by parser folder:
```bash
python3 [FILE_ADDRESS] -initialize question [FILE_NAME_WITHOUT_CPP]
```

without parser folder:
```bash
python3 [FILE_ADDRESS] -initialize question [FILE_NAME_WITHOUT_CPP] -env=off
```

---
### updating test case
update test case from directory files
```bash
./.parse/r -testcase update
```

status of test case
```bash
./.parse/r -testcase status
```