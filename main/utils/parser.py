from .prompt import OP_EXPLANATION


ALL_OPS = OP_EXPLANATION.keys()

ALL_OPS_lower = []
for op in ALL_OPS:
    ALL_OPS_lower.append(op.lower())



def parse_plan(ops_in_string):
    """
    Parse the plan from the string to the list of operators.
    """

    ops_in_string = ops_in_string.strip()
    OP_str_list = ops_in_string.split(" ")

    OP_list = []
    for op in OP_str_list:
        if op.lower() in ALL_OPS_lower:
            # change op to first leteer upper, other letters lower
            op = op[0].upper() + op[1:].lower()
            OP_list.append(op)

    return OP_list



