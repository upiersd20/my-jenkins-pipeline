import unittest
import sys
from io import StringIO

# Импортируем функцию main из hello.py
from hello import main

class TestHelloWorld(unittest.TestCase):
    
    def test_main_output(self):
        """Тест: проверяем, что программа выводит ожидаемый текст"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Hello, World!", output)
        self.assertIn("Jenkins CI/CD Pipeline is working!", output)
    
    def test_main_returns_zero(self):
        """Тест: проверяем, что функция возвращает 0"""
        result = main()
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
