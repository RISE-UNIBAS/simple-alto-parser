import json
import re

from simple_alto_parser import BaseParser
from simple_alto_parser.base_parser import ParserMatch


class AltoDictionaryParser(BaseParser):

    dictionaries = []

    def __init__(self, parser):
        """The constructor of the class. It initializes the list of files.
        The lines are a list of AltoXMLElement objects."""
        super().__init__(parser)

    def load(self, dictionary_file):
        dictionary = json.load(open(dictionary_file))
        self.dictionaries.append(dictionary)

    def find(self, strict=True):
        """Find a pattern in the text lines."""
        self.clear()
        file_id = 0
        for file in self.parser.get_alto_files():
            line_id = 0
            for line in file.get_text_lines():
                for dictionary in self.dictionaries:
                    for entry in dictionary:
                        if strict:
                            match = entry['entry'].strip('.').lower() == line.get_text().strip().strip('.').lower()
                            if match:
                                match = entry['entry']
                        else:
                            match = re.search(entry['entry'], line.get_text().strip())
                        if match:
                            self.matches.append(DictionaryMatch(file_id, line_id, match, entry))
                line_id += 1
            file_id += 1
        return self

    def categorize(self):
        """Add the given category to all matches."""
        for match in self.matches:
            category = match.dict_entry['type']
            if type(match.match) == str:
                match_text = match.match
            else:
                match_text = match.match.group(0)
            self.parser.get_alto_files()[match.file_id].get_text_lines()[match.line_id].add_parser_data(category, match_text)
        return self

    def remove(self, replacement=''):
        """Remove all matched patterns from matching lines."""
        for match in self.matches:
            if type(match.match) == str:
                new_text = self.parser.get_alto_files()[match.file_id].get_text_lines()[match.line_id].get_text().replace(match.match, replacement)
            else:
                new_text = re.sub(match.match,
                                  replacement,
                                  self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].get_text())

            self.parser.get_alto_files()[match.file_id].get_text_lines()[match.line_id].set_text(new_text)
        return self

    def replace(self, replacement):
        self.remove(replacement)
        return self


class DictionaryMatch(ParserMatch):

    dict_entry = {}

    def __init__(self, file_id, line_id, match, dict_entry={}):
        super().__init__(file_id, line_id, match)
        self.dict_entry = dict_entry

    def __str__(self):
        return super().__str__()
        # return self.match.group(0)
