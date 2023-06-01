import csv
import json
import os


class AltoFileExporter:

    file_parser = None
    files = []

    def __init__(self, alto_file_parser):
        self.file_parser = alto_file_parser
        self.files = alto_file_parser.get_alto_files()

    def get_combined_csv_header(self):
        total_header = []
        for file in self.files:
            f_header = file.get_csv_header()
            for header in f_header:
                if header not in total_header:
                    total_header.append(header)
        return total_header

    def save_csv(self, file_name, **kwargs):
        self.assure_is_file(file_name)

        file_idx = 0
        csv_lines = [self.get_combined_csv_header(), ]
        for file in self.files:
            csv_lines.extend(file.get_csv_lines(add_header=False))
            file_idx += 1

        self.save_to_csv(file_name, csv_lines, **kwargs)

    def save_csvs(self, directory_name, **kwargs):
        self.assure_is_dir(directory_name)

        for file in self.files:
            if file.has_lines():
                csv_lines = file.get_csv_lines(add_header=True)
                file_name = os.path.join(directory_name, file.get_file_name(ftype='csv'))
                self.save_to_csv(file_name, csv_lines, **kwargs)
            else:
                pass

    def save_json(self, file_name):
        self.assure_is_file(file_name)

        json_objects = []
        for file in self.files:
            json_objects.extend(file.get_json_objects())

        with open(file_name, 'w', encoding='utf-8') as outfile:
            json.dump(json_objects, outfile, indent=4, sort_keys=True)

    def save_jsons(self, directory_name):
        self.assure_is_dir(directory_name)

        for file in self.files:
            if file.has_lines():
                json_objects = file.get_json_objects()
                file_name = os.path.join(directory_name, file.get_file_name(ftype='json'))

                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(json_objects, f, indent=4, sort_keys=True)
            else:
                pass

    @staticmethod
    def assure_is_file(file_path):
        """Assure that the given path is a file."""
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            return

        if not os.path.isfile(file_path):
            raise ValueError("The given path is not a file.")

    @staticmethod
    def assure_is_dir(file_path):
        """Assure that the given path is a directory."""

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if not os.path.isdir(file_path):
            raise ValueError("The given path is not a directory.")

    @staticmethod
    def save_to_csv(file_path, csv_lines, **kwargs):
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=kwargs.get('delimiter', '\t'),
                                    quotechar=kwargs.get('quotechar', '"'),
                                    quoting=kwargs.get('quoting', csv.QUOTE_MINIMAL))
            for line in csv_lines:
                csv_writer.writerow(line)
