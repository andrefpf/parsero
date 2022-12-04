class FileError(Exception):
    """
    A class to show errors in parts of a file.
    Here lines and columns are idexed by 1 to avoid confusion as
    it is common for text editors to index like this as well.
    """

    def __init__(self, filename, msg="", *, index=0, index_end=0):
        if filename:
            with open(filename, "r") as file:
                self.data = file.read()
        else:
            self.data = ""

        self.filename = filename
        self.msg = msg
        self.index = index
        self.index_end = index_end

    @classmethod
    def from_data(cls, data, msg="", *, index=0, index_end=0):
        error = cls(filename="", msg=msg, index=index, index_end=index_end)
        error.data = data
        return error

    def _find_line_col(self, index):
        last_newline = self.data[:index].rfind("\n")
        line = self.data[:index].count("\n")
        col = index - last_newline
        return line, col

    def __str__(self):
        msg = 'File "{filename}", line {line}\n'
        msg += "{code}\n"
        msg += "{pointer}\n"
        msg += "{class_name}: {msg}"

        line, col = self._find_line_col(self.index)
        _, col_end = self._find_line_col(self.index_end)

        if col_end <= col:
            col_end = col + 1

        spaces = " " * (col - 1)
        pointer = spaces + "^" * (col_end - col)

        lines = self.data.splitlines()
        return msg.format(
            msg=self.msg,
            filename=self.filename,
            line=line,
            code=lines[line].strip("\n"),
            class_name=self.__class__.__name__,
            pointer=pointer,
        )

        return msg


class LexicalError(FileError):
    pass


class SyntacticError(FileError):
    pass
