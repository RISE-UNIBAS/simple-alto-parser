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
                 'file_ending': '.alto',          # The file ending of the files to be parsed.
                 'meta_data': {                   # Metadata to be added to all the lines. Contains static information
                     'title': 'Some title',       # for all files. Any number of key-value pairs can be added.
                     'year': '1951'},
                 'file_name_structure': {         # A regex pattern that is used to extract metadata from the file name.
                        'pattern': r'bscc_(\d{4})',
                        'value_names': ['page',]},
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
alto_parser = AltoFileParser('assets/alto/a_batch', parser_config=parser_config)
alto_parser.parse()

pattern_parser = AltoPatternParser(alto_parser)
pattern_parser.find(r'˚|°').mark('is_member', True).remove()
pattern_parser.find(r'^ ').remove()
pattern_parser.find(r'^﻿').remove()
pattern_parser.find(r'^([0-9abc]+)\.').categorize('id').remove()
pattern_parser.find(r' (B\.? ?[0-9]{1,4}.*C.*)$').categorize('network').remove()
pattern_parser.find(r'\* (C [0-9, ]*)\.$').categorize('network').mark('network_c_only', True).remove()
pattern_parser.find(r'^(.*Ltd\.),').categorize('company').remove()
pattern_parser.find(r'([SWECN]{1,2} [0-9]{1,2})\.\s*$').categorize('address').remove()

dict_parser = AltoDictionaryParser(alto_parser)
dict_parser.load('assets/dicts/locations.json')
dict_parser.find().categorize().remove()

pattern_parser.find(r'^\s*\.\s*$').remove()
pattern_parser.find(r'^\s*$').remove()



"""
pattern_parser.categorize('company_name').remove()
pattern_parser.find(r'^, ?').remove()
pattern_parser.find(r'^([0-9]{1,3}[abc]?, [^,]*)').categorize('address').remove()
pattern_parser.find(r'^, ?').remove()
pattern_parser.find(r'\s*x(\s*)?$').remove()
pattern_parser.find(r'^(\w*( \(\w*\))?)\.\s*$').categorize('location').remove()
pattern_parser.find(r'^[A-Z]\w* \([\w.]*\)\.(\s*)?$').categorize('location').remove()
"""

"""nlp_parser = AltoNLPParser(alto_parser, "en_core_web_sm")
nlp_parser.parse('ORG')
"""

"""The parsed data can be exported to CSV or JSON files with the AltoFileExporter. Pass the parser object to the
constructor of the exporter."""

alto_exporter = AltoFileExporter(alto_parser)
alto_exporter.save_csv('output/export.tsv', delimiter='\t')
alto_exporter.save_json('output/export.json')
alto_exporter.save_csvs('output/csv/', delimiter='\t')
alto_exporter.save_jsons('output/json/')
