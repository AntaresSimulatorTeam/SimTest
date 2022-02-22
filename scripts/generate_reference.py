import argparse
from pathlib import Path

import antares_test_utils as antares_utils

parser = argparse.ArgumentParser()
parser.add_argument("root", help="Directory containing studies",
                    type=str)

parser.add_argument("solver", help="Path to antares-solver",
                    type=str)

args = parser.parse_args()
root = Path(args.root).resolve()
solver_path = Path(args.solver).resolve()

if not solver_path:
    raise RuntimeError("Missing solver")

studies = antares_utils.list_directories(root)

for study in studies:
    print(study.name + '...', end='')
    result = antares_utils.generate_reference_values(solver_path, study, False, "sirius")
    print('OK' if result else 'KO')
