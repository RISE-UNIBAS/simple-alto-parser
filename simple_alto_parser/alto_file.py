"""This module contains the AltoFile class. It is used to parse an alto file and to store the data in a structured
way. The class is used by the AltoTextParser class."""
import csv
import json
import os.path
import xml.etree.ElementTree as ETree

from simple_alto_parser.alto_file_parts import TextRegion


class AltoFile:
    """This class represents an alto file. It is used to parse an alto file and to store the data.
    The class stores text regions which store text lines."""

    file_path = None
    """The path to the file."""

    text_regions = []
    """A list of the text regions in the alto file."""

    def __init__(self, file_path):
        """The constructor of the class. It takes the path to the file as a parameter."""

        if not os.path.isfile(file_path):
            raise ValueError("The given path is not a file.")
        self.file_path = file_path
        self.file_meta_data = {}

    def parse_text(self):
        """This function parses the alto file and stores the data in the class."""

        xml_tree, xmlns = self._xml_parse_file()
        if xml_tree is None:
            raise ValueError("The given file is not a valid xml file.")

        for text_region in xml_tree.iterfind('.//{%s}TextBlock' % xmlns):
            text_region_object = TextRegion(text_region, xmlns)
            self.text_regions.append(text_region_object)

    def _xml_parse_file(self):
        """ This function uses the Etree xml parser to parse an alto file. It should not be called from outside this
            class. The parse_file() method calls it."""

        namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                     'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                     'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                     'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#'}

        try:
            xml_tree = ETree.parse(self.file_path)
        except ETree.ParseError as error:
            raise error

        if 'http://' in str(xml_tree.getroot().tag.split('}')[0].strip('{')):
            xmlns = xml_tree.getroot().tag.split('}')[0].strip('{')
        else:
            try:
                ns = xml_tree.getroot().attrib
                xmlns = str(ns).split(' ')[1].strip('}').strip("'")
            except IndexError as error:
                raise error

        if xmlns not in namespace.values():
            raise IndexError('No valid namespace has been found.')

        return xml_tree, xmlns

    def get_text_regions(self) -> list:
        """This function returns the text regions of the alto file."""

        return self.text_regions

    def get_text_lines(self):
        """This function returns the text lines of the alto file. It iterates over the text regions and calls the
        get_text_lines() function of the text regions."""

        text_lines = []
        for text_region in self.text_regions:
            text_lines.extend(text_region.get_text_lines())
        return text_lines

    def add_file_meta_data(self, parameter_name, parameter_value):
        """This function adds metadata to the file. It takes the parameter name and the parameter value as parameters.
        The parameter name should be a string and the parameter value can be any type."""
        self.file_meta_data[parameter_name] = parameter_value

    def export_to_csv(self, file_path, line_type, **kwargs):
        """This function exports the data of the alto file to a csv file. It takes the file path and the line type as
        parameters. The line type should be either 'text_line' or 'text_region'. The function also takes optional
        parameters for the csv writer. These are delimiter, quotechar and quoting. The default values are '\t', '"' and
        csv.QUOTE_MINIMAL. The function raises a ValueError if the line type is not valid or if no lines have been
        found in the file."""

        if line_type not in ['text_line', 'text_region']:
            raise ValueError("The given line type is not valid.")

        if line_type == 'text_line':
            lines = self.get_text_lines()
        else:
            lines = self.get_text_regions()

        if len(lines) == 0:
            raise ValueError("No lines have been found in the file.")

        csv_lines = []
        csv_title_line = ['text', 'type']
        for key, value in lines[0].element_data.items():
            csv_title_line.append(key)

        for line in lines:
            csv_line = [line.get_text(), line_type]
            for key, value in line.element_data.items():
                csv_line.append(value)
            csv_lines.append(csv_line)

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=kwargs.get('delimiter', '\t'), quotechar=kwargs.get('quotechar', '"'),
                                    quoting=kwargs.get('quoting', csv.QUOTE_MINIMAL))
            csv_writer.writerow(csv_title_line)
            for line in csv_lines:
                csv_writer.writerow(line)

    def export_to_json(self, file_path, line_type):
        """This function exports the data of the alto file to a json file. It takes the file path and the line type as
        parameters. The line type should be either 'text_line' or 'text_region'. The function raises a ValueError if
        the line type is not valid."""

        if line_type not in ['text_line', 'text_region']:
            raise ValueError("The given line type is not valid.")

        if line_type == 'text_line':
            lines = self.get_text_lines()
        else:
            lines = self.get_text_regions()

        json_objects = []
        for line in lines:
            json_objects.append(line.to_dict())

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_objects, f, indent=4, sort_keys=True)

    def __str__(self):
        """This function returns a string representation of the class."""
        return self.file_path
