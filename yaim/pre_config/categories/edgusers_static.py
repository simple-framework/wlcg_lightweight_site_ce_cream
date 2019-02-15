from models.parameter_category import ParameterCategory

def get(data):
    static_category = ParameterCategory("edgusers_static", data)
    edgusers = "155:${GLITE_USER}:155:${GLITE_GROUP}:gLite user:${GLITE_HOME_DIR} \n" \
               "154:${BDII_USER}:158:${BDII_GROUP}:BDII user:${BDII_HOME_DIR}"
    static_category.add(edgusers)
    return [static_category]