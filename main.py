import time
from solvers.dpll import *

def main() -> None:
    start = time.time()
    solve_all_dpll()
    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()
