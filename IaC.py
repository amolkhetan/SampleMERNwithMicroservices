import boto3

ec2 = boto3.client('ec2')

# Create VPC
print("Creating VPC...")
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']
print(f"✅ VPC created with ID: {vpc_id}")

# Tag VPC
print("Tagging VPC...")
ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'MERN-VPC'}])
print("✅ VPC tagged as 'MERN-VPC'")

# Create Subnet
print("Creating Subnet...")
subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24')
subnet_id = subnet['Subnet']['SubnetId']
print(f"✅ Subnet created with ID: {subnet_id}")

# Create Security Group
print("Creating Security Group...")
sg = ec2.create_security_group(
    GroupName='MERN-SG',
    Description='Allow HTTP and SSH',
    VpcId=vpc_id
)
sg_id = sg['GroupId']
print(f"✅ Security Group created with ID: {sg_id}")

# Add Ingress Rules
print("Adding Ingress Rules to Security Group...")
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
    ]
)
print("✅ Ingress rules added: SSH (22) and HTTP (80) open to all")

print("\n🎉 AWS networking setup complete.")
