
def read_yml_file(file_path):
    with open(file_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exec:
            logging.error(exec)

def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string)
    return string

def col_validate(df, col_config):
    cols = df.columns
    cols = cols.str.replace(' ', '_')
    cols = list(map(lambda x: replacer(x, '_'), list(cols)))
    expected_cols = list(map(lambda x: x.lower(), col_config['columns']))
    cols = list(map(lambda x: x.lower(), list(cols)))
    
    if len(cols) == len(expected_cols) and list(cols) == list(expected_cols):
        print("\nColumn name and column length are successfully validated!")
        return 1

    else:
        print("Column name and column length have not passed the validation test")
        mismatched_columns = list(set(colms).difference(expected_col))
        print("The following columns are missing from the YAML file", mismatched_columns)
        missing_file = list(set(expected_col).difference(colms))
        print("The followning columns are missing from the file uploaded", missing_file)
        logging.info(f'df columns: {colms}')
        logging.info(f'expected columns: {expected_col}')
        return 0
