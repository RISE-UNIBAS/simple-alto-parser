# simple-alto-parser
This is a simple parser for ALTO XML files. It is designed to do two tasks separately:
1. Extract the text from the ALTO XML file with the AltoTextParser class.
2. Extract structured information from the text with different parsing methods.

## Usage
```python
from simple_alto_parser import AltoFileParser, AltoPatternParser, AltoFileExporter

# Create a parser instance and supply your data directory
alto_parser = AltoFileParser('data')
alto_parser.parse()

# Find and categorize by patterns
pattern_parser = AltoPatternParser(alto_parser)
pattern_parser.find(r'(^.*\& Cie\.$)').categorize('company_name').remove()

# Other options are: look up in dictionaries, perform spacy NER

# Export the data
alto_exporter = AltoFileExporter(alto_parser)
alto_exporter.save_csv('output/alto_test.csv', delimiter=',')
```
