**Automatically remediate unencrypted RDS Instances and Clusters using the specific Customer master keys**

This sample describes how to automatically remediate unencrypted RDS Instances and Clusters. Amazon RDS encrypted DB instances provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon RDS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

**Deployment Options**

The sample solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using Systems Manger Automation Document (SSM) that will unencrypted RDS instances and clusters by using the specific Customer master keys (CMK) if not initially encrypted when created.

Option # 1: Deploy the CloudFormation which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

Option # 2: Deploy the AWS Cloud Development Kit (AWS CDK) which will create the Remediation Rule that will encrypt the unencrypted RDS Instances and Clusters using your CMK key.

**Enforce Service Control Policies (SCPs)**

Once the resources are remediate, enforce Service control policies(rds_encrypted.json) to deny DB instances and cluster creation in future without encryption.  

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

