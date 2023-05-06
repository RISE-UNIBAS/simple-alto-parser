"""This module contains the class AltoTextParser, which is used to parse text from ALTO files."""
import os
import re

from simple_alto_parser.alto_file import AltoFile


class AltoTextParser:
    """This class is used to parse text from ALTO files. It stores the files in a list of AltoFile objects."""

    files = []

    def __init__(self):
        """The constructor of the class. It initializes the list of files."""
        self.files = []

    def add_files(self, directory_path, file_ending='.xml'):
        """Add all files with the given file ending in the given directory to the list of files to be parsed."""

        if not os.path.isdir(directory_path):
            raise ValueError("The given path is not a directory.")

        for file in os.listdir(directory_path):
            if file.endswith(file_ending):
                self.add_file(os.path.join(directory_path, file))

    def add_file(self, file_path):
        """Add the given file to the list of files to be parsed."""

        alto_file = AltoFile(file_path)
        self.files.append(alto_file)

    def parse_text(self):
        """Parse the text from all files in the list of files."""

        for alto_file in self.files:
            alto_file.parse_text()

    def get_alto_files(self):
        """Return the list of AltoFile objects."""

        return self.files

    def extract_meta_from_filenames(self, parameter_name, parameter_pattern):
        """Extract the given parameter from the filenames of the files in the list of files. This means that filenames
        that match the given pattern are searched for the given parameter. If the parameter is found, it is added to
        the metadata of the file."""

        for file in self.files:
            filename = os.path.basename(file.file_path)
            match = re.search(parameter_pattern, filename)
            if match:
                file.add_file_meta_data(parameter_name, match.group(1))

    def add_meta_data_to_files(self, parameter_name, static_value):
        """Add the given parameter with the given value to the metadata of all files in the list of files."""

        for file in self.files:
            file.add_file_meta_data(parameter_name, static_value)

    def export_lines_to_csv(self, file_path, **kwargs):
        """Export the text lines of all files in the list of files to a csv file."""

        for file in self.files:
            file.export_to_csv(file_path, 'text_line', **kwargs)

    def export_lines_to_json(self, file_path):
        """Export the text lines of all files in the list of files to a json file."""

        for file in self.files:
            file.export_to_json(file_path, 'text_line')

    def export_regions_to_csv(self, file_path):
        """Export the text regions of all files in the list of files to a csv file."""

        for file in self.files:
            file.export_to_csv(file_path, 'text_region')

    def export_regions_to_json(self, file_path):
        """Export the text regions of all files in the list of files to a json file."""

        for file in self.files:
            file.export_to_json(file_path, 'text_region')

