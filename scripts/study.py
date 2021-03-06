from pathlib import Path

class Study:
    """
        Class Study
    """
    def __init__(self, dir_path):
        assert isinstance(dir_path, Path)
        self.study_dir = dir_path
        self.files_path = {}
        self.files_path["desktop"]     = self.study_dir / "Desktop.ini"
        self.files_path["general"]     = self.study_dir / "settings" / "generaldata.ini"
        self.files_path["study"]     = self.study_dir / "study.antares"

    def check_files_existence(self):
        return all([x.is_file() for x in self.files_path.values()])

    def set_variable(self, variable, value, file_nick_name):
        """
            Setting variable with a value in a file
        """
        # File path
        file = self.files_path[file_nick_name]

        # Content to print in file (tmp content)
        content_out = []

        # Reading the file content (content in)
        with open(file) as f:
            content_in = f.readlines()

        # Searching variable and setting its value in a tmp content
        for line in content_in:
            if line.strip().startswith(variable):
                content_out.append(variable + " = " + value + "\n")
            else:
                content_out.append(line)

        # Erasing file content with the tmp content (content out)
        with open(file, "w") as f:
            f.writelines(content_out)
