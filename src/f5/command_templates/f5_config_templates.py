from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict([("\([Yy](es)?/[Nn](o)?\)", lambda session, logger: session.send_line('y', logger))])

SAVE_CONFIG_LOCALLY = CommandTemplate("save /sys ucs {file_path} no-private-key")
LOAD_CONFIG_LOCALLY = CommandTemplate("load /sys ucs {file_path} no-license", action_map=ACTION_MAP)
LOAD_CLUSTER_CONFIG_LOCALLY = CommandTemplate("load /sys ucs {file_path} no-license include-chassis-level-config")

UPLOAD_FILE_FROM_DEVICE = CommandTemplate("curl --upload-file {file_path} {url}")
DOWNLOAD_FILE_TO_DEVICE = CommandTemplate("curl -o {file_path} {url}")
INSTALL_FIRMWARE = CommandTemplate(
    "install sys software image {file_path} volume {boot_volume} create-volume",
    error_map=OrderedDict([("[Ss]yntax\s+[Ee]rror", "Failed to install firmware, Please check logs for details")]))

RELOAD = CommandTemplate("reboot")
RELOAD_TO_CERTAIN_VOLUME = CommandTemplate("reboot volume {volume}")

COPY_CONFIG = CommandTemplate("cpcfg --source={src_config} {dst_config}")
# cpcfg --source=HD1.2 HD1.3

SHOW_VERSION_PER_VOLUME = CommandTemplate("show sys software | grep HD")
