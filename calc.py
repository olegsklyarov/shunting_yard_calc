import math
import sys


def parse_tokens(expression: str) -> list[str]:
    """
    Парсит входную строку на токены (разделенные пробелами).

    Args:
        expression: Строка с выражением в ПОЛИЗ

    Returns:
        Список токенов
    """
    if not expression.strip():
        return []
    return expression.strip().split()


def is_operator(token: str) -> bool:
    """
    Проверяет, является ли токен оператором.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является оператором
    """
    return token in ("+", "-", "*", "/", "^")


def is_function(token: str) -> bool:
    """
    Проверяет, является ли токен функцией.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является функцией (sin)
    """
    return token == "sin"


def is_constant(token: str) -> bool:
    """
    Проверяет, является ли токен константой.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является константой (pi)
    """
    return token == "pi"


def evaluate_rpn(expression: str) -> float:
    """
    Вычисляет результат арифметического выражения в обратной польской нотации (ПОЛИЗ).

    Поддерживает целые числа, операции +, -, *, /, ^, функции (sin),
    константы (pi).

    Args:
        expression: Арифметическое выражение в обратной польской нотации

    Returns:
        Результат вычисления

    Raises:
        ValueError: При недостаточном количестве операндов, делении на ноль,
                   неизвестном токене или некорректном результате
    """
    tokens = parse_tokens(expression)
    stack: list[float] = []

    for token in tokens:
        if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
            stack.append(float(token))
        elif is_constant(token):
            stack.append(math.pi)
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise ValueError("Деление на ноль")
                result = a / b
            elif token == "^":
                result = a ** b
            else:
                raise ValueError(f"Неизвестный оператор: {token}")

            stack.append(result)
        elif is_function(token):
            if len(stack) < 1:
                raise ValueError("Недостаточно операндов для функции")
            operand = stack.pop()

            if token == "sin":
                result = math.sin(operand)
            else:
                raise ValueError(f"Неизвестная функция: {token}")

            stack.append(result)
        else:
            raise ValueError(f"Неизвестный токен: {token}")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение: в стеке остается не один элемент")

    return stack[0]


def main() -> None:
    """CLI интерфейс для вычисления выражений в обратной польской нотации."""
    try:
        expression = sys.stdin.read().strip()
        if not expression:
            return
        result = evaluate_rpn(expression)
        print(result)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

