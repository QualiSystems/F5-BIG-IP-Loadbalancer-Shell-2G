from cloudshell.devices.runners.configuration_runner import ConfigurationRunner

from f5.flows.f5_restore_flow import F5RestoreFlow
from f5.flows.f5_save_flow import F5SaveFlow


class F5ConfigurationRunner(ConfigurationRunner):
    DEFAULT_CONFIG_STORAGE = "/var/local/ucs"

    @property
    def restore_flow(self):
        return F5RestoreFlow(cli_handler=self.cli_handler, logger=self._logger,
                             local_storage=self.DEFAULT_CONFIG_STORAGE)

    @property
    def file_system(self):
        return "/var/local/ucs"

    @property
    def save_flow(self):
        return F5SaveFlow(cli_handler=self.cli_handler, logger=self._logger, local_storage=self.DEFAULT_CONFIG_STORAGE)
