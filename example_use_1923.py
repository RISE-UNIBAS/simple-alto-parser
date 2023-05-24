from simple_alto_parser import AltoFileParser, AltoPatternParser, AltoFileExporter, AltoNLPParser
from simple_alto_parser.dictionary_parser import AltoDictionaryParser

"""The parser can be configured. The following options are available:
    - line_type: Defines what constitutes a line for the parser. Can be either 'TextLine' or 'TextBlock'.
    - file_ending: The file ending of the files to be parsed.
    - meta_data: Metadata to be added to all the lines. Contains static information for all files. 
                 Any number of key-value pairs can be added.
    - file_name_structure: A regex pattern that is used to extract metadata from the file name.
    - export: Options for exporting the parsed data.
    """

parser_config = {'line_type': 'TextBlock',        # TextLine, TextBlock. Defines what constitutes a line for the parser.
                 'file_ending': '.xml',          # The file ending of the files to be parsed.
                 'meta_data': {                   # Metadata to be added to all the lines. Contains static information
                     'title': 'Some title'
                 },
                 'file_name_structure': {         # A regex pattern that is used to extract metadata from the file name.
                        'pattern': r'(\d{4})_(\d{4})',
                        'value_names': ['year', 'page']},
                 'export': {                            # Options for exporting the parsed data.
                        'csv': {
                            'print_manipulated': True,      # Print the manipulated text to the csv.
                            'print_filename': True,         # Print the filename to the csv.
                            'print_attributes': True,       # Print the attributes to the csv.
                            'print_parser_results': True,   # Print the parser results to the csv.
                            'print_file_meta_data': True,   # Print the file meta data to the csv.
                        }
                    }
                 }

"""The parser can be initialized with a directory path. All files in the directory with the given file ending will
be added to the list of files to be parsed. Alternatively, files can be added individually with the add_file() method.
"""
alto_parser = AltoFileParser('assets/alto/data_1923_test', parser_config=parser_config)
alto_parser.parse()

pattern_parser = AltoPatternParser(alto_parser)
pattern_parser.find(r'^([A-Z].* & Co\., A\.-G\.)').categorize('company').remove()
pattern_parser.find(r'(([A-Z]).* (& Co\.|Ltd\.|AG.\|Cie\.|A\.-G\.|S\. A\.))').categorize('company').remove()
pattern_parser.find(r'([A-Z].* Co\.)').categorize('company').remove()
#pattern_parser.find(r'([0-9]{1,3}, [A-Z].*(strasse|platz))').categorize('address').remove()

dictionary_parser = AltoDictionaryParser(alto_parser)
dictionary_parser.load('assets/dicts/titles.json')
dictionary_parser.load('assets/dicts/locations.json')
dictionary_parser.find(strict=False, restrict_to="location").categorize().remove()
dictionary_parser.find(restrict_to="title").categorize().remove()

pattern_parser.find(r'^[., ].*$').remove()

"""alto_parser.print_absent("present")
alto_parser.print_absent("company")"""

alto_exporter = AltoFileExporter(alto_parser)
alto_exporter.save_csv('output/export.tsv', delimiter='\t')
alto_exporter.save_json('output/export.json')
alto_exporter.save_csvs('output/csv/', delimiter='\t')
alto_exporter.save_jsons('output/json/')
