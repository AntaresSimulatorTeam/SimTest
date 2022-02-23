import argparse
from pathlib import Path
import re
import antares_test_utils as antares_utils

parser = argparse.ArgumentParser()
parser.add_argument("root", help="Directory containing studies",
                    type=str)

parser.add_argument("solver", help="Path to antares-solver",
                    type=str)

args = parser.parse_args()
root = Path(args.root).resolve()
solver_path = Path(args.solver).resolve()

def find_solver(solver):
    solver_path = Path(solver)
    if solver_path.is_file():
        return solver.resolve()
    if solver_path.is_dir():
        results = []
        for x in solver_path.iterdir():
            if x.is_file() and re.match("^antares-[0-9]+\.[0-9]+-solver$", x.name):
                results.append(x)
        assert(len(results) == 1)
        return results[0].resolve()
    raise RuntimeError("Missing solver")

solver_path = find_solver(args.solver)
print(f"Found solver {solver_path}")

studies = antares_utils.list_studies(root)

for study in studies:
    print(study.name + '...', end='')
    result = antares_utils.generate_reference_values(solver_path, study, False, "sirius")
    print('OK' if result else 'KO')
