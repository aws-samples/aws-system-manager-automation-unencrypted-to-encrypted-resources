# Automatically remediate unencrypted RDS Instances and Clusters using customer KMS keys

This sample describes how to automatically remediate unencrypted Amazon Relational Database Service (Amazon RDS) Instances and Clusters. Amazon RDS encrypted DB instances provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon RDS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

![RDS architecture diagram](../rds-architecture.png)

## Deployment Options

The sample solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using AWS Systems Manager Automation Document (SSM) that will encrypt unencrypted Amazon RDS instances and clusters by using the specific Customer AWS Key Management Service (AWS KMS) keys if not initially encrypted when created.
 
* Option # 1: Deploy the [CloudFormation](CloudFormation) which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your KMS key.

* Option # 2: Deploy the [AWS Cloud Development Kit AWS CDK](CDK) which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your KMS key. The CDK option also allows you to deploy a test stack, if you desire to evaluate running the remediation on an example RDS scenario.

## Enforce Service Control Policies

Once the resources are remediated, enforce Service Control Policies (rds_encrypted.json) to deny DB instances and cluster creation in future without encryption.  

[SCPs](SCP)



## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.


