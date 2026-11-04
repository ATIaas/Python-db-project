# Python-db-project

A small key-value database written in Python. Data lives in memory as a hash table and every change is appended to a text file, so the file works as a log of the database's modifications.

We built it to practice good habits on GitHub and when programming: issues, branches, pull requests, tests and conventional commits.

## How it works

- Import the main class (DBmain) and create an instance of the database (`db = Database()`).
- Basic Python dict, with strict(key:str and value:str)
- Each function of the main class returns a json with the result (`{"ok": True or False, "Result": ""}`)
- `set` saves `key:data` in memory and appends it to the file.
- `delete` empties the slot and appends `?key` (Tombstone line) to the file.
- `get` fetches data based on key.
- `consolidate` rewrites the file keeping only the latest valid entry of each key (Deals with tombstone lines).
- Saves to a file. Default is "data" in the same directory, can be specified.

## Project structure

```
src/
    modules/
        consolidate.py
        delete.py
        get.py
        initialize.py
        log_line.py
        parse.py
        set.py
        validate.py
    tests/
        e2e/
            test_database.py
        unit/
            test_consolidate.py
            test_delete.py
            test_get.py
            test_initialize.py
            test_log_line.py
            test_parse.py
            test_set.py
            test_validate.py
        conftest.py
        requirements.txt
    DBmain.py   Primary class that unifies all modules
```

## Running the tests

```
pip install -r src/requirements.txt
cd src
pytest tests.py
```

## Requirements

What the client asked for is in [backlog.md](backlog.md).

## Group members

- Kevin Yicheng Zhang
- Rodrigo Garcia
- Arseniy Lugovoy
- Diego Martinez
