#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.standards.base import AbstractResource
from cloudshell.devices.standards.validators import attr_length_validator

AVAILABLE_SHELL_TYPES = ["CS_LoadBalancer"]

__all__ = ["GenericResource", "GenericChassis", "GenericRealServer"
           "GenericModule", "GenericSubModule", "GenericServerFarm"
           "GenericPortChannel", "GenericPowerPort", "GenericPort"]


class GenericResource(AbstractResource):
    RESOURCE_MODEL = "GenericResource"
    RELATIVE_PATH_TEMPLATE = ""

    def __init__(self, shell_name, name, unique_id, shell_type="CS_LoadBalancer"):
        super(GenericResource, self).__init__(shell_name, name, unique_id)

        self.shell_name = "{}.".format(shell_name)
        if shell_type in AVAILABLE_SHELL_TYPES:
            self.shell_type = "{}.".format(shell_type)
        else:
            raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                     "Shell type should be one of: {avail}"
                            .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))

    @property
    def contact_name(self):
        """ Return the name of a contact registered in the device """

        return self.attributes.get("{}Contact Name".format(self.shell_type), None)

    @contact_name.setter
    @attr_length_validator
    def contact_name(self, value):
        """ Set the name of a contact registered in the device """

        self.attributes["{}Contact Name".format(self.shell_type)] = value

    @property
    def os_version(self):
        """ Return version of the Operating System """

        return self.attributes.get("{}OS Version".format(self.shell_type), None)

    @os_version.setter
    @attr_length_validator
    def os_version(self, value):
        """ Set version of the Operating System """

        self.attributes["{}OS Version".format(self.shell_type)] = value

    @property
    def system_name(self):
        """ Set device system name """

        return self.attributes.get("{}System Name".format(self.shell_type), None)

    @system_name.setter
    @attr_length_validator
    def system_name(self, value):
        """ Set device system name """

        self.attributes["{}System Name".format(self.shell_type)] = value

    @property
    def vendor(self):
        """ Return The name of the device manufacture """

        return self.attributes.get("{}Vendor".format(self.shell_type), None)

    @vendor.setter
    @attr_length_validator
    def vendor(self, value=""):
        """ Set The name of the device manufacture """

        self.attributes["{}Vendor".format(self.shell_type)] = value

    @property
    def location(self):
        """ The device physical location identifier. For example Lab1/Floor2/Row5/Slot4 """

        return self.attributes.get("{}Location".format(self.shell_type), None)

    @location.setter
    @attr_length_validator
    def location(self, value=""):
        """ Set The device physical location identifier """

        self.attributes["{}Location".format(self.shell_type)] = value

    @property
    def model(self):
        """ Return the device model. This information is typically used for abstract resource filtering """

        return self.attributes.get("{}Model".format(self.shell_type), None)

    @model.setter
    @attr_length_validator
    def model(self, value=""):
        """ Set the device model. This information is typically used for abstract resource filtering """

        self.attributes["{}Model".format(self.shell_type)] = value

    @property
    def model_name(self):
        """ Return the device model name. This information is typically used for abstract resource filtering """

        return self.attributes.get("{}Model Name".format(self.shell_type), None)

    @model_name.setter
    @attr_length_validator
    def model_name(self, value=""):
        """ Set the device model name. This information is typically used for abstract resource filtering """

        self.attributes["{}Model Name".format(self.shell_type)] = value


