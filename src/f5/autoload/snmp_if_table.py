import re
from f5.autoload.snmp_if_entity import SnmpIfEntity
from f5.autoload.snmp_port_attr_tables import SnmpPortAttrTables


class SnmpIfTable(object):
    def __init__(self, snmp_handler, logger):
        self._snmp = snmp_handler
        self._logger = logger
        self._load_snmp_tables()
        self._if_entities_dict = dict()
        self.port_attributes_snmp_tables = SnmpPortAttrTables(snmp_handler, logger)

    @property
    def if_entities(self):
        if not self._if_entities_dict:
            self._get_if_entities()
        return self._if_entities_dict.values()

    def _get_if_entities(self):
        for index in self._if_table.keys():
            self._if_entities_dict[index] = SnmpIfEntity(snmp_handler=self._snmp, logger=self._logger,
                                                         index=index,
                                                         port_attributes_snmp_tables=self.port_attributes_snmp_tables)

    def _load_snmp_tables(self):
        """ Load all cisco required snmp tables

        :return:
        """

        self._logger.info('Start loading MIB tables:')
        self._if_table = self._snmp.get_table('IF-MIB', "ifDescr")
        self._logger.info('ifIndex table loaded')

        self._logger.info('MIB Tables loaded successfully')

    def get_if_index_from_port_name(self, port_name, port_filter_list):
        for interface in self.if_entities:
            if not re.search("ethernet|other", interface.if_type, re.IGNORECASE):
                continue
            if re.search(r"^(?!.*{0}){1}$".format(port_filter_list, port_name),
                         interface.if_name, re.IGNORECASE):
                return interface
