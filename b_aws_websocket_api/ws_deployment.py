from typing import Optional

from aws_cdk.core import Stack, Construct
from b_stage_deployment.function import StageDeploymentSingletonFunction
from b_stage_deployment.resource import StageDeploymentResource
from b_aws_websocket_api.ws_stage import WsStage


class WsDeployment(Construct):
    """
    Creates web socket api deployment.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            ws_stage: WsStage,
            description: Optional[str] = None
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param ws_stage: Web socket api stage to deploy.
        :param description: Deployment description.
        """
        deployment_func = StageDeploymentSingletonFunction(
            scope=scope,
            name=f'{id}Function'
        )

        StageDeploymentResource(
            scope=scope,
            resource_name=f'{id}Resource',
            deployment_function=deployment_func,
            api_id=ws_stage.api_id,
            stage_name=ws_stage.stage_name,
            description=description or f'Deployment for {ws_stage.stage_name}.'
        )

        super().__init__(
            scope=scope,
            id=id,
        )