class GenericServerFarm(AbstractResource):
    RESOURCE_MODEL = "GenericServerFarm"
    RELATIVE_PATH_TEMPLATE = "SF"

    @property
    def algorithm(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Algorithm".format(self.namespace), None)

    @algorithm.setter
    @attr_length_validator
    def algorithm(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Algorithm".format(self.namespace)] = value

    @property
    def virtual_server_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Virtual Server Address".format(self.namespace), None)

    @virtual_server_address.setter
    @attr_length_validator
    def virtual_server_address(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Virtual Server Address".format(self.namespace)] = value

    @property
    def virtual_server_port(self):
        """d
        :rtype: str
        """
        return self.attributes.get("{}Virtual Server Port".format(self.namespace), None)

    @virtual_server_port.setter
    @attr_length_validator
    def virtual_server_port(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Virtual Server Port".format(self.namespace)] = value


class GenericRealServer(AbstractResource):
    RESOURCE_MODEL = "GenericRealServer"
    RELATIVE_PATH_TEMPLATE = "RS"

    @property
    def address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Server Address".format(self.namespace), None)

    @address.setter
    @attr_length_validator
    def address(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Server Address".format(self.namespace)] = value


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = "GenericChassis"
    RELATIVE_PATH_TEMPLATE = "CH"

    @property
    def model(self):
        """ Return the chassis model """

        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    @attr_length_validator
    def model(self, value=""):
        """ Set the chassis model """

        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericModule(AbstractResource):
    RESOURCE_MODEL = "GenericModule"
    RELATIVE_PATH_TEMPLATE = "M"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    @attr_length_validator
    def model(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    @attr_length_validator
    def version(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericSubModule(AbstractResource):
    RESOURCE_MODEL = "GenericSubModule"
    RELATIVE_PATH_TEMPLATE = "SM"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    @attr_length_validator
    def model(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    @attr_length_validator
    def version(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value


class GenericPort(AbstractResource):
    RESOURCE_MODEL = "GenericPort"
    RELATIVE_PATH_TEMPLATE = "P"

    @property
    def mac_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}MAC Address".format(self.namespace), None)

    @mac_address.setter
    @attr_length_validator
    def mac_address(self, value=""):
        """

        :type value: str
        """
        self.attributes["{}MAC Address".format(self.namespace)] = value

    @property
    def l2_protocol_type(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}L2 Protocol Type".format(self.namespace), None)

    @l2_protocol_type.setter
    @attr_length_validator
    def l2_protocol_type(self, value):
        """
        Such as POS, Serial
        :type value: str
        """
        self.attributes["{}L2 Protocol Type".format(self.namespace)] = value

    @property
    def ipv4_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv4 Address".format(self.namespace), None)

    @ipv4_address.setter
    @attr_length_validator
    def ipv4_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv4 Address".format(self.namespace)] = value

    @property
    def ipv6_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv6 Address".format(self.namespace), None)

    @ipv6_address.setter
    @attr_length_validator
    def ipv6_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv6 Address".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    @attr_length_validator
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value

    @property
    def bandwidth(self):
        """
        :rtype: float
        """
        return self.attributes.get("{}Bandwidth".format(self.namespace), 0)

    @bandwidth.setter
    @attr_length_validator
    def bandwidth(self, value):
        """
        The current interface bandwidth, in MB.
        :type value: float
        """
        self.attributes["{}Bandwidth".format(self.namespace)] = value or 0

    @property
    def mtu(self):
        """
        :rtype: float
        """
        return self.attributes.get("{}MTU".format(self.namespace), 0)

    @mtu.setter
    @attr_length_validator
    def mtu(self, value):
        """
        The current MTU configured on the interface.
        :type value: float
        """
        self.attributes["{}MTU".format(self.namespace)] = value or 0

    @property
    def duplex(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Duplex".format(self.namespace), "Half")

    @duplex.setter
    @attr_length_validator
    def duplex(self, value):
        """
        The current duplex configuration on the interface. Possible values are Half or Full.
        :type value: str
        """

        self.attributes["{}Duplex".format(self.namespace)] = value or "Half"

    @property
    def adjacent(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Adjacent".format(self.namespace), None)

    @adjacent.setter
    @attr_length_validator
    def adjacent(self, value):
        """
        The adjacent device (system name) and port, based on LLDP or CDP protocol.
        :type value: str
        """
        self.attributes["{}Adjacent".format(self.namespace)] = value

    @property
    def auto_negotiation(self):
        """
        :rtype: bool
        """
        return self.attributes.get("{}Auto Negotiation".format(self.namespace), None)

    @auto_negotiation.setter
    @attr_length_validator
    def auto_negotiation(self, value):
        """
        The current auto negotiation configuration on the interface.
        :type value: bool
        """
        self.attributes["{}Auto Negotiation".format(self.namespace)] = value


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = "GenericPowerPort"
    RELATIVE_PATH_TEMPLATE = "PP"

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Model".format(self.namespace), None)

    @model.setter
    @attr_length_validator
    def model(self, value):
        """
        The device model. This information is typically used for abstract resource filtering.
        :type value: str
        """
        self.attributes["{}Model".format(self.namespace)] = value

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Serial Number".format(self.namespace), None)

    @serial_number.setter
    @attr_length_validator
    def serial_number(self, value):
        """

        :type value: str
        """
        self.attributes["{}Serial Number".format(self.namespace)] = value

    @property
    def version(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Version".format(self.namespace), None)

    @version.setter
    @attr_length_validator
    def version(self, value):
        """
        The firmware version of the resource.
        :type value: str
        """
        self.attributes["{}Version".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    @attr_length_validator
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = "GenericPortChannel"
    RELATIVE_PATH_TEMPLATE = "PC"

    @property
    def associated_ports(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Associated Ports".format(self.namespace), None)

    @associated_ports.setter
    @attr_length_validator
    def associated_ports(self, value):
        """ Ports associated with this port channel.
        The value is in the format ???[portResourceName],??????, for example ???GE0-0-0-1,GE0-0-0-2???
        :type value: str
        """
        self.attributes["{}Associated Ports".format(self.namespace)] = value

    @property
    def ipv4_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv4 Address".format(self.namespace), None)

    @ipv4_address.setter
    @attr_length_validator
    def ipv4_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv4 Address".format(self.namespace)] = value

    @property
    def ipv6_address(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}IPv6 Address".format(self.namespace), None)

    @ipv6_address.setter
    @attr_length_validator
    def ipv6_address(self, value):
        """

        :type value: str
        """
        self.attributes["{}IPv6 Address".format(self.namespace)] = value

    @property
    def port_description(self):
        """
        :rtype: str
        """
        return self.attributes.get("{}Port Description".format(self.namespace), None)

    @port_description.setter
    @attr_length_validator
    def port_description(self, value):
        """
        The description of the port as configured in the device.
        :type value: str
        """
        self.attributes["{}Port Description".format(self.namespace)] = value
