class UniqueNameGenerator(object):
    def __init__(self):
        self._used_names = []

    def get_unique_name(self, name):
        """Get unique name.

        :param str name:
        :return:
        """
        while name.lower() in self._used_names:
            name = "{}-1".format(name)

        self._used_names.append(name.lower())
        return name
