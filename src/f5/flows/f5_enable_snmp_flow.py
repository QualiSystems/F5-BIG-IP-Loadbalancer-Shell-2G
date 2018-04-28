#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from cloudshell.devices.flows.cli_action_flows import EnableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV3Parameters, SNMPV2WriteParameters

from f5.command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions


class F5EnableSnmpFlow(EnableSnmpFlow):
    def __init__(self, cli_handler, logger, create_group=True):
        """
        Enable snmp flow
        :param cli_handler:
        :param logger:
        :return:
        """
        super(F5EnableSnmpFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler
        self._create_group = create_group

    def execute_flow(self, snmp_parameters):
        if hasattr(snmp_parameters, "snmp_community") and not snmp_parameters.snmp_community:
            message = 'SNMP community cannot be empty'
            self._logger.error(message)
            raise Exception(self.__class__.__name__, message)

        is_read_only_community = True

        if isinstance(snmp_parameters, SNMPV2WriteParameters):
            is_read_only_community = False

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                snmp_actions = EnableDisableSnmpActions(config_session, logger=self._logger)
                if isinstance(snmp_parameters, SNMPV3Parameters):
                    raise Exception("SNMPv3 currently is not supported")
                else:
                    current_snmp_community_list = snmp_actions.get_current_snmp_communities()
                    if snmp_parameters.snmp_community not in current_snmp_community_list:
                        result = snmp_actions.enable_snmp(snmp_parameters.snmp_community, is_read_only_community)
                        if snmp_parameters.snmp_community not in snmp_actions.get_current_snmp_communities():
                            self._logger.error("Failed to configure snmp community: {}".format(result))
                            raise Exception("Failed to configure snmp parameters. Please see logs for details")
                    current_snmp_access = snmp_actions.get_current_snmp_access_list()
                    if "0.0.0.0/0" not in current_snmp_access:
                        result = snmp_actions.enable_snmp_access()
                        if "0.0.0.0/0" not in snmp_actions.get_current_snmp_access_list():
                            self._logger.error("Failed to configure snmp access list: {}".format(result))
                            raise Exception("Failed to configure snmp parameters. Please see logs for details")
