from cloudshell.devices.standards.validators import attr_length_validator
from cloudshell.devices.standards.load_balancing.autoload_structure import GenericRealServer


class F5RealServer(GenericRealServer):
    @property
    def monitors(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}Monitors".format(self.namespace), None)

    @monitors.setter
    @attr_length_validator
    def monitors(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Monitors".format(self.namespace)] = value
