from simple_alto_parser import AltoTextParser

alto_parser = AltoTextParser()
alto_parser.add_files('assets/data', file_ending='.alto')
alto_parser.extract_meta_from_filenames('year', r'^(\d{4})')
alto_parser.extract_meta_from_filenames('page', r'_(\d{4})')
alto_parser.add_meta_data_to_files('title', 'Some title')
alto_parser.parse_text()

alto_parser.export_lines_to_csv('data_1923.tsv', delimiter='\t')
alto_parser.export_lines_to_json('data_1923.json')
result = alto_parser.get_alto_files()

# content_parser = AltoContentParser()
for file in result:
    print("Meta data", file.file_meta_data)
    lines = file.get_text_regions()
    for line in lines:
        print("Line", line)
