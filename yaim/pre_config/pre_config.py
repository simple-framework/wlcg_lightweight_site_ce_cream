import argparse
import yaml
import yaql
from models.config_file import ConfigFile
from categories import cream_info_static, cream_info_queried, cream_info_advanced

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--id', help="ID of lightweight component")
    args = parser.parse_args()
    return {
        'compiled_site_level_configuration_file': args.filename,
        'component_id': args.id
    }

def get_cream_info_file_categories(data, id):
    categories = []
    static = cream_info_static.get(data)
    queried = cream_info_queried.get(data, id)
    advanced = cream_info_advanced.get(data, id)
    categories.append(static)
    categories.append(queried)
    categories.append(advanced)
    return static + queried + advanced

if __name__ == "__main__":
    args = parse_args()
    id = args['component_id']
    site_config_filename =  args['compiled_site_level_configuration_file']
    site_config = open(site_config_filename, 'r')
    data = yaml.load(site_config)
    cream_info_file = ConfigFile('./.temp/cream-info.def', data)
    users_file = ConfigFile('./.temp/users.conf', data)
    groups_file = ConfigFile('./.temp/groups.conf', data)
    wn_list_file = ConfigFile('./.temp/wn-list.conf', data)
    edgusers_file = ConfigFile('./.temp/edgusers.conf', data)

    cream_info_file.add_categories(get_cream_info_file_categories(data, id))
    cream_info_file.generate_output_file()
