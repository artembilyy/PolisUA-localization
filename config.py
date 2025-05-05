import os

class Config:
    def __init__(self):
        # Get the directory of this script (root of PolisUA-localization)
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        # Directory containing YAML localization files
        self.yaml_dir = os.path.join(self.script_dir, "Localization")
        # Temporary directory for cloning (not used in this repo, but defined for cleanup)
        self.local_repo_dir = os.path.join(self.script_dir, "repo")
        
        # Output paths for iOS localization files
        # Relative to the iOS project root (PolisUA)
        self.ios_output_dir = os.path.join(self.script_dir, "..", "..", "Resources")
        # Path for generated RSKey.swift file
        self.ios_enum_output = os.path.join(self.ios_output_dir, "RSKey.swift")
        
        # Placeholders for future platform support
        self.android_output_dir = ""  # TODO: Define Android output path for strings.xml
        self.web_output_dir = ""      # TODO: Define Web output path for JSON files
