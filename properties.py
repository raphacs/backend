import yaml

class Properties:
    def __init__(self, environment="dev"):
        self.config_file_path = f"config-{environment}.yaml"
        self.load_config()

    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            self.config_data = yaml.safe_load(config_file)
            

    def get(self, key):
        return self.config_data.get(key)
    
    
