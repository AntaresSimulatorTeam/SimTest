from pathlib import Path
import glob
import shutil
import subprocess

from study import Study

def list_directories(directory):
    dir_path = Path(directory)
    assert(dir_path.is_dir())
    dir_list = []
    for x in dir_path.iterdir():
        if x.is_dir():
            dir_list.append(x)
    return dir_list

def list_studies(directory):
    studies = []
    dir_path = Path(directory)
    if (dir_path.is_dir()):
        study = Study(dir_path)
        if study.check_files_existence():
            studies.append(directory)
        else:
            for x in dir_path.iterdir():
                studies.extend(list_studies(x))

    return studies

def find_output_result_dir(output_dir):
    list_output_dir = list_directories(output_dir)
    assert len(list_output_dir) == 1

    list_dir = list_directories(list_output_dir[0])

    dir_list = []
    for x in list_dir:
        dir_path = Path(x)
        if dir_path.is_dir() and (dir_path.name in ["adequacy", "economy", "adequacy-draft"]):
            dir_list.append(x)
    assert len(dir_list) == 1
    return dir_list[0]

def get_headers(df) -> set :
    return set(df.columns)

def remove_outputs(study_path):
    output_path = study_path / 'output'
    files = glob.glob(str(output_path))
    for f in files:
        shutil.rmtree(f)

def launch_solver(solver_path, study_path, use_ortools = False, ortools_solver = "sirius", named_mps_problems = False, ts_generator_path = ""):
    # Clean study output
    remove_outputs(study_path)

    solver_path_full = str(Path(solver_path).resolve())

    command = [solver_path_full, "-i", str(study_path)]
    if use_ortools:
        command.append('--use-ortools')
        command.append('--ortools-solver='+ortools_solver)
    if named_mps_problems:
        command.append('--named-mps-problems')
    if ts_generator_path != "":
        cluster_to_gen_file = open(study_path / "clustersToGen.txt", 'r')
        cluster_to_gen = cluster_to_gen_file.readline().rstrip() # remove new line char
        cluster_to_gen_file.close()
        command = [ts_generator_path, cluster_to_gen, str(study_path)]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
    stdout, stderr = process.communicate()
    exit_code = process.wait()

    return (exit_code == 0)

def generate_reference_values(solver_path, study_path, use_ortools, ortools_solver, named_mps_problems, ts_generator_path):

    enable_study_output(study_path, True)

    result = launch_solver(solver_path,study_path, use_ortools, ortools_solver, named_mps_problems, ts_generator_path)

    output_path = study_path / 'output'
    list_dir = list_directories(output_path)
    assert len(list_dir) == 1

    result_dir = list_dir[0]

    reference_path = study_path / 'output' / 'reference'
    shutil.move(result_dir, reference_path)
    return result

def enable_study_output(study_path, enable):
    st = Study(study_path)
    if not st.check_files_existence():
        raise RuntimeError("Missing file")

    synthesis_value = "true" if enable else "false"
    st.set_variable(variable = "synthesis", value = synthesis_value, file_nick_name="general")

