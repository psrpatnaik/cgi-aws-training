#https://docs.aws.amazon.com/code-samples/latest/catalog/python-ec2-ec2_basics-ec2_setup.py.html
import sys
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

# instantiation of the ec2 client
ec2 = boto3.resource('ec2')

def create_instance(
        image_id, instance_type, key_name, security_group_names=None):
    """
    Creates a new Amazon EC2 instance. The instance automatically starts immediately after
    it is created.

    The instance is created in the default VPC of the current account.

    :param image_id: The Amazon Machine Image (AMI) that defines the kind of
                     instance to create. The AMI defines things like the kind of
                     operating system, such as Amazon Linux, and how the instance is
                     stored, such as Elastic Block Storage (EBS).
    :param instance_type: The type of instance to create, such as 't2.micro'.
                          The instance type defines things like the number of CPUs and
                          the amount of memory.
    :param key_name: The name of the key pair that is used to secure connections to
                     the instance.
    :param security_group_names: A list of security groups that are used to grant
                                 access to the instance. When no security groups are
                                 specified, the default security group of the VPC
                                 is used.
    :return: The newly created instance.
    """
    try:
        instance_params = {
            'ImageId': image_id, 'InstanceType': instance_type, 'KeyName': key_name
        }
        if security_group_names is not None:
            instance_params['SecurityGroups'] = security_group_names
        instance = ec2.create_instances(**instance_params, MinCount=1, MaxCount=1)[0]
        logger.info("Created instance %s.", instance.id)
    except ClientError:
        logging.exception(
            "Couldn't create instance with image %s, instance type %s, and key %s.",
            image_id, instance_type, key_name)
        raise
    else:
        return instance
# Make sure the values you are entering are present if not create them.
create_instance('ami-09e67e426f25ce0d7','t2.micro','sample-instance',['Sample instance'])
	
print("OK")