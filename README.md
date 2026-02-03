# Automatically remediate unencrypted resources

These samples describe how to automatically remediate unencrypted resources such as Amazon Elastic Block Store (Amazon EBS) and Amazon Relational Database Service (Amazon RDS).

## Automatically remediate unencrypted EBS Volumes using customer KMS keys

This [sample](ebs) describes how to automatically remediate unencrypted EBS Volumes. Amazon EBS encrypted volumes provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon EBS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

![EBS architecture diagram](ebs-architecture.png)

The sample solution can be deployed using the AWS CloudFormation template, which creates a Config remediation using an AWS Systems Manager (SSM) Automation Document that will encrypt EBS Volumes using a specific customer-managed AWS Key Management Service (AWS KMS) key if not initially encrypted when created.

Once the resources are remediated, ensure preventive enforcement via Service Control Policies to deny EC2 instance and volume creation in the future without encryption.

## Automatically remediate unencrypted RDS Instances and Clusters using customer KMS keys

This [sample](rds) describes how to automatically remediate unencrypted Amazon RDS Instances and Clusters. Amazon RDS encrypted DB instances provide an additional layer of data protection by securing your data from unauthorized access to the underlying storage. You can use Amazon RDS encryption to increase data protection of your applications deployed in the cloud, and to fulfill compliance requirements for encryption at rest.

![RDS architecture diagram](rds-architecture.png)

The sample solution can be deployed using the AWS CloudFormation stack or AWS Cloud Development Kit (AWS CDK), which create remediation using AWS Systems Manager Automation Document (SSM) that will encrypt unencrypted Amazon RDS instances and clusters by using the specific Customer KMS key if not initially encrypted when created.

Once the resources are remediated, ensure preventive enforcement via Service Control Policies to deny DB instances and cluster creation in future without encryption.  

## Secret Management

This repository follows AWS security best practices for managing secrets and sensitive data. **Never commit secrets, credentials, or sensitive information to version control.**

### Using AWS Secrets Manager and Parameter Store

For production deployments, store sensitive configuration using AWS managed services:

- **AWS Secrets Manager**: Use for database credentials, API keys, and other secrets that require automatic rotation
  ```bash
  # Store a secret
  aws secretsmanager create-secret --name MyDatabasePassword --secret-string "MySecretValue"
  
  # Retrieve a secret in your application
  aws secretsmanager get-secret-value --secret-id MyDatabasePassword
  ```

- **AWS Systems Manager Parameter Store**: Use for configuration values and non-rotating secrets
  ```bash
  # Store a parameter
  aws ssm put-parameter --name /myapp/config/kms-key-id --value "arn:aws:kms:..." --type SecureString
  
  # Retrieve a parameter
  aws ssm get-parameter --name /myapp/config/kms-key-id --with-decryption
  ```

### Protected File Patterns

The repository's `.gitignore` file is configured to prevent accidental commits of sensitive files:

- **Private keys**: `*.pem`, `*.key`, `*.p12`, `*.pfx`, SSH keys
- **Environment files**: `.env`, `.env.local`, `.env.*.local`
- **AWS credentials**: `.aws/credentials`, `aws-credentials.json`
- **CDK context**: `cdk.context.json` (may contain account IDs)
- **Certificate files**: `*.crt`, `*.cer`, `*.der`
- **Secret configuration**: `secrets.yml`, `secrets.json`, `.secrets`

### Secret Scanning

This repository includes a secret scanner to detect accidentally committed secrets:

```bash
# Scan the entire repository
python3 scripts/scan-secrets.py

# Scan with verbose output
python3 scripts/scan-secrets.py --verbose

# Scan a specific directory
python3 scripts/scan-secrets.py --path ./my-directory
```

The scanner detects:
- AWS access keys (AKIA*, ASIA*)
- AWS secret access keys
- Private key headers
- API keys and tokens
- Hardcoded passwords in configuration files

**Best Practice**: Run the secret scanner before committing code and as part of your CI/CD pipeline.

### What to Do If You Commit a Secret

If you accidentally commit a secret to version control:

1. **Immediately rotate the secret** - Assume it is compromised
2. **Remove it from git history** - Use tools like `git filter-branch` or `BFG Repo-Cleaner`
3. **Update AWS credentials** - Deactivate and delete the exposed credentials
4. **Review access logs** - Check CloudTrail for any unauthorized usage
5. **Update your .gitignore** - Ensure the file type is excluded

For more information, see [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

