from cloudshell.devices.standards.load_balancing.autoload_structure import (
    GenericRealServer,
)
from cloudshell.devices.standards.validators import attr_length_validator


class F5RealServer(GenericRealServer):
    @property
    def monitors(self):
        """Get F5 Loadbalancer Monitors.

        :rtype: str
        """
        return self.attributes.get("{}Monitors".format(self.namespace), None)

    @monitors.setter
    @attr_length_validator
    def monitors(self, value=""):
        """Set F5 Loadbalancer Monitors.

        :type value: str
        """
        self.attributes["{}Monitors".format(self.namespace)] = value
