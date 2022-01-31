# main.py
from src.twistlock_clean import TwistlockClean
from src.twistlock_export import TwistlockExport
from src.utils import read_files





if __name__ == '__main__':
    directory = 'data'
    files_to_clean = read_files(directory)
    # create a queue
    clean = TwistlockClean(files_to_clean)
    clean.clean_files()


    clean_files = read_files('clean')
    # export 
    export = TwistlockExport(clean_files)
    export.export_to_excel()
