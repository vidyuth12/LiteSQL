"""
Basic tests for LiteSQL
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.sql_parser import SQLParser
from engine.query_executor import QueryExecutor

class TestLiteSQL(unittest.TestCase):
    
    def setUp(self):
        self.parser = SQLParser()
        self.executor = QueryExecutor()
    
    def test_create_table(self):
        sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        ast = self.parser.parse(sql)
        result = self.executor.execute(ast)
        self.assertIn("Table 'users' created", result)
    
    def test_insert(self):
        # First create the table
        create_sql = "CREATE TABLE test_insert (id INTEGER PRIMARY KEY, name TEXT)"
        ast = self.parser.parse(create_sql)
        self.executor.execute(ast)
        
        # Then insert a row
        insert_sql = "INSERT INTO test_insert VALUES (1, 'Test User')"
        ast = self.parser.parse(insert_sql)
        result = self.executor.execute(ast)
        self.assertIn("Inserted 1 row", result)
    
    def test_select(self):
        # First create and populate the table
        create_sql = "CREATE TABLE test_select (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        self.executor.execute(self.parser.parse(create_sql))
        
        insert_sql = "INSERT INTO test_select VALUES (1, 'Alice', 30)"
        self.executor.execute(self.parser.parse(insert_sql))
        
        insert_sql = "INSERT INTO test_select VALUES (2, 'Bob', 25)"
        self.executor.execute(self.parser.parse(insert_sql))
        
        # Test select all
        select_sql = "SELECT * FROM test_select"
        ast = self.parser.parse(select_sql)
        result = self.executor.execute(ast)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.rows), 2)
        
        # Test select with where clause
        select_sql = "SELECT * FROM test_select WHERE age > 25"
        ast = self.parser.parse(select_sql)
        result = self.executor.execute(ast)
        self.assertEqual(len(result.rows), 1)
        self.assertEqual(result.rows[0][1], 'Alice')
    
    def test_select_columns(self):
        # First create and populate the table
        create_sql = "CREATE TABLE test_projection (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        self.executor.execute(self.parser.parse(create_sql))
        
        insert_sql = "INSERT INTO test_projection VALUES (1, 'Alice', 30)"
        self.executor.execute(self.parser.parse(insert_sql))
        
        # Test select specific columns
        select_sql = "SELECT name, age FROM test_projection"
        ast = self.parser.parse(select_sql)
        result = self.executor.execute(ast)
        self.assertEqual(len(result.column_names), 2)
        self.assertEqual(result.column_names[0], 'name')
        self.assertEqual(result.column_names[1], 'age')
        self.assertEqual(len(result.rows[0]), 2)
        self.assertEqual(result.rows[0][0], 'Alice')
        self.assertEqual(result.rows[0][1], 30)

if __name__ == '__main__':
    unittest.main()