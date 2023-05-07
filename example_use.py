from simple_alto_parser import AltoFileParser, AltoPatternParser, AltoFileExporter

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
                        'pattern': r'bscc_(\d{4})_([a-z0-9]*)',
                        'value_names': ['page', 'id']},
                 'export': {                      # Options for exporting the parsed data.
                        'add_meta_data': True,    # Add the file metadata to the exported data.
                    }
                 }

"""The parser can be initialized with a directory path. All files in the directory with the given file ending will
be added to the list of files to be parsed. Alternatively, files can be added individually with the add_file() method.
"""
alto_parser = AltoFileParser('assets/alto', parser_config=parser_config)
alto_parser.parse()

pattern_parser = AltoPatternParser(alto_parser)
pattern_parser.find(r'(˚|°) ?').mark('member', True).remove()
pattern_parser.find('﻿').remove()
pattern_parser.find(r'^(\d{1,3})\.').categorize('id').remove()
pattern_parser.print_matches()

"""The parsed data can be exported to CSV or JSON files with the AltoFileExporter. Pass the parser object to the
constructor of the exporter."""
alto_exporter = AltoFileExporter(alto_parser)
alto_exporter.save_csv('output/export.tsv', delimiter='\t')
alto_exporter.save_json('output/export.json')
alto_exporter.save_csvs('output/csv/', delimiter='\t')
alto_exporter.save_jsons('output/json/')