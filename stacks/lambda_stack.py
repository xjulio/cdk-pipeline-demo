from os import path

from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk import aws_apigateway as apigw


class LambdaStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #
        current_dir = path.dirname(__file__)

        lambda_function = aws_lambda.Function(
            self, 'Hanlder',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="handler.main",
            code=aws_lambda.Code.from_asset(path.join(current_dir, 'lambda')),
        )

        gw = apigw.LambdaRestApi(
            self, 'Gateway',
            description="Endpoint for a simple Lambda-powered web service",
            handler=lambda_function.current_version
        )

        self.url_output = cdk.CfnOutput(self, 'Url', value=gw.url)
