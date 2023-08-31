import configparser

config = configparser.ConfigParser()

config['user'] = {'Authorization': "Basic SGFubmFoQVBJOlVudDBsZCEhQ2hhbmNl",
                  'Accept': 'application/json'}
config['specifications'] = {
    'url': 'https://uclahealth-dev.collibra.com/rest/2.0/',
    'domain_id_1': '7f0c695e-8577-433d-a3a5-753456ed71ca',
    'domain_id_2': '4710521c-32c0-429f-acad-c180866955a7',
    'asset_type_ids': ["00000000-0000-0000-0000-000000031008", ],
    'asset_limit': 2600
}
config['attributes'] = {
    'api_call': 'attributes',
    'attribute_type_id': '00000000-0000-0000-0000-000000000249'
}
with open('config.ini', 'w') as configfile:
    config.write(configfile)
    configfile.flush()
    configfile.close()

read_file = open('config.ini', 'r')
content = read_file.read()
# print(content)
read_file.flush()
read_file.close()


def read_config():
    config.read('config.ini')
    return config
