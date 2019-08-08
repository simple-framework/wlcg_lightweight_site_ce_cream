from models.parameter_category import ParameterCategory

def get(data):
    static_category = ParameterCategory("edgusers_static", data)
    edgusers = "152:${EDG_USER}:152,151:${EDG_GROUP},${INFOSYS_GROUP}:EDG user:${EDG_HOME_DIR}\n" \
               "153:${EDGINFO_USER}:153,151:${EDGINFO_USER},${INFOSYS_GROUP}:EDG info user:${EDGINFO_HOME_DIR}\n" \
               "155:${GLITE_USER}:155:${GLITE_GROUP}:gLite user:${GLITE_HOME_DIR} \n" \
               "154:${BDII_USER}:158:${BDII_GROUP}:BDII user:${BDII_HOME_DIR}"
    static_category.add(edgusers)
    return [static_category]