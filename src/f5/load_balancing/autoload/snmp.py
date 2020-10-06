from collections import OrderedDict

from cloudshell.devices.standards.load_balancing.autoload_structure import (
    GenericChassis,
    GenericPort,
    GenericPowerPort,
    GenericResource,
    GenericServerFarm,
)
from cloudshell.f5.autoload.f5_generic_snmp_autoload import (
    AbstractF5GenericSNMPAutoload,
)

from f5.load_balancing.autoload.structure import F5RealServer
from f5.load_balancing.utils.name_generator import UniqueNameGenerator


class F5LoadBalancerGenericSNMPAutoload(AbstractF5GenericSNMPAutoload):
    @property
    def root_model_class(self):
        return GenericResource

    @property
    def chassis_model_class(self):
        return GenericChassis

    @property
    def port_model_class(self):
        return GenericPort

    @property
    def power_port_model_class(self):
        return GenericPowerPort

    def _build_resources(self):
        """Discover and create all needed resources.

        :return:
        """
        super(F5LoadBalancerGenericSNMPAutoload, self)._build_resources()
        self._get_server_farms()

    def _get_server_farms(self):
        """Get Server Farms.

        :return:
        """
        server_farms_names = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmVirtualServName"
        )
        server_farms_addresses = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmVirtualServAddr"
        )
        server_farms_addresses_type = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmVirtualServAddrType"
        )
        server_farms_ports = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmVirtualServPort"
        )
        server_farms_pools = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmVirtualServDefaultPool"
        )
        servers_pools = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmPoolMemberPoolName"
        )
        server_pools_algorithm = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmPoolLbMode"
        )
        server_pools_algorithm_names = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmPoolName"
        )
        server_pools_members = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmPoolMemberStatNodeName"
        )
        servers_names = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmNodeAddrName"
        )
        servers_addresses = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmNodeAddrAddr"
        )
        servers_addresses_type = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmNodeAddrAddrType"
        )
        servers_monitors = self.snmp_handler.get_table(
            "F5-BIGIP-LOCAL-MIB", "ltmNodeAddrAddrType"
        )
        servers_pools = OrderedDict(servers_pools)

        farm_names_generator = UniqueNameGenerator()

        for farm_idx, (farm_id, farm_value) in enumerate(server_farms_names.items()):
            server_farm_name = farm_value.get("ltmVirtualServName")
            if not server_farm_name:
                continue

            server_farm_port = server_farms_ports.get(farm_id, {}).get(
                "ltmVirtualServPort"
            )
            server_farm_pool = server_farms_pools.get(farm_id, {}).get(
                "ltmVirtualServDefaultPool"
            )
            farm_name = server_farm_name.strip("/").replace("/", "_")
            farm_name = farm_names_generator.get_unique_name(farm_name)

            server_farm = GenericServerFarm(
                shell_name=self.shell_name,
                name="Server Farm {}".format(farm_name),
                unique_id="{}.{}.{}".format(
                    self.resource_name, "server_farm", farm_idx
                ),
            )
            server_farm.virtual_server_address = self._get_ip_address(
                server_farms_addresses.get(farm_id, {}).get("ltmVirtualServAddr"),
                server_farms_addresses_type.get(farm_id, {}).get(
                    "ltmVirtualServAddrType"
                ),
            )
            server_farm.virtual_server_port = server_farm_port
            server_farm.algorithm = ""
            self.resource.add_sub_resource(farm_idx, server_farm)

            if not server_farm_pool:
                continue

            # todo: rework this with one iteration, not for each server farm
            srvr_names_generator = UniqueNameGenerator()
            for server_idx, (servers_pool_id, servers_pool_value) in enumerate(
                servers_pools.iteritems()
            ):
                if server_farm_pool == servers_pool_value.get("ltmPoolMemberPoolName"):
                    algorithm_key = [
                        k
                        for k, v in server_pools_algorithm_names.iteritems()
                        if server_farm_pool == v.get("ltmPoolName")
                    ]
                    server_farm.algorithm = (
                        server_pools_algorithm.get(algorithm_key[0])
                        .get("ltmPoolLbMode")
                        .replace("'", "")
                    )
                    server_node = server_pools_members.get(servers_pool_id).get(
                        "ltmPoolMemberStatNodeName"
                    )
                    server_id = [
                        k
                        for k, v in servers_names.iteritems()
                        if server_node == v.get("ltmNodeAddrName")
                    ][0]
                    if server_id:
                        server_name = (
                            servers_names.get(server_id, {})
                            .get("ltmNodeAddrName")
                            .strip("/")
                            .replace("/", "_")
                        )
                        server_name = srvr_names_generator.get_unique_name(server_name)

                        unique_id = "{}.{}.{}.{}".format(
                            self.resource_name, "real_server", farm_idx, server_idx
                        )
                        real_server = F5RealServer(
                            name="Real Server {}".format(server_name),
                            shell_name=self.shell_name,
                            unique_id=unique_id,
                        )

                        real_server.address = self._get_ip_address(
                            servers_addresses.get(server_id, {}).get("ltmNodeAddrAddr"),
                            servers_addresses_type.get(server_id, {}).get(
                                "ltmNodeAddrAddrType"
                            ),
                        )
                        real_server.monitors = servers_monitors.get(server_id, {}).get(
                            "ltmNodeAddrMonitorRule"
                        )
                        server_farm.add_sub_resource(server_idx, real_server)
