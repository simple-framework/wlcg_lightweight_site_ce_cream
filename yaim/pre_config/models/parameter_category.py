import yaql
from abc import ABCMeta


class ParameterCategory:
    __metaclass__ = ABCMeta

    def __init__(self, name, data):
        self.engine = yaql.factory.YaqlFactory().create()
        self.name = name
        self.data = data
        self.evaluated_object = {}

    def get(self):
        return self.evaluated_object

    def add(self, key, value):
        self.evaluated_object[key] = value


class ParameterQueriedCategory(ParameterCategory):

    def __init__(self, name, data):
        ParameterCategory.__init__(self, name, data)
        self.name = name
        self.param_query_pairs = {}

    def add(self, param, query):
        self.param_query_pairs[param] = query

    def get(self):
        self.evaluate_all_queries()
        return self.evaluated_object

    def evaluate_query(self, parameter):
        query = self.param_query_pairs[parameter]
        expression = self.engine(query)
        return  expression.evaluate(self.data)

    def evaluate_all_queries(self):
        for parameter in self.param_query_pairs:
            value = self.evaluate_query(parameter)
            self.evaluated_object[parameter] = value


class ParameterStaticCategory(ParameterCategory):

    def __init__(self, name, data):
        ParameterCategory.__init__(self, name, data)
        self.name = name
        self.evaluated_object = {}

