import argparse
import yaml
import yaql


class ConfigFile:
    def __init__(self, filename, data):
        self.query_list = {}
        self.evaluated_object = {}
        self.filename = filename
        self.engine = yaql.factory.YaqlEngine().create()
        self.data


    def add_query(self, parameter, query):
        self.query_list[parameter] = query

    def evaluate_query(self, parameter):
        query = self.query_list[parameter]
        expression = self.engine(query)
        return expression.evaluate(self.data)

    def evaluate_all_queries(self):
        for parameter in self.query_list:
            result = evaluate_query(parameter)
            self.evaluated_object[parameter] = result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help="Compiled Site Level Configuration YAML file")
    args = parser.parse_args()
    return {
        'compiled_site_level_configuration_file': args.filename,
    }

engine = yaql.factory.YaqlFactory().create()
def evaluate_query(data, query):
    expression = engine(query)
    return expression.evaluate(data=data)

def generate_output_from_grouped_queries(data, query_object):
    evaluated_objects = {}
    for element in query_object:
        value = evaluate_query(data, query_object[element])
        evaluated_objects[element] = value
    return evaluated_objects


def populate_wn_info(data):
    wn_info = []
    hardcoded_values = {
        'wn_list' : "/root/wn-list.conf",
        'users_conf': "/root/users.conf",
        'groups_conf': "/root/groups.conf"
    }
    site_level_information_queries =  {
        "site_name": "$.site.name",
        "site_email": "$.site.email",
        "px_host" : "$."
    }
    pbs_component_config_queries = {

    }
    site_level_information = generate_output_from_grouped_queries(data,site_level_information_queries)

    wn_info.append(site_level_information)
    wn_info.append(hardcoded_values)
    return wn_info


def write_output_files(file, file_data):
    for data in file_data:
        for key in data:
            env_variable = key.upper() + "=" + data[key] + "\n"
            file.write(env_variable)


if __name__ == "__main__":
    args = parse_args()
    site_config_filename =  args['compiled_site_level_configuration_file']
    site_config = open(site_config_filename, 'r')
    wn_info_file = open("./.temp/wn_info.def", 'w')
    wn_list_file = open("./.temp/wn_list.conf", 'w')
    users_file = open("./.temp/users.list", 'w')
    groups_file = open("./.temp/groups.list", 'w')

    data = yaml.load(site_config)


    wn_info = []
    wn_list = []
    users = []
    groups = []

    wn_info = populate_wn_info(data)
    print wn_info
    write_output_files(wn_info_file, wn_info)
    site_config.close()
    wn_info_file.close()
    wn_list_file.close()
    users_file.close()
    groups_file.close()
