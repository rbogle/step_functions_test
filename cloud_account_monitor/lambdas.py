from aws_cdk import core
from aws_cdk import aws_lambda


class AccountFactoryLambda(core.Construct):
    def __init__(self, scope: core.Construct, id: str, *, runtime: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_7, timeout: int=30, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.runtime = runtime
        self.timeout = timeout
        self.function = aws_lambda.Function(
            self, 
            id,
            runtime=self.runtime,
            handler="lambda.factory_handler",
            code=aws_lambda.Code.from_asset("lambdas"),
            timeout=core.Duration.seconds(self.timeout)
        )

class StateHandlerLambda(core.Construct):
    def __init__(self, scope: core.Construct, id: str, *, runtime: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_7, timeout: int=30, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.runtime = runtime
        self.timeout = timeout
        self.function = aws_lambda.Function(
            self, 
            id,
            runtime=self.runtime,
            handler="lambda.state_handler",
            code=aws_lambda.Code.from_asset("lambdas"),
            timeout=core.Duration.seconds(self.timeout)
        )