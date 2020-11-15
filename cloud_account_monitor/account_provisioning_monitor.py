from aws_cdk import core
from .acct_factory_monitor import AccountFactoryMonitor


class AccountProvisioningMonitor(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_creator_monitor = AccountFactoryMonitor( self, "Account-Creation-Monitor")
       