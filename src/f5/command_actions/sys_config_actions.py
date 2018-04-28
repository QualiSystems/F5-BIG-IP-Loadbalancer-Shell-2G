import re

import time
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.cli.session.session_exceptions import SessionException

from f5.command_templates import f5_config_templates


class F5SysConfigActions(object):
    def __init__(self, cli_service, logger):
        self._cli_service = cli_service
        self._logger = logger

    def save_config(self, file_path):
        output = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.SAVE_CONFIG_LOCALLY, timeout=180).execute_command(
            file_path=file_path)
        return output

    def load_config(self, file_path):
        output = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.LOAD_CONFIG_LOCALLY, timeout=180).execute_command(
            file_path=file_path)
        return output

    def install_firmware(self, file_path, boot_volume):
        output = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.INSTALL_FIRMWARE, timeout=180).execute_command(
            file_path=file_path, boot_volume=boot_volume)
        return output

    def show_version_per_volume(self):
        result = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.SHOW_VERSION_PER_VOLUME, timeout=180).execute_command()
        result_iter = re.finditer(
            "HD(?P<volume>\S+)\s+(big[- ]ip|none)\s+"
            "(?P<version>\d+(.\d+)+|none)\s+\S*\s*"
            "(?P<is_running>yes|no)\s+"
            "(?P<status>complete|installing\s*\d+.\d+|testing\s*archive:\s*\S+)?",
            result,
            re.IGNORECASE)

        return {float(x.groupdict().get("volume")): x.groupdict() for x in result_iter}

    def reload_device_to_certain_volume(self, timeout, volume, action_map=None, error_map=None):
        """Reload device
        :param timeout: session reconnect timeout
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        try:
            CommandTemplateExecutor(self._cli_service,
                                    f5_config_templates.RELOAD_TO_CERTAIN_VOLUME,
                                    action_map=action_map,
                                    error_map=error_map).execute_command(volume=volume)

        except SessionException as e:
            pass
        self._logger.info("Device rebooted, starting reconnect")
        time.sleep(300)
        self._cli_service.reconnect(timeout)


class F5SysActions(object):
    def __init__(self, cli_service, logger):
        self._cli_service = cli_service
        self._logger = logger

    def download_config(self, file_path, server_config_url):
        """ Download file from FTP/TFTP Server """

        output = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.DOWNLOAD_FILE_TO_DEVICE, timeout=180).execute_command(
            file_path=file_path,
            url=server_config_url)

        if re.search(r"curl:|[Ff]ail|[Ee]rror]", output, re.IGNORECASE):
            self._logger.error("Failed to download configuration: {}".format(output))
            raise Exception("Failed to download configuration.")

    def upload_config(self, file_path, server_config_url):
        """ Upload file to FTP/TFTP Server """

        output = CommandTemplateExecutor(self._cli_service,
                                         f5_config_templates.UPLOAD_FILE_FROM_DEVICE).execute_command(
            file_path=file_path,
            url=server_config_url)

        if re.search(r"curl:|[Ff]ail|[Ee]rror]", output, re.IGNORECASE):
            self._logger.error("Failed to upload configuration: {}".format(output))
            raise Exception("Failed to upload configuration.")

    def reload_device(self, timeout, action_map=None, error_map=None):
        """Reload device
        :param timeout: session reconnect timeout
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        try:
            CommandTemplateExecutor(self._cli_service,
                                    f5_config_templates.RELOAD,
                                    action_map=action_map,
                                    error_map=error_map).execute_command()

        except SessionException as e:
            self._logger.info("Device rebooted, starting reconnect")
        self._cli_service.reconnect(timeout)

    def copy_config(self, source_boot_volume, target_boot_volume):
        CommandTemplateExecutor(self._cli_service, f5_config_templates.COPY_CONFIG, timeout=180).execute_command(
            src_config=source_boot_volume, dst_config=target_boot_volume)
