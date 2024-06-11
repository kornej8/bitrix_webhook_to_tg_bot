import configparser

def get_from_global_config(item):
    _config = configparser.RawConfigParser()
    _config.read('./config.cfg', encoding="utf-8")
    try:
        return dict(_config.items('MAIN CREDENTIONALS'))[item]
    except Exception as e:
        return dict()