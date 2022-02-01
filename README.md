# Automatically remediate unencrypted resources

These samples describe how to automatically remediate uenencrypted resources such as EBS and RDS.

## Automatically remediate unencrypted EBS Volumes using customer KMS keys

This [sample](ebs) describes how to automatically remediate unencrypted EBS Volumes. Amazon EBS encrypted volumes provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon EBS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

![EBS architecture diagram](ebs-architecture.png)

The sample solution can be deployed using the AWS CloudFormation template, which creates a Config remediation using a Systems Manger (SSM) Automation Document that will encrypt EBS Volumes using a specific customer-managed KMS key if not initially encrypted when created.

Once the resources are remediated, ensure preventive enforcement via Service Control Policies to deny EC2 instance and volume creation in the future without encryption.

## Automatically remediate unencrypted RDS Instances and Clusters using customer KMS keys

This [sample](rds) describes how to automatically remediate unencrypted RDS Instances and Clusters. Amazon RDS encrypted DB instances provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon RDS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

![RDS architecture diagram](rds-architecture.png)

The sample solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using Systems Manger Automation Document (SSM) that will unencrypted RDS instances and clusters by using the specific Customer KMS key if not initially encrypted when created.

Once the resources are remediated, ensure preventive enforcement via Service control policies to deny DB instances and cluster creation in future without encryption.  

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

