#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ERROR_MAP = OrderedDict({"[Ss]yntax\s*[Ee]rror": "Failed to initialize snmp. Please check Logs for details."})

ENABLE_SNMP_ACCESS = CommandTemplate("modify sys snmp allowed-addresses add {{ 0.0.0.0/0 }}", error_map=ERROR_MAP)
DISABLE_SNMP_ACCESS = CommandTemplate("modify sys snmp allowed-addresses delete {{ 0.0.0.0/0 }}", error_map=ERROR_MAP)
SHOW_SNMP_ACCESS = CommandTemplate("list sys snmp allowed-addresses", error_map=ERROR_MAP)

CREATE_SNMP_COMMUNITY = CommandTemplate(
    "modify /sys snmp communities add {{ comm-quali {{ access {read_access} community-name {snmp_community}}} }}",
    error_map=ERROR_MAP)
REMOVE_SNMP_COMMUNITY = CommandTemplate("modify /sys snmp communities delete {{ comm-quali }}", error_map=ERROR_MAP)
SHOW_SNMP_COMMUNITY = CommandTemplate("list /sys snmp communities | grep  community-name", error_map=ERROR_MAP)
