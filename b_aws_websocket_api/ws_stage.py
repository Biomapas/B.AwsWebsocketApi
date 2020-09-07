from typing import Optional, Dict, Any

from aws_cdk.aws_apigatewayv2 import CfnStage
from aws_cdk.aws_logs import RetentionDays, LogGroup
from aws_cdk.core import CfnOutput, RemovalPolicy, Stack

from b_aws_websocket_api.ws_api import WsApi


class WsStage(CfnStage):
    """
    Creates a web socket api stage.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            ws_api: WsApi,
            stage_name: str,
            access_log_settings: Optional[CfnStage.AccessLogSettingsProperty] = None,
            create_default_access_log_settings: Optional[bool] = None,
            auto_deploy: Optional[bool] = None,
            client_certificate_id: Optional[str] = None,
            default_route_settings: Optional[CfnStage.RouteSettingsProperty] = None,
            description: Optional[str] = None,
            route_settings: Optional[Dict[str, Any]] = None,
            stage_variables: Optional[Dict[str, Any]] = None,
            tags: Optional[Dict[str, Any]] = None,
            *args,
            **kwargs
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation-equivalent stack.
        :param id: AWS-CDK-specific id.
        :param ws_api: The web socket API for with this stage should be created.
        :param stage_name: The stage name. Stage names can only contain alphanumeric characters, hyphens,
        and underscores. Maximum length is 128 characters.
        :param access_log_settings: Settings for logging access in this stage.
        :param create_default_access_log_settings: Indicate whether to create default access log settings.
        :param auto_deploy: Specifies whether updates to an API automatically trigger a new deployment.
        The default value is false.
        :param client_certificate_id: The identifier of a client certificate for a Stage.
        :param default_route_settings: The default route settings for the stage.
        :param description: The description for the API stage.
        :param route_settings: Route settings for the stage.
        :param stage_variables: A map that defines the stage variables for a Stage. Variable names can have
        alphanumeric and underscore characters, and the values must match [A-Za-z0-9-._~:/?#&=,]+.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        """
        self.__scope = scope
        self.__ws_api = ws_api

        default_route_settings = default_route_settings or CfnStage.RouteSettingsProperty(
            data_trace_enabled=True,
            detailed_metrics_enabled=True,
            logging_level='INFO',
        )

        if access_log_settings and create_default_access_log_settings:
            raise ValueError('Access log settings supplied. Can not request to create default ones.')

        if create_default_access_log_settings:
            log_group = LogGroup(
                scope=scope,
                id=f'{id}LogGroup',
                log_group_name=f'{id}LogGroup',
                removal_policy=RemovalPolicy.DESTROY,
                retention=RetentionDays.ONE_MONTH
            )

            access_log_settings = CfnStage.AccessLogSettingsProperty(
                destination_arn=log_group.log_group_arn,
                format=(
                    "{"
                    "\"requestId\":\"$context.requestId\", "
                    "\"ip\": \"$context.identity.sourceIp\", "
                    "\"caller\":\"$context.identity.caller\", "
                    "\"user\":\"$context.identity.user\","
                    "\"requestTime\":\"$context.requestTime\", "
                    "\"eventType\":\"$context.eventType\","
                    "\"routeKey\":\"$context.routeKey\", "
                    "\"status\":\"$context.status\","
                    "\"connectionId\":\"$context.connectionId\""
                    "}"
                )
            )

        super().__init__(
            scope=scope,
            id=id,
            api_id=ws_api.ref,
            stage_name=stage_name,
            access_log_settings=access_log_settings,
            auto_deploy=auto_deploy,
            client_certificate_id=client_certificate_id,
            default_route_settings=default_route_settings,
            description=description,
            route_settings=route_settings,
            stage_variables=stage_variables,
            tags=tags,
            *args,
            **kwargs
        )

        CfnOutput(
            scope=scope,
            id=f'{ws_api.name}Url',
            value=self.ws_url,
            description='A websocket URL.',
            export_name=f'{ws_api.name}Url'
        )

        CfnOutput(
            scope=scope,
            id=f'{ws_api.name}Id',
            value=self.api_id,
            description='A websocket ID.',
            export_name=f'{ws_api.name}Id'
        )

        CfnOutput(
            scope=scope,
            id=f'{ws_api.name}ConnectionUrl',
            value=self.connection_url,
            description='A websocket connection URL.',
            export_name=f'{ws_api.name}ConnectionUrl'
        )

    @property
    def ws_url(self):
        return f'wss://{self.api.ref}.execute-api.{self.__scope.region}.amazonaws.com/{self.ref}'

    @property
    def connection_url(self):
        return f'https://{self.api.ref}.execute-api.{self.__scope.region}.amazonaws.com/{self.ref}'

    @property
    def api_arn(self):
        return f'arn:aws:apigateway:{self.__scope.region}::/restapis/{self.api.ref}/stages/{self.stage_name}'

    @property
    def connections_url(self):
        return f'arn:aws:execute-api:{self.__scope.region}:{self.__scope.account}:{self.api.ref}/{self.stage_name}/POST/@connections/*'

    @property
    def api(self):
        """
        Api resource getter property.

        :return: Websocket API resource.
        """
        return self.__ws_api
