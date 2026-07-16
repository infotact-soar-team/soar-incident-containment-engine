"""
AWS Security Group Isolation — SIMULATED ONLY via moto.
No real AWS account or credentials are used; moto mocks the AWS API in-memory.
"""
import boto3
from moto import mock_aws

_MOCK_REGION = "us-east-1"


@mock_aws
def isolate_via_security_group(ip: str) -> dict:
    """
    Simulates isolating a malicious IP by creating/updating a
    'quarantine' Security Group that blocks all traffic to/from it.
    Fully mocked — safe to run with zero real AWS cost or risk.
    """
    ec2 = boto3.client("ec2", region_name=_MOCK_REGION)

    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    sg = ec2.create_security_group(
        GroupName="soar-quarantine-sg",
        Description="Auto-created by SOAR playbook to isolate malicious IP",
        VpcId=vpc_id,
    )
    sg_id = sg["GroupId"]

    ec2.revoke_security_group_egress(
        GroupId=sg_id,
        IpPermissions=ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]["IpPermissionsEgress"],
    ) if ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]["IpPermissionsEgress"] else None

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            "IpProtocol": "-1",
            "IpRanges": [{"CidrIp": f"{ip}/32", "Description": "Blocked by SOAR"}],
        }],
    )

    return {
        "action": "AWS_SG_ISOLATE",
        "ip": ip,
        "security_group_id": sg_id,
        "status": "isolated",
        "success": True,
    }
