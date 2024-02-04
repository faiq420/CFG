import re

precedence = {
    "!": 0,
    "(": 1,
    ")": 1,
    "==": 2,
    "!=": 2,
    "<=": 3,
    ">=": 3,
    "<": 3,
    ">": 3,
    "||": 4,
    "&&": 5,
    "+": 6,
    "-": 6,
    "*": 7,
    "/": 7,
}


class Node:
    def __init__(self, value, node_type=None):
        self.value = value
        self.node_type = node_type
        self.left = None
        self.right = None


def get_result_type(operator, left, right):
    if operator == "!":
        return "bool"
    elif left == right and operator in ["==", "!=", "<=", ">=", "<", ">"]:
        return "bool"
    elif left == "num" and right == "num":
        return "num"
    elif left == "num" and right == "fp":
        return "fp"
    elif left == "fp" and right == "fp":
        return "fp"
    elif left == "fp" and right == "num":
        return "fp"
    elif left == "string" and right == "char" and operator == "+":
        return "string"
    elif left == "string" and right == "string" and operator == "+":
        return "string"
    elif left == "char" and right == "char" and operator == "+":
        return "string"
    else:
        raise Exception("Type Mismatch!")


def get_operand_type(id):
    if re.match(r"True|False$", id):
        return "bool"
    elif re.match(r'^"[^"]*"$', id):
        return "string"
    elif re.match(r"'(?:\\.|[^\\'])'", id):
        return "char"
    elif re.match(r"^[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?$", id):
        return "fp"
    elif re.match(r"[0-9]+", id):
        return "num"


def get_precedence(operator):
    return precedence.get(operator, -1)


def is_operand(token):
    if token in precedence:
        return False
    return True


def build_expression_tree_with_types(infix_expression):
    stack = []
    output = []

    for token in infix_expression:
        if is_operand(token):
            operand_type = get_operand_type(token)
            output.append(Node(token, operand_type))
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(Node(stack.pop()))
            stack.pop()  # Pop the '('
        elif not is_operand(token):
            # Handle unary operator "!"
            while stack and get_precedence(token) <= get_precedence(stack[-1]):
                if stack[-1] == "!":
                    output.append(Node(stack.pop()))
                else:
                    break
            stack.append(token)

    while stack:
        output.append(Node(stack.pop()))
    return build_tree_from_postfix(output)


def build_tree_from_postfix(postfix_expression):
    stack = []
    for token in postfix_expression:
        if is_operand(token.value):
            stack.append(token)
        elif not is_operand(token.value):
            if token.value == "!":
                operand = stack.pop()
                operator_node = Node(token.value)
                operator_node.right = operand
                operator_node.node_type = get_result_type(
                    token.value, None, operand.node_type
                )
                stack.append(operator_node)
            else:
                right_operand = stack.pop()
                left_operand = stack.pop()
                operator_node = Node(token.value)
                operator_node.left = left_operand
                operator_node.right = right_operand
                result_type = get_result_type(
                    token.value, left_operand.node_type, right_operand.node_type
                )
                operator_node.node_type = result_type
                stack.append(operator_node)

    result = stack.pop()
    return result.node_type
