# Python-db-project

A small key-value database written in Python. Data lives in memory as a hash table and every change is appended to a text file, so the file works as a log of the database's modifications.

We built it to practice good habits on GitHub and when programming: issues, branches, pull requests, tests and conventional commits.

## How it works

- Each key is turned into a position (the ASCII values of its characters, modulo 100) in a list of 100 slots.
- `set` saves `key:data` in memory and appends it to the file.
- `delete` empties the slot and appends `?key` to the file.
- `getdata` rebuilds the list by reading the file line by line.
- `consolidate` rewrites the file keeping only the latest valid entry of each key.

## Project structure

```
code/
  initialize.py    creates the data file
  set_get.py       set and get
  delete.py        delete
  read_dataset.py  loads the file into memory
  consolidate.py   removes duplicates and delete orders
  dic_convert.py   key to position
  tests.py         pytest tests
backlog.md         client requirements and planned changes
team_history/      notes from the team meetings
```

## Running the tests

```
pip install -r code/requirements.txt
cd code
pytest tests.py
```

## Requirements

What the client asked for is in [backlog.md](backlog.md).

## Group members

- Kevin Yicheng Zhang
- Rodrigo Garcia
- Arseniy Lugovoy
- Diego Martinez
