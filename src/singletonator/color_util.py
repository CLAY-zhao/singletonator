import sys


class COLOR(object):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'

    @staticmethod
    def black(text: str) -> None:
        print(set_color(text, COLOR.BLACK))


    @staticmethod
    def red(text: str) -> None:
        print(set_color(text, COLOR.RED))


    @staticmethod
    def green(text: str) -> None:
        print(set_color(text, COLOR.GREEN))


    @staticmethod
    def yellow(text: str) -> None:
        print(set_color(text, COLOR.YELLOW))


    @staticmethod
    def blue(text: str) -> None:
        print(set_color(text, COLOR.BLUE))


    @staticmethod
    def magenta(text: str) -> None:
        print(set_color(text, COLOR.MAGENTA))


    @staticmethod
    def cyan(text: str) -> None:
        print(set_color(text, COLOR.CYAN))


    @staticmethod
    def white(text: str) -> None:
        print(set_color(text, COLOR.WHITE))


color_support = True


if sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127/...
        # how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
        from ctypes import windll
        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        color_support = False


def set_color(text: str, color: str) -> str:
    if color_support:
        return f"{color}{text}{COLOR.DEFAULT}"
    return f"{text}"  # pragma: no cover



