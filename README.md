# simple-alto-parser
This is a simple parser for ALTO XML files. It is designed to do two tasks separately:
1. Extract the text from the ALTO XML file with the AltoTextParser class.
2. Extract structured information from the text with different parsing methods.

## Usage
```python
from simple_alto_parser import AltoTextParser

alto_parser = AltoTextParser()
alto_parser.add_file('path/to/alto.xml')
alto_parser.parse_text()

result = alto_parser.get_alto_files()
regions = result[0].get_text_regions()
lines = regions[0].get_text_lines()
```
