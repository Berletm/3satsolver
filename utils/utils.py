from nnf.dimacs import load
from nnf import Or
import os
import random

PATH_TO_BENCHMARK = "Z:\\PycharmProjects\\5sem\\logic\\3SAT\\uf20-91"
PATH_TO_BENCHMARK2 = "Z:\\PycharmProjects\\5sem\\logic\\3SAT\\uf50-218"
PATH_TO_BENCHMARK3 = "Z:\\PycharmProjects\\5sem\logic\\3SAT\\UF75.325.100"
PATH_TO_BENCHMARK4 = "Z:\\PycharmProjects\\5sem\\logic\\3SAT\\uf100-430"

all_files = os.listdir(PATH_TO_BENCHMARK4)
choices = [True, False]


def get_variables(exp):
    variables = set()
    for node in exp.walk():
        if hasattr(node, "name"):
            variables.add(node.name)
    return variables


def get_clauses(exp):
    clauses = []
    for node in exp.walk():
        if isinstance(node, Or):
            clauses.append(node)
    return clauses
