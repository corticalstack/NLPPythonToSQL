# 🔍 NLPPythonToSQL

A Natural Language Processing (NLP) application that converts English language queries into SQL to retrieve movie and actor information from a MySQL database.

## Description

NLPPythonToSQL is a Python-based application that allows users to query a movie database using natural language. The system parses English language queries, transforms them into formal SQL statements, and returns the requested information from a MySQL database.

The application uses Natural Language Toolkit (NLTK) with Feature-based Context-Free Grammar (FCFG) rules to parse and understand user queries. It supports various query types, including:

- Simple movie title searches
- Actor information retrieval
- Movie description keyword searches
- Random movie selection
- Complete movie and actor listings

## Prerequisites

- Python 3.x
- MySQL server with the Sakila sample database installed
- NLTK library
- mysql-connector-python

## Features

- 🎬 **Natural Language Movie Queries**: Search for movies using everyday language
- 🌟 **Actor Information**: Find movies by actor names
- 🔎 **Keyword Searching**: Search movie descriptions using keywords
- 🔄 **Synonym Recognition**: Understands synonyms for improved query flexibility
- 🎲 **Random Selection**: Can select random movies when requested

## Setup Guide

1. Clone the repository
2. Install required Python packages:
   ```
   pip install nltk mysql-connector-python
   ```
3. Ensure MySQL is installed with the Sakila sample database
4. Update database connection settings in `database.py` if needed:
   ```python
   self.user = 'imat5118'
   self.password = 'imat5118password'
   self.host = '127.0.0.1'
   self.database = 'sakila'
   ```
5. Run the application:
   ```
   python main.py LIMIT 10
   ```
   (The LIMIT parameter is optional and restricts the number of results)

## Usage

Once the application is running, you can enter natural language queries at the prompt. Here are some example queries:

```
How can I help? list all movies

How can I help? show me a random movie

How can I help? complete list of films

How can I help? "AIRPLANE SIERRA"

How can I help? movies starring "PENELOPE GUINESS"

How can I help? list movies about dinosaur and prehistoric
```

To exit the application, type `quit`.

## Architecture

The application consists of several key components:

- **Main Module** (`main.py`): Entry point that handles user interaction
- **Parser** (`parse.py`): Transforms natural language to SQL
- **Grammar Configuration** (`grammar_config.py`): Loads grammar rules and builds synonyms
- **Database Handler** (`database.py`): Manages database connections and query execution
- **Grammar Rules** (`grammars/*.fcfg`): FCFG rules for parsing different query types
- **Support Classes**: 
  - `grammar.py`: Represents grammar rules
  - `stopword.py`: Handles words to ignore during parsing
  - `synonym.py`: Manages word synonyms
  - `word.py`: Represents words extracted from grammar rules

## Resources

- [NLTK Documentation](https://www.nltk.org/)
- [MySQL Sakila Sample Database](https://dev.mysql.com/doc/sakila/en/)
- [Feature-based Context-Free Grammar](https://www.nltk.org/book/ch09.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
