import configparser
import os


def read_config(section, key):
    """
    Reads value from config.ini file based on section and key
    """

    config = configparser.ConfigParser()

    # Build absolute path to config.ini
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, "config", "config.ini")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.ini not found at {config_path}")

    config.read(config_path)

    if section not in config:
        raise Exception(f"Section '{section}' not found in config.ini")

    if key not in config[section]:
        raise Exception(f"Key '{key}' not found in section '{section}'")

    return config[section][key]
