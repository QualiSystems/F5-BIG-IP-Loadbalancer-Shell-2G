from cloudshell.f5.flows.f5_autoload_flow import AbstractF5SnmpAutoloadFlow

from f5.load_balancing.autoload.snmp import F5LoadBalancerGenericSNMPAutoload


class F5LoadBalancerSnmpAutoloadFlow(AbstractF5SnmpAutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        """Execute SNMP Autoload flow.

        :param supported_os:
        :param shell_name:
        :param shell_type:
        :param resource_name:
        :return:
        """
        with self._snmp_handler.get_snmp_service() as snmp_service:
            f5_snmp_autoload = F5LoadBalancerGenericSNMPAutoload(
                snmp_handler=snmp_service,
                shell_name=shell_name,
                shell_type=shell_type,
                resource_name=resource_name,
                logger=self._logger,
            )
            return f5_snmp_autoload.discover(supported_os)
