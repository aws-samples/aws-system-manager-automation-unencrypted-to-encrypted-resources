# © 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

# This is sample, non-production-ready template create a config remediation rule to create encrypted RDS instances and clusters using the specific CMK.

# Prerequisites
# An active AWS account
# The CMK key should already exist to encrypt RDS Instances and Clusters
# Plesae ensure you have access to update KMS CMK Resource policy
# An unencrypted Amazon RDS DB instance or Clusters
# Access to AWS services, including:
#     AWS Config
#     AWS RDS
#     AWS System Manager Automation Document
#     AWS CloudFormation (Option #1)
#     AWS CDK (Option #2)
#     AWS Key Management Service (KMS)
#     AWS Identity and Access Management (IAM)
#     You must have AWS Config enabled in your AWS account. For more information, see Getting Started with AWS Config.

# You can enable encryption for an Amazon RDS DB instance only when you create it, not after the DB instance is created.
# You can't have an encrypted read replica of an unencrypted DB instance or an unencrypted read replica of an encrypted DB instance.
# You can't restore an unencrypted backup or snapshot to an encrypted DB instance.
# Amazon RDS encryption is available for most DB instance classes. The following table lists DB instance classes that do not support Amazon RDS encryption: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html
# To copy an encrypted snapshot from one AWS Region to another, you must specify the CMK in the destination AWS Region. This is because CMKs are specific to the AWS Region that they are created in.
# The source snapshot remains encrypted throughout the copy process. Amazon RDS uses envelope encryption to protect data during the copy process. For more information about envelope encryption, see Envelope encryption in the AWS Key Management Service Developer Guide.
# You can't unencrypt an encrypted DB instance. However, you can export data from an encrypted DB instance and import the data into an unencrypted DB instance.
# You should delete a CMK only when you are sure that you don't need to use it anymore. If you are not sure, consider disabling the CMK instead of deleting it. You can reenable a disabled CMK if you need to use it again later, but you cannot recover a deleted CMK.
# If you don't choose to retain automated backups, your automated backups in the same AWS Region as the DB instance are deleted. They can't be recovered after you delete the DB instance.
# Your automated backups are retained for the retention period that is set on the DB instance at the time when you delete it. This set retention period occurs whether or not you choose to create a final DB snapshot.

import json

from aws_cdk import core, aws_iam as iam, aws_ssm, aws_config, aws_kms


class UnencryptedToEncryptedRdsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        """
        kms_key_id_param = core.CfnParameter(
            self,
            "kmskeyid",
            type="String",
            description="The KMS key id used to encrypt",
        )

        kms_key_id_value = kms_key_id_param.value_as_string
        """

        # user guide example with assumerolepolicydocument
        # https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-cf.html
        # cloudformation example https://docs.aws.amazon.com/systems-manager/latest/userguide/samples/AWS-SystemsManager-AutomationServiceRole.zip
        automation_role = iam.Role(
            self,
            "EncryptRDSAutomationRole",
            # role_name="EncryptRDSAutomationRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ssm.amazonaws.com"),
                iam.ServicePrincipal("rds.amazonaws.com"),
            ),
        )

        automation_role.grant_pass_role(automation_role)

        rds_key = aws_kms.Key(
            self,
            "rds-encryption-key",
            alias="alias/RDSEncryptionAtRestCMKAlias",
            enable_key_rotation=True,
        )

        # Setup Role Permissions
        automation_role_policy = iam.ManagedPolicy(
            self,
            f"EncryptRDSAutomationRole-policy",
            description="Permissions for the RDS encrypt unencrypted",
            path="/",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ec2:DescribeAvailabilityZones",
                        "ec2:DescribeInternetGateways",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DescribeSubnets",
                        "ec2:DescribeVpcAttribute",
                        "ec2:DescribeVpcs",
                        "rds:AddTagsToResource",
                        "ssm:GetAutomationExecution",
                    ],
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["kms:CreateGrant", "kms:DescribeKey"],
                    resources=[
                        f"arn:aws:kms:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:key/{rds_key.key_id}"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CreateDBClusterSnapshot",
                        "rds:DeleteDBClusterSnapshot",
                        "rds:DescribeDBClusterSnapshots",
                        "rds:RestoreDBClusterFromSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:cluster-snapshot:*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CreateDBClusterSnapshot",
                        "rds:DescribeDBClusters",
                        "rds:RestoreDBClusterFromSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:cluster:*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CreateDBInstance",
                        "rds:CreateDBSnapshot",
                        "rds:DescribeDBInstances",
                        "rds:RestoreDBInstanceFromDBSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:db:*",
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:cluster:*",
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CreateDBInstance",
                        "rds:RestoreDBClusterFromSnapshot",
                        "rds:RestoreDBInstanceFromDBSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:og:*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["rds:CreateDBInstance"],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:secgrp:*",
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:pg:*",
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CopyDBSnapshot",
                        "rds:CreateDBSnapshot",
                        "rds:DeleteDBSnapshot",
                        "rds:DescribeDBSnapshots",
                        "rds:RestoreDBInstanceFromDBSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:snapshot:*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "rds:CreateDBInstance",
                        "rds:RestoreDBInstanceFromDBSnapshot",
                    ],
                    resources=[
                        f"arn:aws:rds:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:subgrp:*"
                    ],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["ssm:StartAutomationExecution"],
                    resources=[
                        # f"arn:aws:ssm:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:automation-definition/*:*",
                        "*",
                    ],
                ),
            ],
        )

        automation_role.add_managed_policy(automation_role_policy)

        encrypt_rds_json = "aws-encrypt-rds.json"
        encrypt_rds_cluster_json = "aws-encrypt-rds-cluster.json"
        encrypt_rds_instance_json = "aws-encrypt-rds-instance.json"
        with open(encrypt_rds_json, "r") as file_encrypt_rds_json, open(
            encrypt_rds_instance_json, "r"
        ) as file_encrypt_rds_instance_json, open(
            encrypt_rds_cluster_json, "r"
        ) as file_encrypt_rds_cluster_json:

            encrypt_rds_content = json.load(file_encrypt_rds_json)
            encrypt_rds_instance_content = json.load(file_encrypt_rds_instance_json)
            encrypt_rds_cluster_content = json.load(file_encrypt_rds_cluster_json)

            encrypt_rds_cluster_ssmdoc = aws_ssm.CfnDocument(
                self,
                "ENCRYPT-unencryptedrdscluster",
                content=encrypt_rds_cluster_content,
                document_type="Automation",
            )

            encrypt_rds_instance_ssmdoc = aws_ssm.CfnDocument(
                self,
                "ENCRYPT-unencryptedrdsinstance",
                content=encrypt_rds_instance_content,
                document_type="Automation",
            )

            encrypt_rds_ssmdoc = aws_ssm.CfnDocument(
                self,
                "ENCRYPT-unencryptedrds",
                content=encrypt_rds_content,
                document_type="Automation",
            )

            rds_storage_encrypted_config_rule_name = (
                "rds-storage-encrypted-with-remediation"
            )

            aws_config.ManagedRule(
                self,
                rds_storage_encrypted_config_rule_name,
                config_rule_name=rds_storage_encrypted_config_rule_name,
                identifier="RDS_STORAGE_ENCRYPTED",
                description="Checks whether storage encryption is enabled for your RDS DB instances.",
            )
            configremediation = aws_config.CfnRemediationConfiguration(
                self,
                "EncryptRDSConfigRemediation",
                config_rule_name=rds_storage_encrypted_config_rule_name,
                target_id=encrypt_rds_ssmdoc.ref,
                target_type="SSM_DOCUMENT",
                automatic=False,
                parameters={
                    "instanceAutomationDocument": {
                        "StaticValue": {"Values": [encrypt_rds_instance_ssmdoc.ref]},
                    },
                    "clusterAutomationDocument": {
                        "StaticValue": {"Values": [encrypt_rds_cluster_ssmdoc.ref]},
                    },
                    "automationAssumeRole": {
                        "StaticValue": {"Values": [automation_role.role_arn]}
                    },
                    "kmsKeyId": {"StaticValue": {"Values": [rds_key.key_id]}},
                    "resourceId": {"ResourceValue": {"Value": "RESOURCE_ID"}},
                },
                resource_type="AWS::RDS::DBInstance",
                target_version="1",
            )
