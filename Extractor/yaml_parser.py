import os
import glob
import yaml

def collect_yaml_data(yaml_dir):
    # Check if the YAML directory exists
    if not os.path.exists(yaml_dir):
        raise Exception(f"Localization directory {yaml_dir} does not exist")

    # Find all YAML files recursively in the directory
    yaml_files = glob.glob(os.path.join(yaml_dir, "**", "*.yaml"), recursive=True)
    if not yaml_files:
        raise Exception("No YAML files found in Localization directory or its subdirectories")
    
    # Dictionary to store parsed YAML data
    all_tables = {}
    for yaml_file in yaml_files:
        # Extract category name from the file (without extension)
        category = os.path.splitext(os.path.basename(yaml_file))[0]
        # Read and parse the YAML file
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            all_tables[category] = data["strings"]
        # Log processed file for debugging
        print(f" - {os.path.relpath(yaml_file, yaml_dir)}")
    
    # Return parsed data as a dictionary
    return all_tables
