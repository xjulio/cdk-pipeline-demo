from aws_cdk import core

from stacks.lambda_stack import LambdaStack


class ServiceStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = LambdaStack(self, 'Lambda')

        self.url_output = service.url_output
