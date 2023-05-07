"""This module contains the AltoFile class. It is used to parse an alto file and to store the data in a structured
way. The class is used by the AltoTextParser class."""
import os.path


class AltoFile:
    """This class represents an alto file. It is used to parse an alto file and to store the data.
    The class stores TextBlocks or TextLines, depending on the configuration of the parser in the
    file_elements list. Items in this list get treated as text lines by the parser."""

    file_path = None
    """The path to the file."""

    file_elements = []
    """A list of the text elements in the alto file. These can be TextBlocks or TextLines, depending on the
    configuration of the parser."""

    parser = None
    """The parser that is used to parse the file."""

    def __init__(self, file_path, parser):
        """The constructor of the class. It takes the path to the file as a parameter."""

        if not os.path.isfile(file_path):
            raise ValueError("The given path is not a file.")

        self.file_path = file_path
        self.file_meta_data = {}
        self.parser = parser
        self.file_elements = []

    def get_text_lines(self):
        """This function returns the text lines of the alto file."""
        return self.file_elements

    def add_file_meta_data(self, parameter_name, parameter_value):
        """This function adds metadata to the file. It takes the parameter name and the parameter value as parameters.
        The parameter name should be a string and the parameter value can be any type."""
        self.file_meta_data[parameter_name] = parameter_value

    def get_csv_header(self):
        """This function returns the header of the csv file. It is used by the export_to_csv() function."""

        csv_title_line = ['text', 'file']
        for key, value in self.file_elements[0].element_data.items():
            csv_title_line.append(key)

        parser_keys = []
        for file_element in self.file_elements:
            for key, value in file_element.parser_data.items():
                parser_keys.append(key)

        parser_keys = list(set(parser_keys))
        csv_title_line += parser_keys

        for key, value in self.file_meta_data.items():
            csv_title_line.append(key)
        return csv_title_line, parser_keys

    def get_csv_lines(self, add_header=True):

        header = self.get_csv_header()
        if add_header:
            csv_lines = [header[0], ]
        else:
            csv_lines = []

        lines = self.get_text_lines()

        if len(lines) == 0:
            raise ValueError("No lines have been found in the file.")

        for line in lines:
            csv_line = [line.get_text(), self.file_path]
            for key, value in line.element_data.items():
                csv_line.append(value)

            for parser_val in header[1]:
                csv_line.append(line.parser_data.get(parser_val, ''))

            for key, value in self.file_meta_data.items():
                csv_line.append(value)
            csv_lines.append(csv_line)

        return csv_lines

    def get_json_objects(self):
        lines = self.get_text_lines()

        json_objects = []
        for line in lines:
            d_line = line.to_dict()
            if self.parser.get_config_value('export', 'add_meta_data', default=False):
                d_line['file_meta_data'] = self.file_meta_data
            json_objects.append(d_line)

        return json_objects

    def get_file_name(self, ftype='plain'):
        if ftype not in ['plain', 'csv', 'json']:
            raise ValueError("The given type is not valid.")

        print(os.path.split(self.file_path)[-1])

        if ftype == 'plain':
            return os.path.split(self.file_path)[-1]
        else:
            return os.path.split(self.file_path)[-1].split('.')[0] + '.' + ftype

    def __str__(self):
        """This function returns a string representation of the class."""
        return self.file_path


class AltoFileElement:

    text = ""
    original_text = ""
    element_data = {}
    meta_data = {}
    parser_data = {}

    def __init__(self, text):
        self.text = text
        self.original_text = text
        self.element_data = {}
        self.parser_data = {}

    def get_text(self):
        """This function returns the text of the element."""
        return self.text

    def set_text(self, text):
        """This function returns the text of the element."""
        self.text = text

    def to_dict(self):
        d = {'text': self.text}
        if self.text != self.original_text:
            d['original_text'] = self.original_text

        d['element_data'] = self.element_data
        if self.meta_data != {}:
            d['meta_data'] = self.meta_data
        if self.parser_data != {}:
            d['parser_data'] = self.parser_data

        return d

    def add_meta_data(self, key, value):
        """This function adds a key-value pair to the element_data dictionary."""
        self.meta_data[key] = value

    def set_attribute(self, key, value):
        """This function adds a key-value pair to the element_data dictionary."""
        self.element_data[key] = value

    def set_attributes(self, dict):
        """This function adds a key-value pair to the element_data dictionary."""
        self.element_data = dict

    def add_parser_data(self, key, value):
        """This function adds a key-value pair to the element_data dictionary."""
        self.parser_data[key] = value
