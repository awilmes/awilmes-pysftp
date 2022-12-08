# Loads the config file once and only once
import tomllib


with open('conf/config.toml', mode='rb') as fp:
    cfg = tomllib.load(fp)
