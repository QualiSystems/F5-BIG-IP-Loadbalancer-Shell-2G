from cloudshell.devices.runners.firmware_runner import FirmwareRunner

from f5.flows.f5_firmware_flow import F5FirmwareFlow


class F5FirmwareRunner(FirmwareRunner):
    LOCAL_STORAGE = "/shared/images"

    def __init__(self, logger, cli_handler):
        super(F5FirmwareRunner, self).__init__(logger, cli_handler)

    @property
    def load_firmware_flow(self):
        return F5FirmwareFlow(self.cli_handler, self._logger, self.LOCAL_STORAGE)
