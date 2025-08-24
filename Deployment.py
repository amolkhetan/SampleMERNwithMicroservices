import boto3
import base64

# Read and encode user-data script
with open('userdata.sh', 'rb') as f:
    user_data_encoded = base64.b64encode(f.read()).decode('utf-8')

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')

# Create Launch Template
print("Creating Launch Template 'MERN-Backend-AMK' without EC2 key pair...")
lt = ec2.create_launch_template(
    LaunchTemplateName='MERN-Backend-AMK',
    LaunchTemplateData={
        'ImageId': 'ami-03aa99ddf5498ceb9',
        'InstanceType': 't2.micro',
        'NetworkInterfaces': [
            {
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'SubnetId': 'subnet-0fee8b5ba154ae3c6',
                'Groups': ['sg-0cf0786e1b21fe65c']
            }
        ],
        'UserData': user_data_encoded
    }
)
lt_id = lt['LaunchTemplate']['LaunchTemplateId']
print(f"✅ Launch Template created with ID: {lt_id}")

# Create Auto Scaling Group
print("Creating Auto Scaling Group 'MERN-Backend-AMK-ASG'...")
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='MERN-Backend-AMK-ASG',
    LaunchTemplate={'LaunchTemplateName': 'MERN-Backend-AMK'},
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=2,
    VPCZoneIdentifier='subnet-0fee8b5ba154ae3c6,subnet-055831d956cc96074'
)
print("✅ Auto Scaling Group created with public IP and EC2 Connect enabled")

print("\n🚀 Backend infrastructure setup complete. You can now connect via EC2 Instance Connect.")
