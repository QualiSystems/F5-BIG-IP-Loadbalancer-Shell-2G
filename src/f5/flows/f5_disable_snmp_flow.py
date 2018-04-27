#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from cloudshell.devices.flows.cli_action_flows import DisableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters

from f5.command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions


class F5DisableSnmpFlow(DisableSnmpFlow):
    def __init__(self, cli_handler, logger, remove_group=True):
        """
          Enable snmp flow
          :param cli_handler:
          :type cli_handler: JuniperCliHandler
          :param logger:
          :return:
          """
        super(F5DisableSnmpFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler
        self._remove_group = remove_group

    def execute_flow(self, snmp_parameters=None):
        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                snmp_actions = EnableDisableSnmpActions(config_session, logger=self._logger)
                if isinstance(snmp_parameters, SNMPV3Parameters):
                    raise Exception("SNMPv3 currently is not supported")
                else:
                    current_snmp_community_list = snmp_actions.get_current_snmp_communities()
                    if snmp_parameters.snmp_community in current_snmp_community_list:
                        result = snmp_actions.disable_snmp()
                        if snmp_parameters.snmp_community in snmp_actions.get_current_snmp_communities():
                            self._logger.error("Failed to configure snmp community: {}".format(result))
                            raise Exception("Failed to configure snmp parameters. Please see logs for details")
                    current_snmp_access = snmp_actions.get_current_snmp_access_list()
                    if "0.0.0.0/0" in current_snmp_access:
                        result = snmp_actions.disable_snmp_access()
                        if "0.0.0.0/0" in snmp_actions.get_current_snmp_access_list():
                            self._logger.error("Failed to remove snmp access list: {}".format(result))
                            raise Exception("Failed to remove snmp parameters. Please see logs for details")
