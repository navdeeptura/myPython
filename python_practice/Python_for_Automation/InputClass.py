
# setting NO_LIMIT to -1 as user may enter 0 if file save not needed
NO_LIMIT = -1

class FileReader:
    # Handles reading lines from a file

    def __init__(self, file_path):
        self.file_path = file_path

    def read_lines(self):
        """yield the lines one by one rather than entire file"""

        try:
            with open(self.file_path, "r") as file_reader:
                for line in file_reader:
                    yield line
        except FileNotFoundError:
            print (f"Error: File not found - '{self.file_path}'")


class FileWriter:
    """Handles writing to a file"""

    def __init__(self, file_path):
        self.file_path = file_path

    def write_lines(self, lines):
        with open(self.file_path, "w") as file_handle:
            for line in lines:
                file_handle.write(line)


class EntryFilter:
    """THis will be the pass/fail entry filter"""

    def is_pass_entry(self, entry):
        return entry == "P"


class InputFileProcessor:
    """Handle categorization of input file into pass and fail"""

    def __init__( self, input_file_reader, pass_file_writer, fail_file_writer,
                  entry_filter, max_entries = NO_LIMIT):
        self.input_file_reader = input_file_reader
        self.pass_file_writer = pass_file_writer
        self.fail_file_writer = fail_file_writer
        self.entry_filter = entry_filter
        self.max_entries = max_entries
        self.pass_counter = 0
        self.fail_counter = 0

    def process_input_data(self):
        """Process data from input file and stores in pass and fail file"""

        pass_lines = []
        fail_lines = []

        for line in self.input_file_reader.read_lines():
            line_split = line.split()

            # Skip lines with insufficient data (less than 3 words)
            if len(line_split) < 3:
                continue

            is_pass_entry = self.entry_filter.is_pass_entry(line_split[2])
            can_add_pass = self.max_entries == NO_LIMIT or self.pass_counter < self.max_entries
            can_add_fail = self.max_entries == NO_LIMIT or self.fail_counter < self.max_entries

            if is_pass_entry and can_add_pass:
                pass_lines.append(line)
                self.pass_counter += 1
            elif can_add_fail:
                fail_lines.append(line)
                self.fail_counter += 1

            # Write files to the file if length reaches 1000
            if len(pass_lines) >= 1000:
                self.pass_file_writer.write_lines(pass_lines)
                pass_lines.clear()

            if len(fail_lines) >= 1000:
                self.fail_file_writer.write_lines(fail_lines)
                fail_lines.clear()

        self.pass_file_writer.write_lines(pass_lines)
        self.fail_file_writer.write_lines(fail_lines)


class FileAnalyzer:
    """Analyze the argument file and prints its data as output"""

    def __init__(self, file_reader, max_entries = NO_LIMIT):
        self.file_reader = file_reader
        self.max_entries = max_entries
        self.print_counter = 0

    def print_file_content(self):
        """Print number of mentioned lines in the file, all lines if entry is Zero"""

        for line in self.file_reader.read_lines():
            can_print_lines = self.max_entries == NO_LIMIT or self.print_counter < self.max_entries
            if can_print_lines:
                print(line.strip())
                self.print_counter += 1


if __name__ == "__main__":
    input_file_reader = FileReader("Ex_Files/inputFile.txt")
    pass_file_writer = FileWriter("Ex_Files/passFile.txt")
    fail_file_writer = FileWriter("Ex_Files/failFile.txt")
    entry_filter = EntryFilter()
    input_file_processor = InputFileProcessor(
        input_file_reader,
        pass_file_writer,
        fail_file_writer,
        entry_filter,
        11
    )
    input_file_processor.process_input_data()

    pass_file_reader = FileReader("Ex_Files/passFile.txt")
    file_printer = FileAnalyzer(pass_file_reader, 0)
    file_printer.print_file_content()











