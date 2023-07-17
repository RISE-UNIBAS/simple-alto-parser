"""This module contains the class AltoTextParser, which is used to parse text from ALTO files."""
import logging
import os
import re
import sys
import xml.etree.ElementTree as ETree
from simple_alto_parser.alto_file import AltoFile, AltoFileElement
from simple_alto_parser.utils import get_logger


class AltoFileParser:
    """This class is used to parse text from ALTO files. It stores the files in a list of AltoFile objects."""

    logger = None
    """The logger of the class."""

    LINE_TYPES = ['TextLine', 'TextBlock']

    attributes_to_get = ["id", "baseline", "hpos", "vpos", "width", "height"]
    """A list of the attributes that should be stored in the element_data dictionary."""

    files = []

    def __init__(self, directory_path=None, parser_config=None):
        """The constructor of the class."""

        self.parser_config = {
            'line_type': 'TextLine',
            'file_ending': '.xml',
            'export': {                            # Options for exporting the parsed data.
                'csv': {
                    'print_manipulated': False,      # Print the manipulated text to the csv.
                    'print_filename': False,         # Print the filename to the csv.
                    'print_attributes': True,       # Print the attributes to the csv.
                    'print_parser_results': True,   # Print the parser results to the csv.
                    'print_file_meta_data': False,   # Print the file meta data to the csv.
                }
            },
            'batches': [],
            'logging': {
                'level': logging.DEBUG,
            }
        }

        if parser_config:
            self.parser_config.update(parser_config)

        self.logger = get_logger(self.parser_config['logging']['level'])

        self.logger.debug("Parser config: %s", self.parser_config)

        if directory_path:
            self.add_files(directory_path, self.get_config_value('file_ending'))
        else:
            self.files = []

        if 'meta_data' in self.parser_config:
            for key, value in self.parser_config['meta_data'].items():
                self.add_meta_data_to_files(key, value)

        if 'file_name_structure' in self.parser_config:
            for file in self.files:
                match = re.search(self.parser_config['file_name_structure']["pattern"],
                                  os.path.basename(file.file_path))

                if match and len(match.groups()) == len(self.parser_config['file_name_structure']['value_names']):
                    idx = 1
                    for value_name in self.parser_config['file_name_structure']['value_names']:
                        file.add_file_meta_data(value_name, match.group(idx))
                        idx += 1
                else:
                    self.logger.warning("The file name structure does not match the file name of the file '%s'.",
                                        file.file_path)

    def add_files(self, directory_path, file_ending='.xml'):
        """Add all files with the given file ending in the given directory to the list of files to be parsed."""

        if not os.path.isdir(directory_path):
            self.logger.error("The given path is not a directory.")
            sys.exit()

        for file in os.listdir(directory_path):
            if file.endswith(file_ending):
                self.add_file(os.path.join(directory_path, file))
        self.logger.info("Added %s files to the list of files to be parsed.", len(self.files))

    def add_file(self, file_path):
        """Add the given file to the list of files to be parsed."""

        alto_file = AltoFile(file_path, self)
        self.files.append(alto_file)
        self.logger.debug("Added file '%s' to the list of files to be parsed.", file_path)

    def parse(self):
        """Parse the text from all files in the list of files."""

        for alto_file in self.files:
            self.parse_file(alto_file)
        self.logger.info(f"Parsed text from {len(self.files)} files.")

    def parse_part(self, parsing_function, name, pages):
        page_list = self.get_page_list(pages)
        executed_pages = []

        for alto_file in self.files:
            for line in alto_file.get_text_lines():
                current_page = int(alto_file.file_meta_data['page'])
                if current_page in page_list:
                    parsing_function(self)
                    executed_pages.append(current_page)

        items_to_remove = set(executed_pages)
        remaining = list(filter(lambda x: x not in items_to_remove, page_list))

        if len(remaining) > 0:
            self.logger.warning(f"Could not parse '{name}' pages {remaining}.")




    def parse_file(self, alto_file):
        """This function parses the alto file and stores the data in the class."""

        xml_tree, xmlns = self._xml_parse_file(alto_file.file_path)
        if xml_tree is None:
            raise ValueError("The given file is not a valid xml file.")

        for text_block in xml_tree.iterfind('.//{%s}TextBlock' % xmlns):
            block_content = ""
            for text_line in text_block.iterfind('.//{%s}TextLine' % xmlns):
                line_content = ""
                for text_bit in text_line.findall('{%s}String' % xmlns):
                    bit_content = text_bit.attrib.get('CONTENT')
                    line_content += " " + bit_content

                if self.get_config_value('line_type') == 'TextLine':
                    element = AltoFileElement(self.sanitize_text(line_content))
                    element.set_attributes(self.get_attributes(text_line))
                    alto_file.file_elements.append(element)

                block_content += " " + line_content

            if self.get_config_value('line_type') == 'TextBlock':
                element = AltoFileElement(self.sanitize_text(block_content))
                element.set_attributes(self.get_attributes(text_block))
                alto_file.file_elements.append(element)

    def _xml_parse_file(self, file_path):
        """ This function uses the Etree xml parser to parse an alto file. It should not be called from outside this
            class. The parse_file() method calls it."""

        namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                     'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                     'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                     'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#'}

        try:
            xml_tree = ETree.parse(file_path)
        except ETree.ParseError as error:
            raise error

        if 'http://' in str(xml_tree.getroot().tag.split('}')[0].strip('{')):
            xmlns = xml_tree.getroot().tag.split('}')[0].strip('{')
        else:
            try:
                ns = xml_tree.getroot().attrib
                xmlns = str(ns).split(' ')[1].strip('}').strip("'")
            except IndexError as error:
                xmlns = ''
                self.logger.error(f"The given file '{file_path}' is not a valid alto file. {error}")
                sys.exit()

        if xmlns not in namespace.values():
            self.logger.error(f"The given file '{file_path}' is not a valid alto file.")
            sys.exit()

        return xml_tree, xmlns

    def get_alto_files(self):
        """Return the list of AltoFile objects."""
        return self.files

    def get_attributes(self, element):
        """This function reads the attributes of the element and stores them in the element_data dictionary."""
        attrs = {}
        for attribute in self.attributes_to_get:
            try:
                attrs[attribute] = element.attrib.get(attribute.upper())
            except KeyError:
                # The attribute is not in the element. This is not a problem.
                self.logger.debug(f"The attribute '%s' is not in the element.", attribute)
                pass
        return attrs

    @staticmethod
    def sanitize_text(text):
        """This function removes all line breaks, tabs and carriage returns from the text and removes leading and
        trailing whitespaces."""
        return text.replace("\n", "").replace("\r", "").replace("\t", "").strip()

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

    def get_config_value(self, *args, default=None):
        """Return the value of the given parameter from the parser config."""
        data = self.parser_config
        for key in args:
            if isinstance(data, dict):
                data = data.get(key, default)
            elif isinstance(data, (list, tuple)) and isinstance(key, int):
                try:
                    data = data[key]
                except IndexError:
                    return default
            else:
                return default
        return data
