#!/usr/bin/env python3

from aws_cdk import core

from cloud_account_monitor.acct_monitor_stack import AccountMonitorStack

app = core.App()
AccountMonitorStack(app, "fcc-acct-prov-monitor")
app.synth()
