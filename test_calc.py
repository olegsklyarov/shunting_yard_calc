import unittest
from calc import evaluate_rpn

PI = 3.141592653589793


class TestEvaluateRPN(unittest.TestCase):
    """Тесты для функции evaluate_rpn."""

    def test_simple_addition(self):
        """Тест простого сложения."""
        self.assertEqual(evaluate_rpn("3 4 +"), 7.0)

    def test_simple_subtraction(self):
        """Тест простого вычитания."""
        self.assertEqual(evaluate_rpn("10 5 -"), 5.0)

    def test_simple_multiplication(self):
        """Тест простого умножения."""
        self.assertEqual(evaluate_rpn("3 4 *"), 12.0)

    def test_simple_division(self):
        """Тест простого деления."""
        self.assertEqual(evaluate_rpn("10 2 /"), 5.0)

    def test_power_operation(self):
        """Тест операции возведения в степень."""
        self.assertEqual(evaluate_rpn("2 3 ^"), 8.0)
        self.assertEqual(evaluate_rpn("2 3 2 ^ ^"), 512.0)

    def test_complex_expression(self):
        """Тест сложного выражения."""
        self.assertEqual(evaluate_rpn("3 4 2 * +"), 11.0)
        self.assertEqual(evaluate_rpn("10 5 2 / -"), 7.5)

    def test_expression_with_parentheses_equivalent(self):
        """Тест выражений, эквивалентных скобкам в инфиксной записи."""
        # (3 + 4) * 2 = 3 4 + 2 *
        self.assertEqual(evaluate_rpn("3 4 + 2 *"), 14.0)
        # 10 - (5 + 2) = 10 5 2 + -
        self.assertEqual(evaluate_rpn("10 5 2 + -"), 3.0)

    def test_pi_constant(self):
        """Тест константы pi."""
        result = evaluate_rpn("pi")
        self.assertAlmostEqual(result, PI, places=10)

    def test_pi_in_expression(self):
        """Тест использования pi в выражениях."""
        # pi * 2
        result = evaluate_rpn("pi 2 *")
        self.assertAlmostEqual(result, PI * 2, places=10)

    def test_sin_function(self):
        """Тест функции sin."""
        # sin(0) = 0
        self.assertAlmostEqual(evaluate_rpn("0 sin"), 0.0, places=10)
        # sin(pi/2) = 1
        result = evaluate_rpn("pi 2 / sin")
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_complex_expression_with_functions(self):
        """Тест сложного выражения с функциями."""
        # sin(pi/2) * 2 = 1 * 2 = 2
        result = evaluate_rpn("pi 2 / sin 2 *")
        self.assertAlmostEqual(result, 2.0, places=10)

    def test_wikipedia_case(self):
        """Тест сложного выражения из примера."""
        # 3 + 4 * 2 / (1 - 5) ^ 2 ^ 3
        result = evaluate_rpn("3 4 2 * 1 5 - 2 3 ^ ^ / +")
        expected = 3 + 4 * 2 / ((1 - 5) ** (2**3))
        self.assertAlmostEqual(result, expected, places=10)

    def test_negative_numbers(self):
        """Тест отрицательных чисел."""
        self.assertEqual(evaluate_rpn("-5 3 +"), -2.0)
        self.assertEqual(evaluate_rpn("5 -3 +"), 2.0)

    def test_division_by_zero_error(self):
        """Тест ошибки деления на ноль."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("10 0 /")
        self.assertIn("Деление на ноль", str(context.exception))

    def test_insufficient_operands_operator(self):
        """Тест ошибки недостаточно операндов для оператора."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("3 +")
        self.assertIn("Недостаточно операндов для операции", str(context.exception))

    def test_insufficient_operands_function(self):
        """Тест ошибки недостаточно операндов для функции."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("sin")
        self.assertIn("Недостаточно операндов для функции", str(context.exception))

    def test_unknown_token_error(self):
        """Тест ошибки неизвестного токена."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("3 4 cos")
        self.assertIn("Неизвестный токен: cos", str(context.exception))

    def test_invalid_expression_error(self):
        """Тест ошибки некорректного выражения."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("3 4 + 5")
        self.assertIn("Некорректное выражение", str(context.exception))

    def test_empty_expression(self):
        """Тест пустого выражения."""
        with self.assertRaises(ValueError) as context:
            evaluate_rpn("")
        self.assertIn("Некорректное выражение", str(context.exception))

    def test_complex_expression_from_shunting_yard(self):
        """Тест сложного выражения из test_shunting_yard."""
        rpn_expression = (
            "15 7 1 1 + - / 3 * "
            "2 1 1 + + 15 * "
            "7 200 1 + - / 3 * - "
            "2 1 1 + + "
            "15 7 1 1 + - / 3 * "
            "2 1 1 + + - "
            "15 7 1 1 + - / 3 * + "
            "2 1 1 + + - * -"
        )
        expected = -30.072164948453608
        result = evaluate_rpn(rpn_expression)
        self.assertAlmostEqual(result, expected, places=10)


if __name__ == "__main__":
    unittest.main()
