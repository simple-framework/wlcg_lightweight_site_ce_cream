from models.parameter_category import ParameterQueriedCategory
import yaql

def get(data):
    category = ParameterQueriedCategory("cream_info_static", data)
    category.add("site_name", "$.site.name")
    category.add("site_email", "$.site.email")
    category.add("site_lat", "$.site.latitude")
    category.add("site_long", "$.site.latitude")
    category.add("site_desc", "$.site.description")
    category.add("site_loc", "$.site.location")
    category.add("site_loc", "$.site.location")
    return category