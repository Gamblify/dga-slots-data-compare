class CSCHeader:
    def __init__(self, start_date):
        self.start_date = start_date


class CSCFile:
    def __init__(self, header: CSCHeader):
        self.header = header


