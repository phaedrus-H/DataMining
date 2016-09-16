# -*- coding: utf-8 -*-

import sys
from collections import OrderedDict
from msap import msap

"""
    This function parses the input file and returns the transaction database
"""

def process_input_file(input_file_name):
    transaction_database = []
    try:
        with open(input_file_name, 'r') as f:
            file_content = f.read()
            #if the file is not empty
            if file_content and file_content.strip():
                file_content = file_content.strip()
                all_rows = file_content.split('\n')
                for row in all_rows:
                    row_content = []
                    for val in row.split(","):
                        row_content.append(val.replace('{','').replace('}','').strip())
                    if len(row_content) > 0:
                        transaction_database.append(row_content)
            else:
                print("Input file is empty")
    except (FileNotFoundError, IOError):
        print("Input file does not exist")
    return transaction_database
    
"""
    This function parses the parameter file and returns the various parameters associated
"""
    
def process_parameter_file(parameter_file_name):
    parameters = dict()
    try:
        with open(parameter_file_name, 'r') as f:
            file_content = f.read()
            #if the file is not empty
            if file_content and file_content.strip():
                file_content = file_content.strip()
                all_rows = file_content.split('\n')
                mis_dictionary = OrderedDict()
                cannot_be_together = []
                must_have = []
                for row in all_rows:
                    if "MIS" in row:
                        mis_list = row.split("=")
                        mis_for_item = mis_list[0]
                        mis_dictionary[mis_for_item[mis_for_item.index("(")+1:mis_for_item.index(")")]] = float(mis_list[-1].strip())
                    elif "SDC" in row:
                        sdc_value = row.split("=")[-1].strip()
                        parameters["SDC"] = float(sdc_value)
                    elif "cannot_be_together" in row:
                        value_string = row.split(":")[-1].strip()
                        for val in value_string.split(","):
                            cannot_be_together.append(val.replace('{','').replace('}','').strip())
                    elif "must-have" in row:
                        value_string = row.split(":")[-1].strip()
                        if "or" in value_string:
                            for val in value_string.split("or"):
                                must_have.append(val.strip())
                        else:
                            must_have.append(value_string.strip())
                parameters["mis_dictionary"] = mis_dictionary
                parameters["cannot_be_together"] = cannot_be_together
                parameters["must_have"] = must_have
            else:
                print("Parameter file is empty")
    except (FileNotFoundError, IOError):
        print("Parameter file does not exist")
    return parameters
    
"""
    This is the entry point of the algorithm
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
        parameter_file_name = sys.argv[2]
        transaction_database = process_input_file(input_file_name)
        parameters = process_parameter_file(parameter_file_name)
        if len(transaction_database) > 0 and len(parameters) > 0 and len(parameters["mis_dictionary"]) > 0:
            msap(transaction_database, parameters)
        else:
            print("Required input parameters are missing")
    else:
        print("Please provide input file name followed by parameter file name as command line parameters")