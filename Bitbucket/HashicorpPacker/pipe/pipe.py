#Source Code From Bitbucket Pipe Hashicorp Vault 
import os
import subprocess
import sys 
import boto3
import yaml
from enum import Enum, auto

from bitbucket_pipes_toolkit import Pipe, get_logger

logger = get_logger()

# Define the schema for the pipe
schema = {
    'AWS_DEFAULT_REGION': {'type': 'string', 'required': True},
    'AWS_ROLE_ARN': {'type': 'string', 'required': True},
    'AWS_ROLE_SESSION_NAME': {'type': 'string', 'required': True},
    'AWS_ENVIRONMENT': {'type': 'string', 'required': True},
    'AWS_VPC_ID': {'type': 'string', 'required': True},
    'AWS_SUBNET_ID': {'type': 'string', 'required': True},
    'AWS_SECURITY_GROUP_ID': {'type': 'string', 'required': True},
    'AWS_PARAMETER_STORE_NAME': {'type': 'string', 'required': True},
    'PACKER_SOURCE_NAME': {'type': 'string', 'required': True},
}


class PackerBuild(Pipe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load AWS and Packer environment variables
        self.aws_default_region = os.getenv('AWS_DEFAULT_REGION')
        self.aws_oidc_role = os.getenv('AWS_ROLE_ARN')
        self.aws_oidc_role_name = os.getenv('AWS_ROLE_SESSION_NAME')
        self.aws_environment = os.getenv('AWS_ENVIRONMENT')
        self.aws_vpc_id = os.getenv('AWS_VPC_ID')
        self.aws_security_group_id = os.getenv('AWS_SECURITY_GROUP_ID')
        self.aws_subnet_id = os.getenv('AWS_SUBNET_ID')
        self.aws_parameter_store_name = os.getenv('AWS_PARAMETER_STORE_NAME')
        self.packer_source_name = os.getenv('PACKER_SOURCE_NAME')
        self.config = self.get_variable('CONFIG')

    def setup_aws_env_credentials(self):
        """Set up AWS environment credentials by assuming the provided role using OIDC."""
        self.log_info("Assuming provided AWS OIDC role with the web-identity")
        # Fetch the Web Identity Token from environment variables
        web_identity_token = os.getenv('BITBUCKET_STEP_OIDC_TOKEN')
        if not web_identity_token:
            self.log_error('Web identity token not found in environment variables.')
            raise ValueError('Web identity token is required for OIDC authentication.')

        # Create an STS client and assume the role using web identity
        client = boto3.client('sts')
        response = client.assume_role_with_web_identity(
            RoleArn=self.aws_oidc_role,
            RoleSessionName=self.aws_oidc_role_name,
            WebIdentityToken=web_identity_token #Getting the Bitbucket Step OIDC Token
        )

        # Set the assumed role credentials into the environment
        os.environ['AWS_ACCESS_KEY_ID'] = response['Credentials']['AccessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = response['Credentials']['SecretAccessKey']
        os.environ['AWS_SESSION_TOKEN'] = response['Credentials']['SessionToken']
        self.log_info("Set up temporary AWS credentials in the environment")

        #Log Credentials to the console for Testing
        self.log_info(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
        self.log_info(f"AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY')}")


    def run_packer_build(self):
        """Run the Packer build process."""
        self.log_info(f"Running Packer build with source name: {self.packer_source_name}")

        # Run packer init .
        self.log_info("Running packer init command")
        init_command = ["packer", "init", "amazon-ecs.pkr.hcl"] #Testing packer version command
        print(init_command)
        try:
            init_result = subprocess.run(init_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.log_info(f"Packer init output: {init_result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            self.log_error(f"Packer init failed: {e.stderr.decode('utf-8')}")
            raise

        # TO-DO - Run packer build with the provided source name
        self.log_info("Running packer build command")
        build_command = [
            "packer", "build",
            "-var", f"env={self.aws_environment}",
            "-var", f"vpcid={self.aws_vpc_id}",
            "-var", f"source_name={self.packer_source_name}",
            "-var", f"subnetid={self.aws_subnet_id}",
            "-var", f"securitygroupid={self.aws_security_group_id}",
            "-var", f"parameterstore={ self.aws_parameter_store_name}",
            "amazon-ecs.pkr.hcl"
        ]
        try:
            build_result = subprocess.run(build_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, capture_output=True, text=True)
            self.log_info(f"Packer build output: {build_result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            self.log_error(f"Packer build failed: {e.stderr.decode('utf-8')}")
            raise

    def run(self):
        """Run the Packer build pipeline."""
        # Set up AWS credentials
        self.setup_aws_env_credentials()
        # Execute the Packer build
        self.run_packer_build()
        result = subprocess.run(stdout=sys.stdout, stderr=sys.stderr)
        logger.info(f"Result: {result}")
        
if __name__ == '__main__':
    with open('/pipe.yml', 'r') as metadata_file:
        metadata = yaml.safe_load(metadata_file.read())
        pipe = PackerBuild(schema=schema, pipe_metadata=metadata, check_for_newer_version=True)
        pipe.run()
