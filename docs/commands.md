# Guide to various program commands

You can also find out most of the switches and subswitches by reading the [parser.py](../rcph/core/parser.py) file.

| command | description | arguments |
|:---:|---|---|
| `init` (`i`) | Creating a `.rcph` file and generally creating a contest | `<folder name>`: this argument use for contest name by default (if you use `.` instead of a name current directory select for root directory for contest.<br>`test`: this argument use for activing test mode and unsaving in contest db file (`contests.json` by default)
| `resign` (`sign`) | for rewriting `sign` of problems | `<problem letter>`: This argument may be a ‍`.` or a `<problem letter>`. |
| `info` | Display general contest information including all contest details such as its name, link, details, repository of gates, as well as question details such as name, letter, and status. We also use this switch for editing. | `-empty-`: for showing brief information<br>`edit`: for editing informations<br>`status`: for editing problems status<br>`db`: to edit database connection (using `-empty` or `add` or `rm` as 2nd subcommand)<br>`parent`: for editing parent (using `choose` or `-empty-` or `+` (or `add`) for editing parents) |
| `tca` (`t`) | for adding test case | `<problem_name>` or `.` or `domejudge` |
| `judge` (`j`) | judgement of problem code | `<problem_name>` or using last judge (empty argument) or `input` for executing `input.txt` |
| `asset` (`ass`) | using prepared codes | `save` or `+`: for adding a script as asset in asset directory (you should enter your file to load as 2nd subcommand)<br>`-empty-`: for launch a script to your current contest |
| `search` | searching in past contests or testcase bank (search by contest name - problem name - test cases in past contest or test case bank) | without switch |
| `codeforces` (`cf`) | parsing codeforces page (contest) and load information like test case or problem name | without argument |
| `global` | explore in past contests | without argument |
| `question` (`q`) | for adding or removing problems | `add` and `rm` as 1st subcommand and `.` or `<problem_name>` as 2nd subcommand (`.` for multi adding/removing) |
| `make` and `cp` | for copying codes from [data/template](../data/template/) | `<source_path>` as 1st subcommand and `<destination_path>` as 2nd subcommand (optional) (for `make` you just need `<des_path>`) |
| `connect` | for connecting elements like **asset folder** and **tcbank** and **chrome driver** (for codeforces parser) | without argument |