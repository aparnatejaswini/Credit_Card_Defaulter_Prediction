from defaulter_prediction.exception import Custom_Defaulter_Exception
import yaml
import sys


def read_yaml_file(file_path):
    try:
        with open(file_path) as file_obj:
            yaml_dict = yaml.safe_load(file_obj)
            return yaml_dict
    except Exception as e:
        raise Custom_Defaulter_Exception(e, sys)