from cloudshell.devices.flows.cli_action_flows import SaveConfigurationFlow

from f5.command_actions.sys_config_actions import F5SysConfigActions, F5SysActions


class F5SaveFlow(SaveConfigurationFlow):
    def __init__(self, cli_handler, logger, local_storage):
        super(F5SaveFlow, self).__init__(cli_handler, logger)
        self._local_storage = local_storage

    def execute_flow(self, folder_path, configuration_type, vrf_management_name=None):
        filename = "{}.ucs".format(folder_path.split("/")[-1])
        local_path = "/".join((self._local_storage, filename))
        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                sys_config_actions = F5SysConfigActions(config_session, logger=self._logger)
                sys_config_actions.save_config(local_path)
            sys_actions = F5SysActions(session, logger=self._logger)
            sys_actions.upload_config(local_path, folder_path)
