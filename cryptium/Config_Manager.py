import json
class ConfigManager:
    def __init__(self, config_file = None):
        if config_file is None:
            config_file = "config_file.json"
        self.config_file = config_file

        self.default_config = {
            "base_path": "C:\\Users\\LENOVO\\Desktop\\AUTOMATION_PROJ_1\\",
            "log_files": {
                "Info_log": "Info Logs.log",
                "Error_log": "Error logs.log"
            },
            "extensions": {
                "extensions": {
            ".txt": "Text Files",
            "jpeg": "Images",
            ".jpg": "Images",
            ".png": "Images",
            ".doc": "Word Documents",
            ".docx": "Word Documents",
            ".ppt": "Powerpoint Documents",
            ".pptx": "POWERPOINT PRESENTATIONS",
            ".pdf": "PDF FILES"}
                }
        }
        self.load_config()
    def load_config(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        try:
            with open(config_file, 'r') as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            print("Config file not found. Setting default config...")
            self.config_data = self.default_config
        except json.JSONDecodeError:
            print("Config file is not a valid JSON.")   
            self.config_data = self.default_config
            
    def save_config(self):
        try:
            with open(self.config_file, 'r') as f:
                existing_data = json.load(f)
            # Merge existing data with current config_data because adding raw data corrupts the JSON structure
            existing_data.update(self.config_data)
            self.config_data = existing_data
            print("Merged existing config data with new data.") 
            
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f, indent=2)

    def get(self, key, default=None):
        return self.config_data.get(key, default)
    
    def update_config(self, key, value):
        try:
            # Ensures extensions dictionary exists
            if "extensions" not in self.config_data:
                self.config_data["extensions"] = {}
            
            # Updates the extensions dictionary
            self.config_data["extensions"][key] = value
            
            # Saves the changes to file
            self.save_config()
            print(f"Config updated: {key} = {value}")
            return True
        except Exception as e:
            print(f"Failed to update config: {e}")
            return False
    def load_overrides(self, override:dict):
        for key, value in override.items(): #What this line does is to iterate through the key-value pairs in the override dictionary
            if key in self.config_data:#This line checks if the key from the override dictionary exists in the config_data dictionary
                self.config_data[key] = value #what this line does is to update the config_data with the override values
    def reset_to_defaults(self):
        self.config_data = self.default_config
        self.save_config()
        print("Configuration reset to default settings.")
    