from os import path

import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_codedeploy as codedeploy
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda
from aws_cdk import core as core


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #
        current_dir = path.dirname(__file__)

        lambda_function = aws_lambda.Function(
            self, 'Hanlder',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="handler.main",
            code=aws_lambda.Code.from_asset(path.join(current_dir, 'lambda')),
        )

        alias = aws_lambda.Alias(
            self, 'HandlerAlias',
            alias_name='Current',
            version=lambda_function.current_version,
        )

        gw = apigw.LambdaRestApi(
            self, 'Gateway',
            description="Endpoint for a simple Lambda-powered web service",
            handler=alias
        )

        failure_alarm = cloudwatch.Alarm(
            self, 'FailureAlarm',
            metric=cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions={
                    'ApiName': 'Gateway',
                },
                statistic='Sum',
                period=core.Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1)

        codedeploy.LambdaDeploymentGroup(
            self,
            'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES,
            alarms=[failure_alarm],
        )

        self.url_output = core.CfnOutput(self, 'Url', value=gw.url)
