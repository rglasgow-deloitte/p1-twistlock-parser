import os
import re
from tkinter import W


class TwistlockClean:
    def __init__(self, file_queue) -> None:
        self.file_queue = file_queue

    def __scrub_compliance(self, data):
        """
        Scrub the compliance data
        """
        # regex to capture the compliance data
        compliance_regex = r"(?<=\'compliance\':)([\S\s]*?)(?='cve': \[)"
        
        compliance = re.search(compliance_regex, data).group(0)

        cause_regex = r"(?<=\'cause\':)([\S\s]*?)(?=\'cri\')"
        # not none or empty array
        if compliance is not None and len(compliance) > 6:
            cause = re.search(cause_regex, compliance).group(0)
            
            # remove "Found: " from the cause
            cause = cause.replace("Found: ", "")
            
            cause = cause.replace("'", "")
            cause = cause.replace(" ", "")
            cause = cause.replace('\n', '')
            cause = cause.split(",")
            
            data = data.replace(re.search(cause_regex, data).group(0), str(cause)+',')


        # regex = r"(?<=\'cause\':)([\S\s]*?)(?='discovered':)"
        return data

    def __scrub_cve(self, data):
        # regex to match the 'description' and 'discovered' lines
        regex = r"(?<=\'description\':)([\S\s]*?)(?='discovered':)"
        # each time the regex is found in the data
        for match in re.finditer(regex, data):
            # remove the text between the delimiters
            data = data.replace(match.group(0), "'',\n\t\t")

        return data

    def __correct_datatypes(self, data):
        # correcting the incorrect boolean values
        data = data.replace("False", "false")
        data = data.replace("True", "true")

        # replace None with null
        data = data.replace("None", "null")

        return data


    def __scrub_data(self, data):
        """ """
        # remove all the text up to and including the 'Report completed' line
        data = data.split("Report completed")[1]

        regex = r"(?s)(?<=}]})(.*)"
        data= data.replace(re.search(regex, data).group(0), "")

        data = self.__scrub_compliance(data)
        data = self.__scrub_cve(data)
        
        data = self.__correct_datatypes(data)

        # replace all the single quotes with double quotes
        data = data.replace("'", '"')

        return data

    def clean_files(self):
        """
        This function will clean the files in the directory and create new files with the same name _clean in a new directory called clean.
        """
        for file in self.file_queue:
            # open the file from the directory data
            with open(f"data/{file}", "r") as f:
                print(f"Reading file {file}")
                # read the file
                data = f.read()
                # scrub the data
                data = self.__scrub_data(data)
                # create the new directory clean if it does not exist
                if not os.path.exists("clean"):
                    os.mkdir("clean")
                # create a new file with the same name _clean in the directory clean
                file_name = file.split(".")[0] + "_clean.json"
                with open(f"clean/{file_name}", "w") as f:
                    print(f"Writing file {file}_clean")
                    # write the data to the new file
                    for line in data:
                        f.write(line)
