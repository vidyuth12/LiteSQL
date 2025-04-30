## LiteSQL
A lightweight SQL engine supporting in-memory table storage, basic SQL parsing, and query execution using a custom AST and planner. Designed with modular components inspired by real DBMS internals.

# Features
  - In-memory table storage
  - Basic SQL parsing and execution
  - Supports common SQL operations:
  
  - CREATE TABLE table_name (...)
  - INSERT INTO table_name VALUES (...)
  - SELECT * FROM table_name
  - Simple WHERE clauses with comparison operators

# Setup and Installation

1) Clone the repository
2) Install required dependencies:
  pip install lark-parser
3) Run the interactive SQL shell:
  python main.py

# Usage Examples
Start the LiteSQL shell:

  $ python main.py
  Welcome to LiteSQL! Type 'help' or '?' for help, 'exit' to quit.
  litesql>

Create a table:

  litesql> CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);
  Table 'users' created with 3 columns

Insert data:

  litesql> INSERT INTO users VALUES (1, 'John Doe', 30);
  Inserted 1 row into 'users' (ID: 0)

Query data:

  litesql> SELECT * FROM users;
  id | name     | age
  ---+----------+----
  1  | John Doe | 30
  (1 rows)

Query with WHERE clause:

  litesql> SELECT name FROM users WHERE age > 25;
  name  
  --------
  John Doe
  (1 rows)
  Running Tests
  python -m unittest tests/test_basic.py
  
# Limitations

  Only supports basic SQL syntax
  In-memory storage only (no persistence)
  Limited data types (INTEGER, TEXT, FLOAT, DOUBLE)
  Simple WHERE conditions only (no complex expressions)
  No joins or aggregations yet

# Future Enhancements

  Support for more SQL operations (UPDATE, DELETE)
  Expanded WHERE clause support
  Simple joins
  Basic aggregation functions (COUNT, SUM, AVG)
  File-based storage for persistence
  Transaction support



