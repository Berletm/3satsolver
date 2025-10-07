from utils.utils import *

def get_unsatisfied_clauses(clauses, assignment):
    unsatisfied_clauses = []
    for clause in clauses:
        current_variables = get_variables(clause)
        current_model = {v: assignment[v] for v in current_variables}
        if not clause.satisfied_by(current_model):
            unsatisfied_clauses.append(clause)
    return unsatisfied_clauses


def greedy(exp, max_tries=100, max_flips=1000, epsilon_explore=0.1):
    variables = get_variables(exp)
    clauses = get_clauses(exp)

    for try_i in range(max_tries):
        assignment = {v: random.choice(choices) for v in variables}

        for flip in range(max_flips):
            unsatisfied = get_unsatisfied_clauses(clauses, assignment)

            if not unsatisfied:
                return assignment, try_i + 1, flip + 1

            clause = random.choice(unsatisfied)
            current_variables = list(get_variables(clause))

            if random.uniform(0, 1) < epsilon_explore:
                var_to_flip = random.choice(current_variables)
            else:
                best_var = None
                best_score = float("inf")

                for v in current_variables:
                    assignment[v] = not assignment[v]
                    current_score = len(get_unsatisfied_clauses(clauses, assignment))
                    assignment[v] = not assignment[v]

                    if current_score < best_score:
                        best_score = current_score
                        best_var = v

                var_to_flip = best_var

            assignment[var_to_flip] = not assignment[var_to_flip]

    return None, max_tries, 0


def solve_all_random():
    solution_counter = 0
    for f in all_files:
        with open(os.path.join(PATH_TO_BENCHMARK2, f), 'r') as file:
            exp = load(file)

            solution, tries, flips = greedy(exp, max_tries=100, epsilon_explore=0.1)

            if solution:
                print("solution found")
                print(f"tries: {tries}, flips: {flips}")
                print(f"solution: {solution}")
                solution_counter += 1
            else:
                print("didnt find solution")
    print(f"solved: {solution_counter}")
    print(f"failed: {len(all_files) - solution_counter}")
