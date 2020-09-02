from aws_cdk.aws_apigatewayv2 import CfnDeployment
from aws_cdk.core import Stack

from b_aws_websocket_api.ws_stage import WsStage


class WsDeployment(CfnDeployment):
    """
    Creates web socket api deployment.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            ws_stage: WsStage
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param ws_stage: Web socket api stage to deploy.
        """
        super().__init__(
            scope=scope,
            id=id,
            api_id=ws_stage.api.ref,
            description='Websocket API deployment.',
            stage_name=ws_stage.stage_name,
        )
