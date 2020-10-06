from cloudshell.f5.runners.f5_autoload_runner import AbstractF5AutoloadRunner

from f5.load_balancing.flows.autoload import F5LoadBalancerSnmpAutoloadFlow


class F5LoadBalancerAutoloadRunner(AbstractF5AutoloadRunner):
    @property
    def autoload_flow(self):
        return F5LoadBalancerSnmpAutoloadFlow(
            snmp_handler=self.snmp_handler, logger=self._logger
        )
