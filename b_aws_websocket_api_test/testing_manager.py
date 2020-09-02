import logging
import os
import subprocess
from subprocess import CalledProcessError

from biomapas_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class TestingManager:
    """
    Test manager class which prepares infrastructure for tests.
    After tests are finished, destroys the infrastructure.
    """
    __TEST_PROFILE_KEY = 'BIOMAPAS_AWS_API_WS_TEST_PROFILE'
    TEST_PROFILE = os.environ[__TEST_PROFILE_KEY]

    # Ensure region supports the resources we are going to create.
    # For example, eu-central-1 supports websocket APIs.
    AWS_REGION_NAME = 'eu-central-1'

    __BOOTSTRAP_COMMAND = f'cdk bootstrap --profile {TEST_PROFILE}'
    __CREATE_COMMAND = f'cdk deploy * --profile {TEST_PROFILE} --require-approval never'
    __DELETE_COMMAND = f'cdk destroy * --profile {TEST_PROFILE} --require-approval never -f'

    __CDK_APP_PATH = os.path.dirname(os.path.abspath(__file__))

    CLOUDFORMATION_STACK_OUTPUTS = {}

    @staticmethod
    def bootstrap() -> None:
        subprocess.check_call(['pip', 'install', 'websockets', 'boto3'])

    @staticmethod
    def prepare_infrastructure() -> None:
        TestingManager.bootstrap_infrastrucutre()
        TestingManager.destroy_infrastructure()

        try:
            TestingManager.create_infrastructure()
        except CalledProcessError as ex:
            TestingManager.destroy_infrastructure()
            raise ex

        TestingManager.__set_outputs()

    @staticmethod
    def bootstrap_infrastrucutre() -> None:
        # Bootstrap infrastructure.
        output = ContinuousSubprocess(TestingManager.__BOOTSTRAP_COMMAND).execute(path=TestingManager.__CDK_APP_PATH)
        for line in output: print(line)

    @staticmethod
    def create_infrastructure() -> None:
        # Create fresh infrastructure.
        output = ContinuousSubprocess(TestingManager.__CREATE_COMMAND).execute(path=TestingManager.__CDK_APP_PATH)
        for line in output: print(line)

    @staticmethod
    def destroy_infrastructure() -> None:
        # Delete infrastructure.
        output = ContinuousSubprocess(TestingManager.__DELETE_COMMAND).execute(path=TestingManager.__CDK_APP_PATH)
        for line in output: print(line)

    @staticmethod
    def __set_outputs() -> None:
        import boto3

        # We expect one stack. And the name of the stack is an output of a "cdk list" command.
        output = subprocess.check_output(
            f'cdk list --profile {TestingManager.TEST_PROFILE}',
            shell=True,
            cwd=TestingManager.__CDK_APP_PATH
        ).decode().strip()

        session = boto3.session.Session(profile_name=TestingManager.TEST_PROFILE)
        response = session.client('cloudformation', region_name=TestingManager.AWS_REGION_NAME).describe_stacks(
            StackName=output)
        stack_outputs = response['Stacks'][0]['Outputs']

        stack_outputs_container = {}

        for output in stack_outputs:
            key = output['OutputKey'] or output['ExportName']
            value = output['OutputValue']

            stack_outputs_container[key] = value

        TestingManager.CLOUDFORMATION_STACK_OUTPUTS = stack_outputs_container
