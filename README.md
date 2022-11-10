# Application for comparing slotmachine data from CSC with SAFE data

### Installation

 Installation of pipenv:  `pip install --user pipenv`  
 pipenv can be found in: `~/.local/bin/pipenv`   
 Setup the environment: `pipenv install`
 
 ### Usage
 ```
usage: main.py [-h] [-v] [-d] --safe-dir SAFE_DIR --csc-dir CSC_DIR --start-date START_DATE [--end-date END_DATE] [--csc-extension CSC_EXTENSION]
               [--safe-extension SAFE_EXTENSION]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -d, --debug           Show debug log
  --safe-dir SAFE_DIR   Directory with all the SAFE EndOfDay reports
  --csc-dir CSC_DIR     Directory with all the CSC reports
  --start-date START_DATE
                        Start date in the format YYYY-MM-DD
  --end-date END_DATE   End date in the format YYYY-MM-DD. If not provided it will be today
  --csc-extension CSC_EXTENSION
                        File extensions for the CSC files. default=msg
  --safe-extension SAFE_EXTENSION
                        File extensions for the SAFE files. default=xml

```
 
 ### Run the application: 
 `pipenv run python main.py --csc-dir csc_data_prod --safe-dir safe_data --start-date 2020-01-01`
 
