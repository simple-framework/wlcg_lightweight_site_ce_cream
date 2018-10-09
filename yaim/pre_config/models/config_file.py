class ConfigFile:
    def __init__(self, output_file, data):
        self.categories = []
        self.evaluated_objects = []
        self.output_file = output_file
        self.data = data

    def add_categories(self, categories):
        for category in categories:
            self.categories.append(category)

    def evaluate_categories(self):
        for category in self.categories:
            evaluated_results = category.get()
            self.evaluated_objects.append(evaluated_results)

    def generate_output_file(self):
        output_file = open(self.output_file, 'w')
        for evaluated_object in self.evaluated_objects:
            for key in evaluated_object:
                output = self.generate_yaim_output(key, evaluated_object[key])
                output_file.write(output)
        output_file.close()

    def generate_yaim_output(self, key, value):
        env_variable = key.upper() + "=" + str(value) + "\n"
        return env_variable