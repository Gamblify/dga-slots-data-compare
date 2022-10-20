from src.csc.CSCFile import CSCFile, CSCHeader


class CSCParser:
    def parse(self, name: str) -> CSCFile:
        return CSCFile(header=CSCHeader(start_date='test'))
