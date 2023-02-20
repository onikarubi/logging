class FileManager:
    def __init__(self, file) -> None:
        self.file = file

    def read_file(self):
        with open(self.file, 'r') as f:
            read_file = f.read()

        return read_file

