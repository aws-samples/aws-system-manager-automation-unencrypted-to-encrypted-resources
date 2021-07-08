#!/bin/bash
set -Eeuox pipefail

aws ec2 enable-ebs-encryption-by-default

aws ec2 get-ebs-default-kms-key-id

EBS_CMK_ARN=$(aws kms describe-key --key-id 'alias/EC2EncryptionAtRestCMKAlias' |jq --raw-output '.KeyMetadata.Arn')

aws ec2 modify-ebs-default-kms-key-id --kms-key-id "$EBS_CMK_ARN"

aws ec2 get-ebs-default-kms-key-id
