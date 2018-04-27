#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.autoload_runner import AutoloadRunner

from f5.flows.f5_autoload_flow import F5SnmpAutoloadFlow


class F5AutoloadRunner(AutoloadRunner):
    def __init__(self, logger, resource_config, snmp_handler):
        super(F5AutoloadRunner, self).__init__(resource_config)
        self._logger = logger
        self.snmp_handler = snmp_handler

    @property
    def autoload_flow(self):
        return F5SnmpAutoloadFlow(self.snmp_handler, self._logger)
