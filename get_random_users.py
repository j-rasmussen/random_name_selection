
# _*_ encoding: utf-8 _*_
import sys
import logging
import random
import pandas as pd

"""
This terminal app is for returning a random list of users from a csv or json file
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

required_keys = ["file", "column", "number"]
help_response = "\n".join(
    [
        "-h, --help     return the available args",
        "-f, --file     is the containing the name excepted types are CSV or JSON",
        "-c, --column   is the columns or key that the name are to be chosen from",
        "-n, --number   is the number of user to return default is 10"
    ]
)


def get_args() -> dict:
    """
    parses the terminal args
    :return:
    """
    arg_keys: dict = {}
    global required_keys
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            arg_keys['help'] = True
        elif arg in ("-f", "--file"):
            arg_keys['file'] = sys.argv[sys.argv.index(arg) + 1]
        elif arg in ("-c", "--column"):
            arg_keys['column'] = sys.argv[sys.argv.index(arg) + 1]
        elif arg in ("-n", "--number"):
            arg_keys['number'] = int(sys.argv[sys.argv.index(arg) + 1])
    if not any(x in arg_keys.keys() for x in required_keys):
        print(f"\n{help_response}")
        exit()
    return arg_keys


def gen_names(file: str, column: str, number: int = 10) -> list:
    """
    returning a random list of users from a csv or json file
    :param file: needs to be a json or csv file with its path
    :param column: is the column or key to do the random selection on
    :param number: the amount of records to return
    :return: a list of the randomly selected records
    """
    if "csv" in file.lower():
        df = pd.read_csv(file)
    elif "json" in file.lower():
        df = pd.read_json()
    else:
        raise f"Not a valued file type\n\n{help_response}"
    try:
        col = list(df[column].drop_duplicates())
        if len(col) <= number:
            return col
        else:
            random_index = set()
            while len(random_index) <= number:
                if len(random_index) == number:
                    return [col[x] for x in random_index]
                random_index.add(random.randrange(number))
            return [col[x] for x in random_index]
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e


def main():
    arg_keys: dict = get_args()
    if "help" in arg_keys.keys():
        logger.info(help_response)
        return None
    names: str = "\n".join(str(x) for x in gen_names(**arg_keys))
    logger.info(f"\n\nRandomly selected:\n{names}")


if __name__ == '__main__':
    main()
