from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core,
)


class RDSStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.Vpc(self, "VPC", max_azs=99)

        rds.DatabaseInstance(
            self,
            "RDS-instance",
            database_name="dbinstance1",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_16
            ),
            vpc=vpc,
            port=3306,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            publicly_accessible=False,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            allocated_storage=10,
        ),

        rds.DatabaseCluster(
            self,
            "RDS-cluster",
            cluster_identifier="dbcluster1",
            engine=rds.DatabaseClusterEngine.aurora_mysql(
                version=rds.AuroraMysqlEngineVersion.VER_2_08_1
            ),
            port=3306,
            instance_props=rds.InstanceProps(
                vpc=vpc,
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.MEMORY4,
                    ec2.InstanceSize.LARGE,
                ),
                publicly_accessible=False,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
        )
