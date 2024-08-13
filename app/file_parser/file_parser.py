class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_file(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    def _parse_file(self):
        file_content = self._read_file()
        return file_content


class TextFileParser(FileParser):
    def _read_file(self):
        return super()._read_file()

    def _parse_file(self):
        return super()._parse_file()
