from utils.utils import *

def exp_to_list(exp):
    temp = []
    clauses = get_clauses(exp)

    for clause in clauses:
        cur_clause = []
        for l in clause:
            cur_clause.append(int(l.name) * (-1 if not l.true else 1))
        temp.append(cur_clause)
    return temp


def unit_propagation(exp):
    unit_literals = [clause[0] for clause in exp if len(clause) == 1]
    if unit_literals:
        lit = unit_literals[0]
        val = lit > 0
        var = abs(lit)
        return var, val

    return None, None


def simplify(exp, assigment):
    new_exp = []

    for clause in exp:
        satisfied = False
        new_clause = []
        for l in clause:
            v = abs(l)
            if v in assigment:
                sign = l > 0
                if sign == assigment[v]:
                    satisfied = True
                    break
                else:
                    continue
            else:
                new_clause.append(l)
        if not satisfied:
            new_exp.append(new_clause)

    return  new_exp


def pure_elimination(exp):
    all_literals = {lit for clause in exp for lit in clause}
    pure_literals = set()

    for lit in all_literals:
        if -lit not in all_literals:
            pure_literals.add(lit)

    if pure_literals:
        pure_lit = pure_literals.pop()
        val = pure_lit > 0
        var = abs(pure_lit)
        return all_literals, var, val
    return all_literals, None, None


def frequency_heuristic(exp, available_vars):
    freq = {}
    for clause in exp:
        for literal in clause:
            var = abs(literal)
            if var in available_vars:
                freq[var] = freq.get(var, 0) + 1

    if not freq:
        return next(iter(available_vars))

    return max(freq.items(), key=lambda x: x[1])[0]


def dpll(exp, assigment=None):
    if assigment is None:
        assigment = {}

    exp = simplify(exp, assigment)

    if not exp:
        return assigment

    if any(len(clause) == 0 for clause in exp):
        return None

    # setting single variable to be always TRUE
    unit_var, unit_val = unit_propagation(exp)
    if unit_var is not None:
        return dpll(exp, {**assigment, unit_var: unit_val})

    # setting pure variable (when have x and do not have not x)  to be always TRUE
    all_literals, pure_var, pure_val = pure_elimination(exp)
    if pure_var and pure_val:
        return dpll(exp, {**assigment, pure_var: pure_val})

    # setting random variable to be TRUE or FALSE to find if it works
    l = frequency_heuristic(exp, all_literals)
    v = abs(l)

    res = dpll(exp, {**assigment, v:True})
    if res is not None:
        return res

    return dpll(exp, {**assigment, v:False})


def solve_all_dpll():
    for f in all_files:
        with open(os.path.join(PATH_TO_BENCHMARK4, f), 'r') as file:
            exp = load(file)
            lexp = exp_to_list(exp)

            ans = dpll(lexp)

            if ans is not None:
                variables = get_variables(exp)
                ans = {**ans, **{i: False for i in variables if i not in ans}}
                print("solution found")
                print(ans)
            else:
                print("didnt find any solution")
