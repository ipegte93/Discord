def getDefNameList(cls):
    def_name_list = []
    for method in dir(cls):
        if method.startswith("_") is False:
            def_name_list.append(method)

    return def_name_list