import hashlib
from typing import Optional, Mapping, List

from aws_cdk.aws_ec2 import ISecurityGroup, IVpc, SubnetSelection
from aws_cdk.aws_iam import PolicyStatement, IRole
from aws_cdk.aws_lambda import *
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.aws_sqs import IQueue
from aws_cdk.core import Stack, Duration
from jsii import Number


class WsFunction(Function):
    """
    Creates a lambda function which is API Gateway friendly.
    """

    def __init__(
            self,
            scope: Stack,
            id: str,
            code: Code,
            handler: str,
            runtime: Runtime,
            allow_all_outbound: Optional[bool] = None,
            current_version_options: Optional[VersionOptions] = None,
            dead_letter_queue: Optional[IQueue] = None,
            dead_letter_queue_enabled: Optional[bool] = None,
            description: Optional[str] = None,
            environment: Optional[Mapping[str, str]] = None,
            events: Optional[List[IEventSource]] = None,
            function_name: Optional[str] = None,
            initial_policy: Optional[List[PolicyStatement]] = None,
            layers: Optional[List[ILayerVersion]] = None,
            log_retention: Optional[RetentionDays] = None,
            log_retention_role: Optional[IRole] = None,
            memory_size: Optional[Number] = None,
            reserved_concurrent_executions: Optional[Number] = None,
            role: Optional[IRole] = None,
            security_groups: Optional[List[ISecurityGroup]] = None,
            timeout: Optional[Duration] = None,
            tracing: Optional[Tracing] = None,
            vpc: Optional[IVpc] = None,
            vpc_subnets: Optional[SubnetSelection] = None,
            max_event_age: Optional[Duration] = None,
            on_failure: Optional[IDestination] = None,
            on_success: Optional[IDestination] = None,
            retry_attempts: Optional[Number] = None,
            *args,
            **kwargs
    ) -> None:
        """
        Constructor.

        :param scope: Cloud formation stack.
        :param id: AWS-CDK-specific id.
        :param code: The code for the function.
        :param handler: The name of the method within your code that Lambda calls to execute your function.
        :param runtime: The identifier of the function's runtime.
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic.
        :param current_version_options: Current version options.
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled.
        :param dead_letter_queue_enabled: Enabled DLQ.
        :param description: A description of the function.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions.
        :param events: Event sources for this function.
        :param function_name: A name for the function.
        :param initial_policy: Initial policy statements to add to the created Lambda Role.
        :param layers: A list of layers to add to the function's execution environment.
        :param log_retention: The number of days log events are kept in CloudWatch Logs.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets
        the retention policy.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve
        for the function.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function.
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function.
        :param vpc: VPC network to place Lambda network interfaces.
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing.
        :param on_failure: The destination for failed invocations.
        :param on_success: The destination for successful invocations.
        :param retry_attempts: The maximum number of times to retry when the function returns an error.
        :param args: Additional arguments.
        :param kwargs: Additional named arguments.
        """
        self.__id = id
        self.__name = function_name

        super().__init__(
            scope=scope,
            id=id,
            code=code,
            handler=handler,
            runtime=runtime,
            allow_all_outbound=allow_all_outbound,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            description=description,
            environment=environment,
            events=events,
            function_name=function_name,
            initial_policy=initial_policy,
            layers=layers,
            log_retention=log_retention,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
            *args,
            **kwargs
        )

        CfnPermission(
            scope=scope,
            id=f'{function_name}WsApiInvokePermission',
            action='lambda:InvokeFunction',
            function_name=self.function_name,
            principal='apigateway.amazonaws.com',
        )

    @property
    def hash(self):
        hashable = (
               self.__id +
               self.__name
        ).encode('utf-8')

        return hashlib.sha256(hashable).hexdigest()
