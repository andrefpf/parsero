class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKBLUE = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class FileError(Exception):
    def __init__(self, filename, msg="", *, line=0, column=0):
        self.filename = filename
        self.msg = msg
        self.line = line
        self.column = column
    
    def _format_title(self):
        pass
    
    def _format_line(self, text, line_number):
        pass

    def __str__(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()

        msg = "File \"{filename}\", line {line}\n"\
              "{line}\n" \
              "{pointer}\n" \
              "{class}: {msg}" 
        
        # msg = f"File \"{self.filename}\", line {self.line}\n"
        # msg += lines[self.line-1]
        # msg += " " * (self.column - 1) + "^\n"
        # msg += f"{self.__class__.__name__}: {self.msg}"

        # msg = bcolors.BOLD + f"Error on file {bcolors.UNDERLINE}{self.filename}{bcolors.ENDC}\n"

        # for i in range(self.line-2, self.line):
        #     msg += f"{bcolors.OKBLUE}{i} |{bcolors.ENDC} {lines[i-1]}"

        # msg += f"{bcolors.OKBLUE}{self.line} |{bcolors.ENDC} {bcolors.FAIL}{lines[self.line-1]}{bcolors.ENDC}"
        # msg += bcolors.OKBLUE + " " * (5 + self.column - 1) + "^\n" + bcolors.ENDC

        # for i in range(self.line+1, self.line+3):
        #     msg += f"{bcolors.OKBLUE}{i} |{bcolors.ENDC} {lines[i-1]}"

        return msg

class LexicalError(FileError):
    pass

class SyntacticError(FileError):
    pass

if __name__ == "__main__": 
    print(SyntacticError("../README.md", msg="Unexpected char \"&\"", line=22, column=11))
