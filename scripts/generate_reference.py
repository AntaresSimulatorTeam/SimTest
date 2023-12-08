import argparse
from pathlib import Path
import re
import antares_test_utils as antares_utils
import sys

parser = argparse.ArgumentParser()
parser.add_argument("root", help="Directory containing studies",
                    type=str)

parser.add_argument("solver", help="Path to antares-solver",
                    type=str)

args = parser.parse_args()
root = Path(args.root).resolve()
solver_path = Path(args.solver).resolve()

def find_solver(solver):
    if sys.platform.startswith("win"):
        suffix=".exe"
    else:
        suffix=""

    solver_path = Path(solver)
    if solver_path.is_file():
        return solver.resolve()
    if solver_path.is_dir():
        results = []
        for x in solver_path.iterdir():
            if x.is_file() and re.match(f"^antares-[0-9]+\.[0-9]+-solver{suffix}$", x.name):
                results.append(x)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing solver")

solver_path = find_solver(args.solver)
print(f"Found solver {solver_path}")

studies = antares_utils.list_studies(root)

def solver_config(study_name):
    if study_name == "valid-milp":
        return ("coin", True)
    else:
        return ("sirius", False)

for study in studies:
    print(study.name + '...', end='')

    # Do we need named MPS problems ?
    named_mps_problems = (study.parent.name == 'valid-named-mps')
    # What optimization solver to use ?
    (opt_solver, use_ortools) = solver_config(study.parent.name)

    result = antares_utils.generate_reference_values(solver_path, study, use_ortools, opt_solver, named_mps_problems)


    print('OK' if result else 'KO')
