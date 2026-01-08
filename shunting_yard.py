def tokenize(expression: str) -> list[str]:
    """
    Парсит входную строку в список токенов.

    Поддерживает оба формата: с пробелами и без пробелов.
    Обрабатывает целые числа, операторы: +, -, *, /, ^ и круглые скобки: (, ).

    Args:
        expression: Арифметическое выражение в виде строки

    Returns:
        Список токенов (числа, операторы, скобки)
    """
    tokens: list[str] = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char in '()+-*/^':
            tokens.append(char)
            i += 1
        elif char.isdigit():
            num_str = ''
            while i < len(expression) and expression[i].isdigit():
                num_str += expression[i]
                i += 1
            tokens.append(num_str)
        else:
            raise ValueError(f"Неизвестный символ: {char}")

    return tokens


def get_precedence(operator: str) -> int:
    """
    Возвращает приоритет оператора.

    Args:
        operator: Оператор (+, -, *, /, ^)

    Returns:
        Приоритет оператора (1 для +, -, 2 для *, /, 3 для ^)
    """
    if operator == '^':
        return 3
    elif operator in ('*', '/'):
        return 2
    elif operator in ('+', '-'):
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
    return token in ('+', '-', '*', '/', '^')


def is_right_associative(operator: str) -> bool:
    """
    Проверяет, является ли оператор правоассоциативным.

    Args:
        operator: Оператор для проверки

    Returns:
        True, если оператор правоассоциативен (^)
    """
    return operator == '^'


def is_left_parenthesis(token: str) -> bool:
    """
    Проверяет, является ли токен открывающей скобкой.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является открывающей скобкой
    """
    return token == '('


def is_right_parenthesis(token: str) -> bool:
    """
    Проверяет, является ли токен закрывающей скобкой.

    Args:
        token: Токен для проверки

    Returns:
        True, если токен является закрывающей скобкой
    """
    return token == ')'


def shunting_yard(expression: str) -> list[str]:
    """
    Преобразует арифметическое выражение в инфиксной записи в обратную польскую нотацию (ПОЛИЗ).

    Реализует алгоритм сортировочной станции (Shunting Yard).
    Поддерживает целые числа, операции +, -, *, /, ^ и круглые скобки.

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
        elif is_left_parenthesis(token):
            operator_stack.append(token)
        elif is_right_parenthesis(token):
            while operator_stack and not is_left_parenthesis(operator_stack[-1]):
                output.append(operator_stack.pop())
            if operator_stack:
                operator_stack.pop()
        elif is_operator(token):
            # Для правоассоциативных операторов (^) используем < вместо <=
            # Для левоассоциативных операторов используем <=
            while (operator_stack and
                   not is_left_parenthesis(operator_stack[-1]) and
                   (get_precedence(token) < get_precedence(operator_stack[-1]) if is_right_associative(token)
                    else get_precedence(token) <= get_precedence(operator_stack[-1]))):
                output.append(operator_stack.pop())
            operator_stack.append(token)

    while operator_stack:
        output.append(operator_stack.pop())

    return output
