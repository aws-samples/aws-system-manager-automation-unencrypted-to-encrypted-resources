# Security

## Reporting a Vulnerability

If you discover a potential security issue in this project, we ask that you notify AWS Security via our [vulnerability reporting page](https://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

For more information, see the [AWS Vulnerability Reporting Guide](https://aws.amazon.com/security/vulnerability-reporting/).

## Supported Versions

This project follows the AWS Systems Manager automation lifecycle. We recommend using the latest version of the automation documents and CloudFormation/CDK templates to ensure you have the most recent security updates and improvements.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Security Best Practices

### Encryption at Rest

**Customer-Managed KMS Keys**: This solution uses AWS Key Management Service (AWS KMS) to encrypt Amazon Elastic Block Store (Amazon EBS) volumes and Amazon Relational Database Service (Amazon RDS) instances and clusters. We recommend using customer-managed KMS keys for the following benefits:

- Full control over key policies and access permissions
- Ability to enable automatic key rotation
- Detailed audit trail through AWS CloudTrail
- Granular access control through IAM policies

**Key Rotation**: Enable automatic key rotation for your customer-managed KMS keys to enhance security:

```bash
aws kms enable-key-rotation --key-id <your-key-id>
```

**Key Policy Best Practices**:
- Scope KMS key permissions to specific IAM principals
- Use condition keys to restrict key usage to specific services
- Regularly review and audit key policies
- Enable CloudTrail logging for all KMS API calls

### Encryption in Transit

**RDS SSL/TLS Configuration**: When connecting to encrypted RDS instances, always use SSL/TLS to protect data in transit:

- Enable the `rds.force_ssl` parameter for RDS instances
- Use SSL/TLS certificates provided by Amazon RDS
- Configure your database clients to require SSL/TLS connections
- Regularly update SSL/TLS certificates before expiration

**VPC Endpoints**: Use VPC endpoints for AWS service communication to keep traffic within the AWS network:

- Create VPC endpoints for AWS Systems Manager, Amazon EC2, and Amazon RDS
- Configure security groups to restrict access to VPC endpoints
- Use VPC endpoint policies to control access to AWS services

### IAM Least Privilege

This solution implements IAM least privilege by scoping permissions to specific resource ARNs:

**Resource Scoping**: All IAM policies use specific resource ARNs instead of wildcards (`*`):

```yaml
# Good: Scoped to specific resource types
Resource:
  - !Sub 'arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:instance/*'
  - !Sub 'arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:volume/*'

# Avoid: Wildcard permissions
Resource: '*'
```

**Separation of Read and Write Operations**: Read-only operations (e.g., `Describe*`) are separated from write operations to minimize the blast radius of potential security incidents.

**Permission Review Practices**:
- Regularly review IAM policies using AWS IAM Access Analyzer
- Remove unused permissions and roles
- Use IAM policy conditions to further restrict access
- Monitor IAM activity through CloudTrail logs

### Logging and Monitoring

**CloudTrail Integration**: Enable AWS CloudTrail to log all API calls made by the automation:

```bash
aws cloudtrail create-trail \
  --name security-automation-trail \
  --s3-bucket-name <your-cloudtrail-bucket>

aws cloudtrail start-logging --name security-automation-trail
```

**CloudWatch Alarms**: Configure CloudWatch alarms to monitor security events:

- Failed automation executions
- Unauthorized API calls
- KMS key usage anomalies
- IAM policy changes

**Example CloudWatch Alarm**:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name automation-failures \
  --alarm-description "Alert on automation failures" \
  --metric-name ExecutionsFailed \
  --namespace AWS/SSM \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold
```

**AWS Config Compliance**: Use AWS Config rules to continuously monitor compliance:

- `encrypted-volumes` - Ensures EBS volumes are encrypted
- `rds-storage-encrypted` - Ensures RDS instances are encrypted
- `cloudtrail-enabled` - Ensures CloudTrail is enabled

### Data Classification

> **Note**: Data classification through tagging is an optional but recommended practice for production environments. It enables you to apply appropriate security controls based on data sensitivity.

**Tagging Strategies**: Use resource tags to classify data and apply appropriate security controls:

| Classification | Tag Key | Tag Value | Encryption Requirement |
|---------------|---------|-----------|------------------------|
| Public | DataClassification | Public | Optional |
| Internal | DataClassification | Internal | Recommended |
| Confidential | DataClassification | Confidential | Required |
| Restricted | DataClassification | Restricted | Required with customer-managed KMS |

**Applying Tags**:

```bash
# Tag an EBS volume
aws ec2 create-tags \
  --resources vol-1234567890abcdef0 \
  --tags Key=DataClassification,Value=Confidential

# Tag an RDS instance
aws rds add-tags-to-resource \
  --resource-name arn:aws:rds:us-east-1:123456789012:db:mydb \
  --tags Key=DataClassification,Value=Restricted
```

**Encryption Based on Classification**:
- **Public**: No encryption required, but recommended
- **Internal**: Use AWS-managed keys or customer-managed keys
- **Confidential**: Use customer-managed KMS keys with key rotation enabled
- **Restricted**: Use customer-managed KMS keys with strict key policies and access controls

## Optional Security Enhancements

The following security enhancements are optional but recommended for production environments:

### Enhanced Monitoring

Configure enhanced monitoring for RDS instances to collect detailed metrics:

```bash
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --monitoring-interval 60 \
  --monitoring-role-arn arn:aws:iam::123456789012:role/rds-monitoring-role
```

### Advanced CloudTrail Configuration

Enable CloudTrail Insights to detect unusual API activity:

```bash
aws cloudtrail put-insight-selectors \
  --trail-name security-automation-trail \
  --insight-selectors '[{"InsightType": "ApiCallRateInsight"}]'
```

### VPC Flow Logs

Enable VPC Flow Logs to monitor network traffic:

```bash
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-12345678 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs
```

### AWS Security Hub Integration

Enable AWS Security Hub for centralized security findings:

```bash
aws securityhub enable-security-hub
aws securityhub batch-enable-standards \
  --standards-subscription-requests StandardsArn=arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0
```

## Additional Resources

- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Systems Manager Security](https://docs.aws.amazon.com/systems-manager/latest/userguide/security.html)
