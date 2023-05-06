"""This file contains the classes that represent the different parts of an ALTO file. The AltoFile class uses these
classes to store the data of an ALTO file."""
from abc import ABC, abstractmethod


class AltoXMLElement(ABC):
    """This class represents an element of an ALTO file. It is used to store the data of an element. It is an abstract
    class and should not be used directly."""

    namespace = None
    raw_data = None
    element_data = None

    attributes_to_get = ["id", "baseline", "hpos", "vpos", "width", "height"]
    """A list of the attributes that should be stored in the element_data dictionary."""

    def __init__(self, xml_data, namespace):
        """The constructor of the class. It takes the xml data of the element and the namespace of the file as
        parameters."""

        self.raw_data = xml_data
        self.namespace = namespace
        self.element_data = {}
        self.text = None
        self.read_attributes()

    def read_attributes(self):
        """This function reads the attributes of the element and stores them in the element_data dictionary."""
        for attribute in self.attributes_to_get:
            try:
                self.element_data[attribute] = self.raw_data.attrib.get(attribute.upper())
            except KeyError:
                # The attribute is not in the element. This is not a problem.
                pass

    def sanitize_text(self):
        """This function removes all line breaks, tabs and carriage returns from the text and removes leading and
        trailing whitespaces."""
        self.text = self.text.replace("\n", "").replace("\r", "").replace("\t", "").strip()

    @abstractmethod
    def to_dict(self):
        """This function returns the data of the element as a dictionary.
        It should be implemented in the subclasses."""
        pass

    @abstractmethod
    def get_text(self):
        """This function returns the text of the element.
        It should be implemented in the subclasses."""
        pass


class TextRegion(AltoXMLElement):
    """This class represents a text region of an ALTO file. It is used to store the data of a text region. It is a
    subclass of the AltoXMLElement class."""

    text_lines = []

    def __init__(self, text_region_data, namespace):
        """The constructor of the class. It takes the xml data of the text region and the namespace of the file as
        parameters."""

        super().__init__(text_region_data, namespace)
        self.text_lines = []

        for text_line in text_region_data.iterfind('.//{%s}TextLine' % namespace):
            self.add_text_line(text_line)

    def add_text_line(self, text_line_data):
        """This function adds a text line to the text region. It takes the xml data of the text line as a parameter."""

        text_line_object = TextLine(text_line_data, self.namespace)
        self.text_lines.append(text_line_object)

    def get_text_lines(self):
        """This function returns the text lines of the text region."""

        return self.text_lines

    def get_text(self):
        """This function returns the text of the text region. This means that it returns the text of all text lines
        of the text region."""

        parts = []
        for text_line in self.text_lines:
            parts.append(text_line.get_text())
        self.text = " ".join(parts)
        self.sanitize_text()
        return self.text

    def to_dict(self):
        """This function returns the data of the text region as a dictionary."""

        dict_object = {
            'type': 'text_region',
            'text': self.get_text(),
            'text_lines': []
        }

        # Add the attributes of the text region to the dictionary.
        for key, value in self.element_data.items():
            dict_object[key] = value

        # Add the text lines of the text region to the dictionary.
        for text_line in self.text_lines:
            dict_object['text_lines'].append(text_line.to_dict())

        return dict_object

    def __str__(self):
        """This function returns the text of the text region."""

        return self.get_text()


class TextLine(AltoXMLElement):
    """This class represents a text line of an ALTO file. It is used to store the data of a text line. It is a
    subclass of the AltoXMLElement class."""

    text = None

    def __init__(self, text_line_data, namespace):
        """The constructor of the class. It takes the xml data of the text line and the namespace of the file as
        parameters."""

        super().__init__(text_line_data, namespace)
        self.text = ""

        for text_bit in text_line_data.findall('{%s}String' % namespace):
            line_content = text_bit.attrib.get('CONTENT')
            self.text += " " + line_content
        self.sanitize_text()

    def get_text(self):
        """This function returns the text of the text line."""

        return self.text

    def to_dict(self):
        """This function returns the data of the text line as a dictionary."""

        dict_object = {
            'type': 'text_line',
            'text': self.get_text()
        }

        # Add the attributes of the text line to the dictionary.
        for key, value in self.element_data.items():
            dict_object[key] = value

        return dict_object

    def __str__(self):
        """This function returns the text of the text line."""

        return self.text
