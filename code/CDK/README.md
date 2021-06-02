Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install the tool locally
```
pip3 install  -r requirements.txt
```

Bootstrap the environment for CDK
```
cdk bootstrap
```

Deploy the automation stack
```
cdk deploy unencrypted-to-encrypted-rds
```

For testing, deploy the test stack, test, and then destroy
1. Deploy the test resources ```cdk deploy test-rds-stack```
2. Test by going to config and clicking remediate on the test resource.
3. Destroy the test resources ```cdk destroy```
