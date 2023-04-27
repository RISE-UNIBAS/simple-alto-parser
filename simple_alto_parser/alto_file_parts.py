
class AltoXMLElement:

    namespace = None
    raw_data = None
    element_data = None

    def __init__(self, xml_data, namespace):
        self.raw_data = xml_data
        self.namespace = namespace
        self.element_data = {}
        self.text = None
        self.attributes_to_get = ["id", "baseline", "hpos", "vpos", "width", "height"]

        self.read_attributes()

    def read_attributes(self):
        for attribute in self.attributes_to_get:
            try:
                self.element_data[attribute] = self.raw_data.attrib.get(attribute.upper())
            except KeyError:
                print("KeyError: " + attribute)


class TextRegion(AltoXMLElement):

    text_lines = []

    def __init__(self, text_region_data, namespace):
        super().__init__(text_region_data, namespace)
        self.text_lines = []

        for text_line in text_region_data.iterfind('.//{%s}TextLine' % namespace):
            self.add_text_line(text_line)

    def add_text_line(self, text_line_data):
        text_line_object = TextLine(text_line_data, self.namespace)
        self.text_lines.append(text_line_object)

    def get_text_lines(self):
        return self.text_lines

    def get_text(self):
        parts = []
        for text_line in self.text_lines:
            parts.append(text_line.get_text())
        return " ".join(parts)

    def __str__(self):
        return self.get_text()


class TextLine(AltoXMLElement):

    text = None

    def __init__(self, text_line_data, namespace):
        super().__init__(text_line_data, namespace)
        self.text = ""

        for text_bit in text_line_data.findall('{%s}String' % namespace):
            line_content = text_bit.attrib.get('CONTENT')
            self.text += " " + line_content

    def get_text(self):
        return self.text

    def __str__(self):
        return self.text
