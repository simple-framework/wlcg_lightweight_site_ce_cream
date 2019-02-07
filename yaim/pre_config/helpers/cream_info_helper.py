import yaql

engine = yaql.YaqlFactory().create()
def evaluate(data, query):
    expression = engine(query)
    return expression.evaluate(data)

def globus_tcp_port_range(component_section):
    print evaluate(component_section, "$.config.globus_tcp_port_range")

    return "20k-21k"