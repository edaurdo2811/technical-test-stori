from aws_cdk import (
    Stack,
    aws_lambda as lb,
    aws_apigateway as apg,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy, CfnOutput
)
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, 'bucket-stori', bucket_name="stori-technical-test", removal_policy=RemovalPolicy.DESTROY,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        s3deploy.BucketDeployment(self, "DeployImages",
                                  sources=[s3deploy.Source.asset("cdk/resources/dependencias")],
                                  destination_bucket=bucket
                                  )

        role = iam.Role(
            self,
            "Lambda_to_S3",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            description='My CDK Role',
            role_name='LambdaS3'
        )

        arn_s3 = bucket.bucket_arn
        CfnOutput(self, 'bucker-arn', value=arn_s3)
        policy_statement = iam.PolicyStatement(
            actions=["s3:*"],
            resources=[f"{arn_s3}/*"]
        )

        role.add_to_policy(policy_statement)

        lambda_function = lb.Function(
            self,
            'lambda_events',
            runtime=lb.Runtime.PYTHON_3_11,
            handler='events_info.lambda_handler',
            code=lb.Code.from_asset('cdk/resources/events'),
            role=role
        )

        apig_function = apg.LambdaRestApi(
            self,
            "ApiGwEndpoint",
            handler=lambda_function,
            rest_api_name="cdk_api"
        )

        lambda_function.add_layers(lb.LayerVersion.from_layer_version_arn(self,'numpy_layer','arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-numpy:11'))
        lambda_function.add_layers(lb.LayerVersion.from_layer_version_arn(self,'pillow_layer',
                                                                          'arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-Pillow:6'))

