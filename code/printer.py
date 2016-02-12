class Printer:
    """
    Simple printer class that provides static methods for printing text to STDOUT.
    """


    def __init__(self):
        pass

    @staticmethod
    def pp(text, char='*', length=75):
        print(char*length)
        print(text)
        print(char*length)