#!/usr/bin/python
# -*- coding: utf-8 -*-


from f5.flows.f5_disable_snmp_flow import F5DisableSnmpFlow
from f5.flows.f5_enable_snmp_flow import F5EnableSnmpFlow
from cloudshell.devices.snmp_handler import SnmpHandler


class F5SnmpHandler(SnmpHandler):
    def __init__(self, resource_config, logger, api, cli_handler):
        super(F5SnmpHandler, self).__init__(resource_config, logger, api)
        self.cli_handler = cli_handler

    def _create_enable_flow(self):
        return F5EnableSnmpFlow(self.cli_handler, self._logger)

    def _create_disable_flow(self):
        return F5DisableSnmpFlow(self.cli_handler, self._logger)
