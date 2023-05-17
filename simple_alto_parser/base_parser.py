class BaseParser:

    matches = []

    def __init__(self, parser):
        """The constructor of the class. It initializes the list of files.
        The lines are a list of AltoXMLElement objects."""
        self.parser = parser
        self.matches = []

    def mark(self, name, value):
        """Add the given category to all matches."""
        for match in self.matches:
            self.parser.get_alto_files()[match.file_id].get_text_lines()[match.line_id].add_parser_data(name, value)
        return self

    def clear(self):
        self.matches = []
        return self

    def print_matches(self):
        """Print all matches."""
        for match in self.matches:
            print("Found pattern '%s' in line '%s'." %
                  (match,
                   self.parser.get_alto_files()[match.file_id].get_text_lines()[match.line_id].get_text()))
        return self

    def get_unmatched(self):
        """Return all unmatched lines."""
        match_ids = []
        for match in self.matches:
            match_ids.append((match.file_id, match.line_id))

        unmatched = []
        file_id = 0
        for file in self.parser.get_alto_files():
            line_id = 0
            for line in file.get_text_lines():
                if (file_id, line_id) not in match_ids:
                    unmatched.append(line.get_text())
                line_id += 1
            file_id += 1
        return unmatched


class ParserMatch:

    def __init__(self, file_id, line_id, match):
        self.file_id = file_id
        self.line_id = line_id
        self.match = match
