CSCI 6032 - Machine Learning

Working Safely with Agents, Git, Docker and Skills

Repository URL: https://github.com/BatOrgil7/csci6032-hw2-batorgil7/

Host operating system: Windows 11 Home, version 25H2, OS Build 26200.9457

Description: This repo is for how to safely automate workflows using any CLI Agents with Docker container. I use docker to put the agent in a sandbox environment to constrain its' work space. Also creating skills for agents to follow.

## Text statistics

`src/text_stats.py` reads one UTF-8 text file and prints a JSON object containing
the number of `lines`, `words`, and `characters`. Words are separated by
whitespace, and characters include whitespace and line breaks.

Run it from the repository root:

```bash
python src/text_stats.py sample.txt
```

Example output:

```json
{"lines": 5, "words": 40, "characters": 227}
```

Run the tests with Python's built-in `unittest` framework:

```bash
python -m unittest discover -s tests
```
