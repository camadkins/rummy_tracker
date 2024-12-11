import yaml

def load_config(filename):
    try:
        with open(filename, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}
