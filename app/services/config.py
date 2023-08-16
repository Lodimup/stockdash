import tomllib

def read_config():
    with open('config.toml', 'rb') as f:
        config = tomllib.load(f)
    return config

read_config()