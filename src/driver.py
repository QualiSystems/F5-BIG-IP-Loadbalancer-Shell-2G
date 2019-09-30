from cloudshell.devices.standards.networking.configuration_attributes_structure import \
    create_networking_resource_from_context
from f5.cli.f5_cli_handler import F5CliHandler as CliHandler
from cloudshell.devices.driver_helper import get_logger_with_thread_id, get_api, get_cli
from cloudshell.devices.driver_helper import parse_custom_commands
from f5.snmp.f5_snmp_handler import F5SnmpHandler as SNMPHandler
from f5.runners.f5_autoload_runner import \
    F5AutoloadRunner as AutoloadRunner

from f5.runners.f5_configuration_runner import F5ConfigurationRunner as ConfigurationRunner
from f5.runners.f5_firmware_runner import F5FirmwareRunner as FirmwareRunner
from cloudshell.devices.runners.run_command_runner import RunCommandRunner as CommandRunner
from cloudshell.devices.runners.state_runner import StateRunner as StateRunner
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface


class F5BigIpLoadbalancerShell2GDriver(ResourceDriverInterface):
    SUPPORTED_OS = ["BIG[ -]?IP"]
    SHELL_NAME = "F5 BigIp LB Shell 2G"

    def __init__(self):
        super(F5BigIpLoadbalancerShell2GDriver, self).__init__()
        self._cli = None

    def initialize(self, context):
        """Initialize method

        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)
        return 'Finished initializing'

    @GlobalLock.lock
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: response
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)
        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        snmp_handler = SNMPHandler(resource_config, logger, api, cli_handler)

        autoload_operations = AutoloadRunner(logger=logger,
                                             resource_config=resource_config,
                                             snmp_handler=snmp_handler)
        logger.info('Autoload started')
        response = autoload_operations.discover()
        logger.info('Autoload completed')
        return response

    def run_custom_command(self, context, custom_command):
        """Send custom command

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        send_command_operations = CommandRunner(logger=logger, cli_handler=cli_handler)

        response = send_command_operations.run_custom_command(custom_command=parse_custom_commands(custom_command))

        return response

    def run_custom_config_command(self, context, custom_command):
        """Send custom command in configuration mode

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: result
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        send_command_operations = CommandRunner(logger=logger, cli_handler=cli_handler)

        result_str = send_command_operations.run_custom_config_command(
            custom_command=parse_custom_commands(custom_command))

        return result_str

    def health_check(self, context):
        """Performs device health check

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return: Success or Error message
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)
        cli_handler = CliHandler(self._cli, resource_config, logger, api)

        state_operations = StateRunner(logger=logger, api=api, resource_config=resource_config, cli_handler=cli_handler)
        return state_operations.health_check()

    def cleanup(self):
        pass

    def save(self, context, folder_path, configuration_type, vrf_management_name):
        """Save selected file to the provided destination

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param configuration_type: source file, which will be saved
        :param folder_path: destination path where file will be saved
        :param vrf_management_name: VRF management Name
        :return str saved configuration file name:
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        if not configuration_type:
            configuration_type = 'running'

        if not vrf_management_name:
            vrf_management_name = resource_config.vrf_management_name

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        configuration_operations = ConfigurationRunner(cli_handler=cli_handler,
                                                       logger=logger,
                                                       resource_config=resource_config,
                                                       api=api)
        logger.info('Save started')
        response = configuration_operations.save(folder_path=folder_path, configuration_type=configuration_type,
                                                 vrf_management_name=vrf_management_name)
        logger.info('Save completed')
        return response

    @GlobalLock.lock
    def restore(self, context, path, configuration_type, restore_method, vrf_management_name):
        """Restore selected file to the provided destination

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param path: source config file
        :param configuration_type: running or startup configs
        :param restore_method: append or override methods
        :param vrf_management_name: VRF management Name
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        if not configuration_type:
            configuration_type = 'running'

        if not restore_method:
            restore_method = 'override'

        if not vrf_management_name:
            vrf_management_name = resource_config.vrf_management_name

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        configuration_operations = ConfigurationRunner(cli_handler=cli_handler,
                                                       logger=logger,
                                                       resource_config=resource_config,
                                                       api=api)
        logger.info('Restore started')
        configuration_operations.restore(path=path, restore_method=restore_method,
                                         configuration_type=configuration_type,
                                         vrf_management_name=vrf_management_name)
        logger.info('Restore completed')

    def orchestration_save(self, context, mode, custom_params):
        """

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param mode: mode
        :param custom_params: json with custom save parameters
        :return str response: response json
        """

        if not mode:
            mode = 'shallow'

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        configuration_operations = ConfigurationRunner(cli_handler=cli_handler,
                                                       logger=logger,
                                                       resource_config=resource_config,
                                                       api=api)

        logger.info('Orchestration save started')
        response = configuration_operations.orchestration_save(mode=mode, custom_params=custom_params)
        logger.info('Orchestration save completed')
        return response

    def orchestration_restore(self, context, saved_artifact_info, custom_params):
        """

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param saved_artifact_info: OrchestrationSavedArtifactInfo json
        :param custom_params: json with custom restore parameters
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        configuration_operations = ConfigurationRunner(cli_handler=cli_handler,
                                                       logger=logger,
                                                       resource_config=resource_config,
                                                       api=api)

        logger.info('Orchestration restore started')
        configuration_operations.orchestration_restore(saved_artifact_info=saved_artifact_info,
                                                       custom_params=custom_params)
        logger.info('Orchestration restore completed')

    @GlobalLock.lock
    def load_firmware(self, context, path, vrf_management_name):
        """Upload and updates firmware on the resource

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param path: full path to firmware file, i.e. tftp://10.10.10.1/firmware.tar
        :param vrf_management_name: VRF management Name
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        if not vrf_management_name:
            vrf_management_name = resource_config.vrf_management_name

        cli_handler = CliHandler(self._cli, resource_config, logger, api)

        logger.info('Start Load Firmware')
        firmware_operations = FirmwareRunner(cli_handler=cli_handler, logger=logger)
        response = firmware_operations.load_firmware(path=path, vrf_management_name=vrf_management_name)
        logger.info('Finish Load Firmware: {}'.format(response))

    def shutdown(self, context):
        """ Shutdown device

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :return:
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_networking_resource_from_context(shell_name=self.SHELL_NAME,
                                                                  supported_os=self.SUPPORTED_OS,
                                                                  context=context)

        cli_handler = CliHandler(self._cli, resource_config, logger, api)
        state_operations = StateRunner(logger=logger, api=api, resource_config=resource_config, cli_handler=cli_handler)

        return state_operations.shutdown()


if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = "192.168.73.149"
    user = "root"
    password = "admin"
    cs_address = "192.168.85.44"

    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext(*(None, ) * 4)
    context.resource = ResourceContextDetails(*(None, ) * 13)
    context.resource.name = 'F5 BIG-IP Firewall 2G'
    context.resource.fullname = 'F5 BIG-IP Firewall 2G'
    context.reservation = ReservationContextDetails(*(None, ) * 7)
    context.reservation.reservation_id = '0cc17f8c-75ba-495f-aeb5-df5f0f9a0e97'
    context.resource.attributes = {}
    context.resource.address = address
    context.resource.family = "CS_LoadBalancer"


    for attr, val in [("User", user),
                      ("Password", password),
                      ("Sessions Concurrency Limit", 1),
                      ("SNMP Read Community", "public"),
                      ("SNMP Version", "2"),
                      ("Enable SNMP", "False"),
                      ("Disable SNMP", "False"),
                      ("CLI Connection Type", "ssh")]:

        context.resource.attributes['{}.{}'.format(F5BigIpLoadbalancerShell2GDriver.SHELL_NAME, attr)] = val

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = cs_address

    dr = F5BigIpLoadbalancerShell2GDriver()
    dr.initialize(context)

    with mock.patch('__main__.get_api') as get_api:
        get_api.return_value = type('api', (object,), {
            'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        result = dr.get_inventory(context=context)

        for res in result.resources:
            print res.__dict__