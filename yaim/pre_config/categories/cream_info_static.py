from models.parameter_category import ParameterStaticCategory


def get(data):
    category = ParameterStaticCategory("cream_info_static", data)
    category.add("wn_list", "/root/wn-list")
    category.add("users_conf", "/root/users_conf")
    return category
