import os
import re

from updated_alto_parser.alto_file import AltoFile


class AltoTextParser:

    files = []

    def __init__(self):
        self.files = []

    def add_files(self, directory_path, file_ending='.xml'):
        """Add all files with the given file ending in the given directory to the list of files to be parsed."""
        if not os.path.isdir(directory_path):
            raise ValueError("The given path is not a directory.")
        for file in os.listdir(directory_path):
            if file.endswith(file_ending):
                self.add_file(os.path.join(directory_path, file))

    def add_file(self, file_path):
        alto_file = AltoFile(file_path)
        self.files.append(alto_file)

    def parse_text(self):
        for alto_file in self.files:
            alto_file.parse_text()

    def get_alto_files(self):
        return self.files

    def extract_meta_from_filenames(self, parameter_name, parameter_pattern):
        for file in self.files:
            filename = os.path.basename(file.file_path)
            match = re.search(parameter_pattern, filename)
            if match:
                file.add_file_meta_data(parameter_name, match.group(1))

    def add_meta_data_to_files(self, parameter_name, static_value):
        for file in self.files:
            file.add_file_meta_data(parameter_name, static_value)

    def export_lines_to_csv(self, file_path):
        for file in self.files:
            file.export_to_csv(file_path, 'text_line')

    def export_lines_to_json(self, file_path):
        for file in self.files:
            file.export_to_csv(file_path, 'text_line')

    def export_regions_to_csv(self, file_path):
        for file in self.files:
            file.export_to_csv(file_path, 'text_region')

    def export_regions_to_json(self, file_path):
        for file in self.files:
            file.export_to_csv(file_path, 'text_region')

