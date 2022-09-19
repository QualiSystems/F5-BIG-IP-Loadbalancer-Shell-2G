from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_pool_manager import SessionPoolManager
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.orchestration_save_restore import OrchestrationSaveRestore
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.command.basic_flow import RunCommandFlow
from cloudshell.shell.standards.load_balancer.autoload_model import (
    LoadBalancerResourceModel,
)
from cloudshell.shell.standards.load_balancer.driver_interface import (
    LoadBalancerResourceDriverInterface,
)
from cloudshell.shell.standards.load_balancer.resource_config import (
    LoadBalancerResourceConfig,
)
from cloudshell.snmp.snmp_configurator import EnableDisableSnmpConfigurator

from cloudshell.f5.cli.f5_cli_configurator import F5CliConfigurator
from cloudshell.f5.flows.f5_autoload_flow import BigIPAutoloadFlow
from cloudshell.f5.flows.f5_configuration_flow import F5ConfigurationFlow
from cloudshell.f5.flows.f5_enable_disable_snmp_flow import F5EnableDisableSnmpFlow
from cloudshell.f5.flows.f5_state_flow import F5StateFlow

if TYPE_CHECKING:
    from cloudshell.shell.core.driver_context import (
        AutoLoadCommandContext,
        AutoLoadDetails,
        InitCommandContext,
        ResourceCommandContext,
    )


class F5BigIPLoadBalancerShell2GDriver(
    ResourceDriverInterface, LoadBalancerResourceDriverInterface
):
    SUPPORTED_OS = ["BIG[ -]?IP"]
    SHELL_NAME = "F5 BIG IP Loadbalancer 2G"

    def __init__(self):
        self._cli = None

    def initialize(self, context: InitCommandContext) -> str:
        """Initialize the driver session.

        :param context: the context the command runs on
        """
        resource_config = LoadBalancerResourceConfig.from_context(
            self.SHELL_NAME, context
        )
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = CLI(
            SessionPoolManager(max_pool_size=session_pool_size, pool_timeout=100)
        )
        return "Finished initializing"

    @GlobalLock.lock
    def get_inventory(self, context: AutoLoadCommandContext) -> AutoLoadDetails:
        """Return device structure with all standard attributes.

        :param context: ResourceCommandContext object with all
          Resource Attributes inside
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME, context, api, self.SUPPORTED_OS
            )

            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)
            enable_disable_snmp_flow = F5EnableDisableSnmpFlow(cli_configurator, logger)
            snmp_configurator = EnableDisableSnmpConfigurator(
                enable_disable_snmp_flow, resource_config, logger
            )

            resource_model = LoadBalancerResourceModel.from_resource_config(
                resource_config
            )

            autoload_operations = BigIPAutoloadFlow(snmp_configurator, logger)
            logger.info("Autoload started")
            response = autoload_operations.discover(self.SUPPORTED_OS, resource_model)
            logger.info("Autoload completed")
            return response

    def run_custom_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Executes a custom command on the device.

        :param context: The context object
         for the command with resource and reservation info
        :param custom_command: The command to run
        :return: the command result text
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            send_command_operations = RunCommandFlow(logger, cli_configurator)
            response = send_command_operations.run_custom_command(custom_command)
            return response

    def run_custom_config_command(
        self, context: ResourceCommandContext, custom_command: str
    ) -> str:
        """Executes a custom command on the device in configuration mode.

        :param context: The context object
         for the command with resource and reservation info
        :param custom_command: The command to run
        :return: the command result text
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            send_command_operations = RunCommandFlow(logger, cli_configurator)
            result_str = send_command_operations.run_custom_config_command(
                custom_command
            )
            return result_str

    def save(
        self,
        context: ResourceCommandContext,
        folder_path: str,
        configuration_type: str,
        vrf_management_name: str,
    ) -> str:
        """Save a configuration file to the provided destination.

        :param context: The context object
         for the command with resource and reservation info
        :param folder_path: The path to the folder in which the configuration
         file will be saved
        :param configuration_type: startup or running config
        :return The configuration file name
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            configuration_operations = F5ConfigurationFlow(
                resource_config, logger, cli_configurator
            )
            logger.info("Save started")
            response = configuration_operations.save(
                folder_path=folder_path,
                configuration_type=configuration_type,
                vrf_management_name=vrf_management_name,
            )
            logger.info("Save completed")
            return response

    @GlobalLock.lock
    def restore(
        self,
        context: ResourceCommandContext,
        path: str,
        configuration_type: str,
        restore_method: str,
        vrf_management_name: str,
    ) -> None:
        """Restores a configuration file.

        :param context: The context object for the command
         with resource and reservation info
        :param path: The path to the configuration file, including the
         configuration file name
        :param restore_method: Determines whether the restore should append or
         override the current configuration
        :param configuration_type: Specify whether the file should update
         the startup or running config
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            configuration_operations = F5ConfigurationFlow(
                resource_config, logger, cli_configurator
            )
            logger.info("Restore started")
            configuration_operations.restore(
                path=path,
                restore_method=restore_method,
                configuration_type=configuration_type,
                vrf_management_name=vrf_management_name,
            )
            logger.info("Restore completed")

    def shutdown(self, context: ResourceCommandContext) -> str:
        """Sends a graceful shutdown to the device.

        :param context: The context object
         for the command with resource and reservation info
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            state_operations = F5StateFlow(
                logger, resource_config, cli_configurator, api
            )
            return state_operations.shutdown()

    def orchestration_save(
        self, context: ResourceCommandContext, mode: str, custom_params: str
    ) -> str:
        """Saves the Shell state and returns a description of the saved artifacts.

        This command is intended for API use only by sandbox orchestration
        scripts to implement a save and restore workflow
        :param context: the context object containing
         resource and reservation info
        :param mode: Snapshot save mode, can be one of two values
         'shallow' (default) or 'deep'
        :param custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            configuration_operations = F5ConfigurationFlow(
                resource_config, logger, cli_configurator
            )

            logger.info("Orchestration save started")

            response = configuration_operations.orchestration_save(
                mode=mode, custom_params=custom_params
            )
            response_json = OrchestrationSaveRestore(
                logger, resource_config.name
            ).prepare_orchestration_save_result(response)
            logger.info("Orchestration save completed")
            return response_json

    def orchestration_restore(self, context, saved_artifact_info, custom_params):
        """Restores a saved artifact previously saved by this Shell.

        :param ResourceCommandContext context: The context object
         for the command with resource and reservation info
        :param str saved_artifact_info: A JSON string representing the state
         to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            flow = F5ConfigurationFlow(resource_config, logger, cli_configurator)

            restore_params = OrchestrationSaveRestore(
                logger, resource_config.name
            ).parse_orchestration_save_result(saved_artifact_info)

            logger.info("Orchestration restore started")
            flow.restore(**restore_params)
            logger.info("Orchestration restore completed")

    def health_check(self, context: ResourceCommandContext) -> str:
        """Checks if the device is up and connectable.

        :param context: ResourceCommandContext object
         with all Resource Attributes inside
        :return: Success or fail message
        """
        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()

            resource_config = LoadBalancerResourceConfig.from_context(
                self.SHELL_NAME,
                context,
                api,
                self.SUPPORTED_OS,
            )
            cli_configurator = F5CliConfigurator(self._cli, resource_config, logger)

            state_operations = F5StateFlow(
                logger, resource_config, cli_configurator, api
            )
            return state_operations.health_check()

    def cleanup(self):
        """Destroy the driver session.

        This function is called everytime a driver instance is destroyed.
        This is a good place to close any open sessions, finish writing to log files
        """
        pass
