class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKBLUE = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class FileError(Exception):
    """
    A class to show errors in parts of a file.
    Here lines and columns are idexed by 1 to avoid confusion as
    it is common for text editors to index like this as well.
    """

    def __init__(self, filename, msg="", *, index=0):
        if filename:
            with open(self.filename, "r") as file:
                self.data = file.read()
        else:
            self.data = ""

        self.filename = filename
        self.msg = msg
        self.line, self.col = self._find_line_col(index)

    @classmethod
    def from_data(cls, data, msg="", *, index=0):
        error = cls(filename="", msg=msg)
        error.data = data
        error.line, error.col = error._find_line_col(index)
        return error

    def _find_line_col(self, index):
        last_newline = self.data[:index].rfind("\n")
        line = self.data[:index].count("\n") + 1
        col = index - last_newline
        return line, col

    def __str__(self):

        msg = 'File "{filename}", line {line}\n'
        msg += "{code}\n"
        msg += "{pointer}\n"
        msg += "{class_name}: {msg}"

        spaces = " " * (self.col - 1)
        pointer = spaces + "^"

        lines = self.data.splitlines()
        return msg.format(
            msg=self.msg,
            filename=self.filename,
            line=self.line,
            code=lines[self.line - 1].strip("\n"),
            class_name=self.__class__.__name__,
            pointer=pointer,
        )

        return msg


class LexicalError(FileError):
    pass


class SyntacticError(FileError):
    pass
