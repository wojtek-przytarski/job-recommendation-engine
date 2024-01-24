# Job Recommendation System

This program is designed to provide job recommendations based on candidate bios. It uses a command-line interface for interaction.
The default recommendation system uses Spacy's similarity engine to find the most similar candidates.
I used Spacy as a natural language processing library because it allows to implement a decent solution in a time constraint and 
is easy to use.
The biggest limitation of the program is that it doesn't take into account negative location preferences. 
I decided not to focus on that part because in my opinion correct role recommendation is more important in the limited time.

However, there is also a simple recommendation engine that uses a simple scoring system to find the most similar candidates. 
This illustrates an example on how another engines could be implemented based on the base engine class `RecommendationsEngine`. 
It would allow to build new engines and compare the data between them easily.

## Installation

This project uses `pipenv` for package management. If you don't have `pipenv` installed, you can install it by running:

```bash
pip install pipenv
```

Once `pipenv` is installed, you can install the project dependencies by navigating to the project directory and running:

```bash
pipenv install
```

You also have to download the Spacy model for English language. You can do it by running:

```bash
python -m spacy download en_core_web_md
```

To activate the virtual environment, run:

```bash
pipenv shell
```

## Usage

You can run the program with the following command:

```bash
python main.py
```

You can also run the program with the `--help` option to see a list of available options:

```bash
python main.py --help
```

There are a few options available:

- `--max-delta`: This option allows you to specify the maximum delta compared to the highest score for further recommendations. The default value is 0.1. For example, to use a `max_delta` value of 0.3, you would run:
- `--simple`: This flag allows you to use the simple (and less accurate) recommendation engine. By default, the Spacy recommendations engine is used. To use the simple recommendations engine, you would run:
- `--desired-location-bonus`: This option allows you to specify the bonus for desired location. The default value is 0.1. For example, to use a `desired_location_bonus` value of 0.2, you would run:
- `--show-bio`: This flag allows you to display the candidate's bio. By default, the bio is not displayed. To display the bio, you would run:

## Testing
Unit tests use Pytest framework. To run the tests, you need to install the development dependencies with:
```bash
pipenv install --dev
```

Once the development dependencies are installed, you can run the tests by running:

```bash
pytest
```
