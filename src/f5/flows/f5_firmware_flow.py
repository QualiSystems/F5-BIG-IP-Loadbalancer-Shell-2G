import time

from cloudshell.cli.session.session_exceptions import ExpectedSessionException
from cloudshell.devices.flows.cli_action_flows import LoadFirmwareFlow

from f5.command_actions.sys_config_actions import F5SysConfigActions, F5SysActions


class F5FirmwareFlow(LoadFirmwareFlow):
    RELOAD_TIMEOUT = 500
    INSTALL_CMD_TIMEOUT = 60
    INSTALL_TIMEOUT = 120
    BOOT_TIMEOUT = 60

    def __init__(self, cli_handler, logger, local_storage):
        super(F5FirmwareFlow, self).__init__(cli_handler, logger)
        self._local_storage = local_storage

    def execute_flow(self, path, vrf, timeout):
        filename = path.split("/")[-1]
        local_path = "{}/{}".format(self._local_storage, filename)

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as session:
            sys_actions = F5SysActions(session, logger=self._logger)
            sys_actions.download_config(local_path, path)
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                sys_config_actions = F5SysConfigActions(config_session, logger=self._logger)
                current_volumes_dict = sys_config_actions.show_version_per_volume()
                volume_ids = current_volumes_dict.keys()
                volume_ids.sort()
                boot_volume = round(volume_ids[-1] + 0.1, 1)
                sys_config_actions.install_firmware(filename, boot_volume="HD{}".format(boot_volume))
                time.sleep(self.INSTALL_CMD_TIMEOUT)

                max_retries = 20
                retry = 0
                volume_dict = sys_config_actions.show_version_per_volume().get(boot_volume, {})
                if volume_dict:
                    while ("installing" in volume_dict.get("status") or "testing" in volume_dict.get(
                            "status")) and retry != max_retries:
                        time.sleep(self.INSTALL_TIMEOUT)
                        try:
                            volume_dict = sys_config_actions.show_version_per_volume().get(boot_volume)
                        except ExpectedSessionException as e:
                            pass
                        retry += 1

                if "complete" not in volume_dict.get("status"):
                    self._logger.error(
                        "Failed to load {} firmware".format(filename))
                    raise Exception(
                        "Failed to load {} firmware, Please check logs for details.".format(filename))

                sys_config_actions.reload_device_to_certain_volume(self.RELOAD_TIMEOUT, "HD{}".format(boot_volume))
            with session.enter_mode(self._cli_handler.config_mode) as config_session:
                sys_config_actions = F5SysConfigActions(config_session, logger=self._logger)

                max_boot_retries = 10
                boot_retry = 1
                while "(active)" not in config_session.send_command("").lower() and boot_retry < max_boot_retries:
                    time.sleep(self.BOOT_TIMEOUT)
                    boot_retry += 1

                updated_volumes_dict = sys_config_actions.show_version_per_volume()

                if updated_volumes_dict.get(boot_volume, {}).get("is_running", "no") == "no":
                    self._logger.error(
                        "Failed to load {} firmware, available boot volumes: {}".format(filename, updated_volumes_dict))
                    raise Exception("Failed to update firmware version")
