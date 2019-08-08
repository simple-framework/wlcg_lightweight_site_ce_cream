from models.parameter_category import ParameterCategory


def get(data, id):
    advanced_category = ParameterCategory("hosts_advanced", data)
    dns = None
    for dns_info in data['dns']:
        if dns_info['execution_id'] == int(id):
            dns = dns_info
            break
    if dns is None:
        raise Exception("Cannot find dns info for current lightweight component in augmented site level config file")

    advanced_category.add("{host_ip} {host_fqdn} {hostname}".format(host_ip=dns['host_ip'],
                                                                    host_fqdn=dns['host_fqdn'],
                                                                    hostname=dns['host_fqdn'].split('.')[0]
                                                                    ))
    return [advanced_category]