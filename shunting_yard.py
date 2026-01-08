def tokenize(expression: str) -> list[str]:
    """
    Парсит входную строку в список токенов.

    Поддерживает оба формата: с пробелами и без пробелов.
    Обрабатывает целые числа, операторы: +, -, *, /, ^, функции (sin),
    константы (pi) и круглые скобки: (, ).

    Args:
        expression: Арифметическое выражение в виде строки

    Returns:
        Список токенов (числа, операторы, функции, константы, скобки)
    """
    tokens: list[str] = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char in "()+-*/^":
            tokens.append(char)
            i += 1
        elif char.isdigit():
            num_str = ""
            while i < len(expression) and expression[i].isdigit():
                num_str += expression[i]
                i += 1
            tokens.append(num_str)
        elif char.isalpha():
            identifier = ""
            while i < len(expression) and expression[i].isalpha():
                identifier += expression[i]
                i += 1
            tokens.append(identifier)
        else:
            raise ValueError(f"Неизвестный символ: {char}")

    return tokens


def get_precedence(operator: str) -> int:
    """
    Возвращает приоритет оператора или функции.

    Args:
        operator: Оператор (+, -, *, /, ^) или функция (sin)

    Returns:
        Приоритет оператора (1 для +, -, 2 для *, /, 3 для ^, 4 для функций)
    """
    if is_function(operator):
        return 4
    elif operator == "^":
        return 3
    elif operator in ("*", "/"):
        return 2
    elif operator in ("+", "-"):
        return 1
    return 0


def is_operator(token: str) -> bool:
    """
    Проверяет, является ли токен оператором.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является оператором
    """
    return token in ("+", "-", "*", "/", "^")


def is_right_associative(operator: str) -> bool:
    """
    Проверяет, является ли оператор правоассоциативным.

    Args:
        operator: Оператор для проверки

    Returns:
        True, если оператор правоассоциативен (^)
    """
    return operator == "^"


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


def is_left_parenthesis(token: str) -> bool:
    """
    Проверяет, является ли токен открывающей скобкой.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является открывающей скобкой
    """
    return token == "("


def is_right_parenthesis(token: str) -> bool:
    """
    Проверяет, является ли токен закрывающей скобкой.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является закрывающей скобкой
    """
    return token == ")"


def shunting_yard(expression: str) -> list[str]:
    """
    Преобразует арифметическое выражение в инфиксной записи в обратную польскую нотацию (ПОЛИЗ).

    Реализует алгоритм сортировочной станции (Shunting Yard).
    Поддерживает целые числа, операции +, -, *, /, ^, функции (sin),
    константы (pi) и круглые скобки.

    Args:
        expression: Арифметическое выражение в инфиксной записи

    Returns:
        Список токенов в обратной польской нотации
    """
    tokens = tokenize(expression)
    output: list[str] = []
    operator_stack: list[str] = []

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif is_constant(token):
            output.append(token)
        elif is_left_parenthesis(token):
            operator_stack.append(token)
        elif is_right_parenthesis(token):
            while operator_stack and not is_left_parenthesis(operator_stack[-1]):
                output.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()
            # Если на вершине стека функция, переносим её в выход
            if operator_stack and is_function(operator_stack[-1]):
                output.append(operator_stack.pop())
        elif is_function(token):
            operator_stack.append(token)
        elif is_operator(token):
            # Для правоассоциативных операторов (^) используем < вместо <=
            # Для левоассоциативных операторов используем <=
            while (
                operator_stack
                and not is_left_parenthesis(operator_stack[-1])
                and not is_function(operator_stack[-1])
                and (
                    get_precedence(token) < get_precedence(operator_stack[-1])
                    if is_right_associative(token)
                    else get_precedence(token) <= get_precedence(operator_stack[-1])
                )
            ):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            # Неизвестный идентификатор
            if token.isalpha():
                raise ValueError(f"Неизвестная функция или константа: {token}")

    while operator_stack:
        output.append(operator_stack.pop())

    return output


def main() -> None:
    """CLI интерфейс для преобразования выражений в обратную польскую нотацию."""
    import sys

    try:
        expression = sys.stdin.read().strip()
        if not expression:
            return
        result = shunting_yard(expression)
        print(" ".join(result))
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
