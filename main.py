#!/usr/bin/env python3
"""
LiteSQL - A lightweight SQL engine supporting basic SQL operations
"""

import os
import sys
import cmd
from parser.sql_parser import SQLParser
from engine.query_executor import QueryExecutor

class LiteSQLPrompt(cmd.Cmd):
    intro = "Welcome to LiteSQL! Type 'help' or '?' for help, 'exit' to quit."
    prompt = "litesql> "
    
    def __init__(self):
        super().__init__()
        self.parser = SQLParser()
        self.executor = QueryExecutor()
        
    def default(self, line):
        if line.lower() == "exit":
            return self.do_exit(line)
        
        try:
            # Parse SQL and execute
            ast = self.parser.parse(line)
            result = self.executor.execute(ast)
            
            # Print result if any
            if result:
                print(result)
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def do_exit(self, arg):
        """Exit the LiteSQL shell"""
        print("Goodbye!")
        return True
    
    def emptyline(self):
        pass
    
def main():
    try:
        LiteSQLPrompt().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()