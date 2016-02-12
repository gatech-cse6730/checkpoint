import csv

class Reader(object):
    """
    Generic Reader class for processing input. Should be subclassed instead of used directly.
    """


    def __init__(self, filename):
        self.filename = filename

        return self.process()

    def process(self):
        # Override in subclass.
        pass