import argparse
import yaml
import yaql
from models.config_file import ConfigFile
from categories import cream_info_static, cream_info_queried, cream_info_advanced, \
    users_advanced, \
    groups_advanced, \
    edgusers_static, \
    wn_list_advanced, \
    hosts_container_advanced

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_config', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--execution_id', help="ID of lightweight component")
    parser.add_argument('--output_dir', help="Output directory")
    args = parser.parse_args()
    return {
        'augmented_site_level_config_file': args.site_config,
        'execution_id': args.execution_id,
        'output_dir': args.output_dir
    }


def get_cream_info_file_categories(data, id):
    static = cream_info_static.get(data)
    queried = cream_info_queried.get(data, id)
    advanced = cream_info_advanced.get(data, id)
    return static + queried + advanced


def get_users_conf_file_categories(data, id):
    advanced = users_advanced.get(data, id)
    return advanced


def get_groups_conf_file_categories(data, id):
    advanced = groups_advanced.get(data, id)
    return advanced


def get_edgusers_file_categories(data):
    static = edgusers_static.get(data)
    return  static


def get_wn_list_file_categories(data):
    advanced = wn_list_advanced.get(data)
    return advanced

def get_hosts_container_file_advanced_category(data, id):
    advanced = hosts_container_advanced.get(data, id)
    return advanced

if __name__ == "__main__":
    args = parse_args()
    id = args['execution_id']
    site_config_filename =  args['augmented_site_level_config_file']
    site_config = open(site_config_filename, 'r')
    data = yaml.load(site_config)
    output_dir = args['output_dir']
    cream_info_file = ConfigFile(output_dir +'/cream-info.def', data)
    users_file = ConfigFile(output_dir + '/users.conf', data)
    groups_file = ConfigFile(output_dir + '/groups.conf', data)
    wn_list_file = ConfigFile(output_dir + '/wn-list.conf', data)
    edgusers_file = ConfigFile(output_dir + '/edgusers.conf', data)
    hosts_container_file = ConfigFile(output_dir + '/hosts-container.conf', data)

    cream_info_file.add_categories(get_cream_info_file_categories(data, id))
    cream_info_file.generate_output_file()

    users_file.add_categories(get_users_conf_file_categories(data, id))
    users_file.generate_output_file()

    groups_file.add_categories(get_groups_conf_file_categories(data, id))
    groups_file.generate_output_file()

    edgusers_file.add_categories(get_edgusers_file_categories(data))
    edgusers_file.generate_output_file()

    wn_list_file.add_categories(get_wn_list_file_categories(data))
    wn_list_file.generate_output_file()

    hosts_container_file.add_categories(get_hosts_container_file_advanced_category(data, id))
    hosts_container_file.generate_output_file()