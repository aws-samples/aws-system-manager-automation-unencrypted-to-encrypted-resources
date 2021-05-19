#!/usr/bin/env python3

from aws_cdk import core

from unencrypted_to_encrypted_rds.unencrypted_to_encrypted_rds_stack import UnencryptedToEncryptedRdsStack
from unencrypted_to_encrypted_rds.test_rds_stack import RDSStack

app = core.App()
description="This sample, non-production-ready template create a config remediation rule to create encrypted RDS instances and clusters using the specific CMK."
UnencryptedToEncryptedRdsStack(app, "unencrypted-to-encrypted-rds", description=description)
RDSStack(app,"test-rds-stack", description="This sample, non-production-ready template creating a test RDS instance and cluster in order to test remediation.")

app.synth()
