import json

class SaveManager:
    def __init__(self, file_path='save.json'):
        self.file_path = file_path

    def load_game(self):
        try:
            with open(self.file_path, 'r') as f:
                loaded_data = json.load(f)
            
            default_data = self.get_default_save()
            
            def merge_data(default, loaded):
                for key, value in default.items():
                    if key not in loaded:
                        loaded[key] = value
                    elif isinstance(value, dict):
                        merge_data(value, loaded[key])
            
            merge_data(default_data, loaded_data)
            return loaded_data

        except (FileNotFoundError, json.JSONDecodeError):
            return self.get_default_save()

    def save_game(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_default_save(self):
        return {
            "currencies": {
                "gold": 0,
                "exp": 0,
                "flesh": 0
            },
            "furnace_upgrades": {
                "production_rate": 0,
                "storage_capacity": 0,
                "production_speed": 0,
                "health": 0
            },
            "wall_upgrades": {
                "health": 0,
                "enchantment_slots": 0,
                "enchantment_level": 0
            },
            "troop_upgrades": {
                "strength": 0,
                "stamina": 0,
                "training_cost": 0
            }
        }
