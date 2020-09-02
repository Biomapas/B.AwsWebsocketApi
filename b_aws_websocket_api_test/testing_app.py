import os
import sys

from aws_cdk.core import App

from b_aws_websocket_api_test.testing_infrastructure import TestingInfrastructure

# Append python package root path so resources could be imported.
# Failing to add these few lines below will result in a "module not found" error.
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)


app = App()
TestingInfrastructure(app)
app.synth()
