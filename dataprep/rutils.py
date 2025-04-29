import yaml 

def write_yaml(yaml_data, yaml_file_path):
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file)
    print('write_yaml')
    
def read_yaml(filename):
    with open(filename, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        print('read_yaml')
        return yaml_data