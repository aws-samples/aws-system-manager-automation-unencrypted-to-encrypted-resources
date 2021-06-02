Automatically remediate unencrypted RDS Instances and Clusters using the specific Customer master keys

This sample describes how to automatically remediate unencrypted RDS Instances and Clusters. Amazon RDS encrypted DB instances provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon RDS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

Deployment Options

The sample solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using Systems Manger Automation Document (SSM) that will unencrypted RDS instances and clusters by using the specific Customer master keys (CMK) if not initially encrypted when created.

Option # 1: Deploy the CloudFormation which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

Option # 2: Deploy the AWS Cloud Development Kit (AWS CDK) which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

You can enable encryption for an Amazon RDS DB instance when you create it, but not after it's created. However, you can add encryption to an unencrypted DB instance by creating a snapshot of your DB instance, and then creating an encrypted copy of that snapshot. You can then restore a DB instance from the encrypted snapshot to get an encrypted copy of your original DB instance.

This sample automatically remediate unencrypted RDS Instances and Clusters using the AWS Config rule and specific Customer master keys. AWS Config allows you to remediate noncompliant resources that are evaluated by AWS Config Rules. AWS Config applies remediation using AWS System Manger Automation documents. These documents define the actions to be performed on noncompliant AWS resources evaluated by AWS Config Rules.

The target outcome is to remediate unencrypted RDS Instances and Clusters using your Customer master (CMK) key and then enforce service control policies (SCPs) to deny DB instances and cluster creation in future without encryption enabled.
Deployment Options

The solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using Systems Manger Automation Document (SSM) that will unencrypted RDS instances and clusters by using the specific Customer master keys (CMK) if not initially encrypted when created.

Option # 1: Deploy the CloudFormation which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

Option # 2: Deploy the AWS Cloud Development Kit (AWS CDK) which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

Enforce Service Control Policies (SCPs)

Once the resources are remediate, enforce Service control policies(rds_encrypted.json) to deny DB instances and cluster creation in future without encryption.  

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

