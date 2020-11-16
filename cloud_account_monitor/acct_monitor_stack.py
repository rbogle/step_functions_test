from aws_cdk import core
from .acct_factory_monitor import AccountFactoryMonitor
from .acct_config_monitor import AccountConfigMonitor
from .acct_prov_monitor import AccountProvMonitor


class AccountMonitorStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_creator_monitor = AccountFactoryMonitor( self, "Account-Creation-Monitor")
        account_config_monitor = AccountConfigMonitor(self, "Account-Config-Monitor")
        account_prov_monitor = AccountProvMonitor(self, "Account-Prov-Monitor", account_creator_monitor, account_config_monitor)