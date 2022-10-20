from src.csc.CSCFile import CSCFile, CSCHeader


class CSCParser:
    def parse(self, data: str) -> CSCFile:
        return CSCFile(header=CSCHeader(start_date='test'))
