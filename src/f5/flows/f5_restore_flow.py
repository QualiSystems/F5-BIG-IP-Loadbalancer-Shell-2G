from cloudshell.devices.flows.cli_action_flows import RestoreConfigurationFlow

from f5.command_actions.sys_config_actions import F5SysConfigActions, F5SysActions


class F5RestoreFlow(RestoreConfigurationFlow):
    def __init__(self, cli_handler, logger, local_storage):
        super(F5RestoreFlow, self).__init__(cli_handler, logger)
        self._local_storage = local_storage

    def execute_flow(self, path, restore_method, configuration_type, vrf_management_name):
        filename = path.split("/")[-1]
        local_path = "{}/{}".format(self._local_storage, filename)

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            sys_actions = F5SysActions(session, logger=self._logger)
            sys_actions.download_config(local_path, path)
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                sys_config_actions = F5SysConfigActions(config_session, logger=self._logger)
                sys_config_actions.load_config(local_path)
            sys_actions.reload_device(120)
