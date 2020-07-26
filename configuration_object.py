import json

class ConfigObject:
    def __init__(self):
        self.data = self.get_config_data()
        self.username = self.data["SSOL"]["username"]
        self.password = self.data["SSOL"]["password"]
        self.url = self.data["SSOL"]["url"]

    def get_config_data(self):
        with open('configuration.json') as json_data_file:
            data = json.load(json_data_file)
        
        return data
