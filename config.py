import configparser

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['API_KEYS'].get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("APIキーが設定されていません。config.iniを確認してください。")
    return api_key
