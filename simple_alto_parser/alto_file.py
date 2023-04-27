import csv
import os.path
import xml.etree.ElementTree as ETree

from updated_alto_parser.alto_file_parts import TextRegion


class AltoFile:

    file_path = None
    text_regions = []

    def __init__(self, file_path):
        if not os.path.isfile(file_path):
            raise ValueError("The given path is not a file.")
        self.file_path = file_path
        self.file_meta_data = {}

    def parse_text(self):
        xml_tree, xmlns = self.xml_parse_file()
        if xml_tree is None:
            raise ValueError("The given file is not a valid xml file.")

        for text_region in xml_tree.iterfind('.//{%s}TextBlock' % xmlns):
            text_region_object = TextRegion(text_region, xmlns)
            self.text_regions.append(text_region_object)

    def xml_parse_file(self):
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

    def get_text_regions(self):
        return self.text_regions

    def get_text_lines(self):
        text_lines = []
        for text_region in self.text_regions:
            text_lines.extend(text_region.get_text_lines())
        return text_lines

    def add_file_meta_data(self, parameter_name, parameter_value):
        self.file_meta_data[parameter_name] = parameter_value

    def export_to_csv(self, file_path, line_type):
        if line_type not in ['text_line', 'text_region']:
            raise ValueError("The given line type is not valid.")

        if line_type == 'text_line':
            lines = self.get_text_lines()
        else:
            lines = self.get_text_regions()

        if len(lines) == 0:
            raise ValueError("No lines have been found in the file.")

        csv_lines = []
        csv_title_line = ['text', ]
        for key, value in lines[0].element_data.items():
            csv_title_line.append(key)

        for line in lines:
            csv_line = [line.get_text()]
            for key, value in line.element_data.items():
                csv_line.append(value)
            csv_lines.append(csv_line)

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter='\t')
            for line in csv_lines:
                csv_writer.writerow(line)

    def export_to_json(self, file_path, line_type):
        if line_type not in ['text_line', 'text_region']:
            raise ValueError("The given line type is not valid.")

        if line_type == 'text_line':
            lines = self.get_text_lines()
        else:
            lines = self.get_text_regions()

        with open(file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(str(line) + '\n')

    def __str__(self):
        return self.file_path
