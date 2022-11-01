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

    def __init__(self, filename, msg="", *, line=1, col=1):
        self.filename = filename
        self.msg = msg
        self.line = line
        self.col = col
        self.data = ""

    @classmethod
    def from_data(cls, data, msg="", *, line=1, col=1):
        exp = cls(filename=None, msg=msg, line=line, col=col)
        exp.data = data
        return exp

    def __str__(self):
        if self.filename is None:
            lines = self.data.splitlines()
        else:
            with open(self.filename, "r") as file:
                lines = file.readlines()

        msg = 'File "{filename}", line {line}\n'
        msg += "{code}\n"
        msg += "{pointer}\n"
        msg += "{class_name}: {msg}"

        spaces = " " * (self.col - 1)
        pointer = spaces + "^"

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
