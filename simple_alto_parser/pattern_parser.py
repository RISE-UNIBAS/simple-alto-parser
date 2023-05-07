import re


class AltoPatternParser:

    matches = []

    def __init__(self, parser):
        """The constructor of the class. It initializes the list of files.
        The lines are a list of AltoXMLElement objects."""
        self.parser = parser
        self.matches = []

    def find(self, pattern):
        """Find a pattern in the text lines."""
        self.clear()

        fidx = 0
        for file in self.parser.get_alto_files():
            lidx = 0
            for line in file.get_text_lines():
                match = re.search(pattern, line.get_text())
                if match:
                    self.matches.append(PatternMatch(pattern, (fidx, lidx), match))
                lidx += 1
            fidx += 1

        return self

    def categorize(self, category):
        """Add the given category to all matches."""
        for match in self.matches:
            self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].add_parser_data(category, match.match.group(1))
        return self

    def mark(self, name, value):
        """Add the given category to all matches."""
        for match in self.matches:
            self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].add_parser_data(name, value)
        return self

    def remove(self):
        """Remove all matched patterns from matching lines."""
        for match in self.matches:
            self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].set_text(
                re.sub(match.pattern, '',
                       self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].get_text()))
        return self

    def clear(self):
        self.matches = []
        return self

    def print_matches(self):
        """Print all matches."""
        for match in self.matches:
            print("Found pattern '%s' in line '%s'." %
                  (match.pattern, self.parser.get_alto_files()[match.fidx].get_text_lines()[match.lidx].get_text()))
        return self


class PatternMatch:

    def __init__(self, pattern, line_id, match):
        self.pattern = pattern
        self.line_id = line_id
        self.fidx = line_id[0]
        self.lidx = line_id[1]
        self.match = match
