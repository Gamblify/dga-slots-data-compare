import sys

from src.csc.CSCParser import CSCParser


def read_csc_file() -> str:
    with open('/tmp/csc.msg', 'r') as csc_file:
        return csc_file.read()


def main() -> int:
    csc_raw_data = read_csc_file()

    csc_parser = CSCParser()
    csc_parsed_data = csc_parser.parse(data=csc_raw_data)

    return 0


if __name__ == '__main__':
    sys.exit(main())
