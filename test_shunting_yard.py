import unittest
from shunting_yard import shunting_yard


class TestShuntingYard(unittest.TestCase):
    """Тесты для функции shunting_yard."""

    def test_simple_addition(self):
        """Тест простого сложения."""
        self.assertEqual(shunting_yard("3 + 4"), ["3", "4", "+"])

    def test_simple_subtraction(self):
        """Тест простого вычитания."""
        self.assertEqual(shunting_yard("10 - 5"), ["10", "5", "-"])

    def test_simple_multiplication(self):
        """Тест простого умножения."""
        self.assertEqual(shunting_yard("3 * 4"), ["3", "4", "*"])

    def test_simple_division(self):
        """Тест простого деления."""
        self.assertEqual(shunting_yard("10 / 2"), ["10", "2", "/"])

    def test_operator_precedence(self):
        """Тест приоритета операторов."""
        self.assertEqual(shunting_yard("3 + 4 * 2"), ["3", "4", "2", "*", "+"])
        self.assertEqual(shunting_yard("10 - 5 / 2"), ["10", "5", "2", "/", "-"])

    def test_expression_without_spaces(self):
        """Тест выражения без пробелов."""
        self.assertEqual(shunting_yard("3+4*2"), ["3", "4", "2", "*", "+"])
        self.assertEqual(shunting_yard("10-5/2"), ["10", "5", "2", "/", "-"])

    def test_expression_with_parentheses(self):
        """Тест выражений с круглыми скобками."""
        self.assertEqual(shunting_yard("(3 + 4) * 2"), ["3", "4", "+", "2", "*"])
        self.assertEqual(shunting_yard("10 - (5 + 2)"), ["10", "5", "2", "+", "-"])
        self.assertEqual(shunting_yard("(10 - 5) / 2"), ["10", "5", "-", "2", "/"])

    def test_expression_with_parentheses_no_spaces(self):
        """Тест выражений со скобками без пробелов."""
        self.assertEqual(shunting_yard("(3+4)*2"), ["3", "4", "+", "2", "*"])
        self.assertEqual(shunting_yard("10-(5+2)"), ["10", "5", "2", "+", "-"])

    def test_nested_parentheses(self):
        """Тест вложенных скобок."""
        self.assertEqual(shunting_yard("((3 + 4) * 2)"), ["3", "4", "+", "2", "*"])
        self.assertEqual(shunting_yard("(3 + (4 * 2))"), ["3", "4", "2", "*", "+"])

    def test_complex_expression(self):
        """Тест сложного выражения с комбинацией операций."""
        self.assertEqual(
            shunting_yard("3 + 4 * 2 - 5 / 1"),
            ["3", "4", "2", "*", "+", "5", "1", "/", "-"],
        )
        self.assertEqual(
            shunting_yard("(3 + 4) * (2 - 5)"), ["3", "4", "+", "2", "5", "-", "*"]
        )

    def test_single_number(self):
        """Тест одного числа."""
        self.assertEqual(shunting_yard("42"), ["42"])

    def test_single_operation(self):
        """Тест одного оператора."""
        self.assertEqual(shunting_yard("1 + 2"), ["1", "2", "+"])
        self.assertEqual(shunting_yard("5 * 3"), ["5", "3", "*"])

    def test_power_operation(self):
        """Тест операции возведения в степень."""
        self.assertEqual(shunting_yard("2 ^ 3"), ["2", "3", "^"])
        self.assertEqual(shunting_yard("2 ^ 3 ^ 2"), ["2", "3", "2", "^", "^"])

    def test_power_with_parentheses(self):
        """Тест возведения в степень со скобками."""
        self.assertEqual(shunting_yard("(1 - 5) ^ 2"), ["1", "5", "-", "2", "^"])
        self.assertEqual(shunting_yard("(3 + 4) ^ 2"), ["3", "4", "+", "2", "^"])

    def test_wikipedia_case_with_power(self):
        """Тест сложного выражения с возведением в степень из примера."""
        self.assertEqual(
            shunting_yard("3 + 4 * 2 / (1 - 5) ^ 2 ^ 3"),
            ["3", "4", "2", "*", "1", "5", "-", "2", "3", "^", "^", "/", "+"],
        )

    def test_sin_function(self):
        """Тест функции sin."""
        self.assertEqual(shunting_yard("sin(0)"), ["0", "sin"])
        self.assertEqual(shunting_yard("sin(pi)"), ["pi", "sin"])

    def test_max_function(self):
        """Тест функции max."""
        self.assertEqual(shunting_yard("max(2, 3)"), ["2", "3", "max"])
        self.assertEqual(shunting_yard("max(1, 5)"), ["1", "5", "max"])

    def test_pi_constant(self):
        """Тест константы pi."""
        self.assertEqual(shunting_yard("pi"), ["pi"])
        self.assertEqual(shunting_yard("pi * 2"), ["pi", "2", "*"])

    def test_functions_with_expressions(self):
        """Тест функций с выражениями."""
        self.assertEqual(shunting_yard("sin(2 + 3)"), ["2", "3", "+", "sin"])
        self.assertEqual(shunting_yard("max(2 * 3, 4)"), ["2", "3", "*", "4", "max"])

    def test_wikipedia_case_with_sin_max_and_pi(self):
        """Тест сложного выражения с функциями и константой."""
        self.assertEqual(
            shunting_yard("sin( max(2, 3) / 3 * pi )"),
            ["2", "3", "max", "3", "/", "pi", "*", "sin"]
        )

    def test_unknown_function_error(self):
        """Тест ошибки при парсинге неизвестной функции."""
        with self.assertRaises(ValueError) as context:
            shunting_yard("sin(90) / cos(90)")
        self.assertIn("Неизвестная функция или константа: cos", str(context.exception))


if __name__ == "__main__":
    unittest.main()
