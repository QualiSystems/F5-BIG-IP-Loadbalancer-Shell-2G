#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.snmp_action_flows import AutoloadFlow

from f5.autoload.f5_generic_snmp_autoload import F5GenericSNMPAutoload


class F5SnmpAutoloadFlow(AutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        with self._snmp_handler.get_snmp_service() as snmp_service:
            f5_snmp_autoload = F5GenericSNMPAutoload(snmp_service,
                                                     shell_name,
                                                     shell_type,
                                                     resource_name,
                                                     self._logger)
            return f5_snmp_autoload.discover(supported_os)
