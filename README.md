# Backend Engineering Challenge

This is my solution to the challenge

## Installation

This project uses Python 3.5 and pipenv.

If you have other Python version use pyenv.

Install pyenv:

``` $ brew install pyenv ```

Install Python 3.5:

``` $ pyenv install 3.5.0 ```

Change global version to 3.5.0:

``` $ pyenv global 3.5.0 ```

Verify change:

``` 
$ python --version 

Python 3.5.0
```

If version does not change verify if you have pyenv shims directory in your PATH.

https://github.com/pyenv/pyenv#understanding-shims

Then install pipenv to manage Python version and dependencies (present in Pipenv file)

```$ pip install pipenv ```

In the Pipenv file we can see the Python version and the package versions used by the solution.

In the root of the project to install dependencies run:

```$ pipenv install ```

This generates a Pipfile.lock with the packages that will be used by the application.

## Tests

The solution has some tests that can be used. In the root of the project run:

```$ pipenv run pytest ```

## Usage

To use the application run the following command with the necessary arguments:

``` 
$ pipenv run python unbabel_cli.py --input_file tests/data/events_test.json --window_size 10 --output_file results.json

```
This will output the result present in the challenge README page.

To understand what the arguments mean run:

```
$ pipenv run python unbabel_cli.py --help 

Usage: unbabel_cli.py [OPTIONS]

Options:
  --input_file PATH            File in JSON format to read translation events
                               (must exists).
  --window_size INTEGER RANGE  Average window size in minutes.
  --output_file PATH           File to store the translation average info.
  --help                       Show this message and exit.
```

The arguments are similar to those presented in the challenge with the exception of "output_file" that refers to the file where the results must be stored.

## Other notes

The solution begins in the unbabel_cli.py script that implements a CLI that parses the necessary arguments and starts the translation events processing.
The implementation was separated into three classes.

### EventStreamReader

Implements an iterator that reads a file in JSON lines format one event at a time. Ignores malformed JSON and events that do not have the necessary fields for the average calculation.

### TimeslotDurationAverage

This class has functions to support the average calculation. It stores the current window of events from where the average for the current timeslot (current minute minus window_size) is calculated. This window of events gets cleaned from events outside the window size to save memory space.

### ResultsWriter

Class that writes dictionaries in JSON lines format to a file.

In the main file (unbabel_cli.py) these classes are instantiated with the arguments given on the command and there is a loop that iterates through the events from the translation files and calculates the averages minute by minute.
