#!/bin/bash

"""
Bash Shell Script that will be used for Packer build process as a Custom Bitbucket Pipe.
Reference:: https://community.atlassian.com/t5/Bitbucket-questions/Custom-pipe-pointing-to-bitbucket-repository/qaq-p/1402376
https://support.atlassian.com/bitbucket-cloud/docs/write-a-pipe-for-bitbucket-pipelines/
"""
ROLE_ARN=""
SESSION_NAME=""
PACKER_FILE=""
ENVIRONMENT=""
VPC=""
SOURCE=""
SUBNET=""
SECURITYGROUP=""
PARAMETERSTORE=""

while [ "$1" != "" ]; do
    case $1 in
        --role-arn )         shift
                             ROLE_ARN=$1
                             ;;
        --role-session-name ) shift
                             SESSION_NAME=$1
                             ;;
        --packer-file )       shift
                             PACKER_FILE=$1
                             ;;
        --environment )       shift
                             ENVIRONMENT=$1
                             ;;
        --vpc-id )            shift
                             VPC=$1
                             ;;
        --source-name )       shift
                             SOURCE=$1
                             ;;
        --subnet-id )         shift
                             SUBNET=$1
                             ;;
        --security-group-id ) shift
                             SECURITYGROUP=$1
                             ;;
        --parameter-store )   shift
                             PARAMETERSTORE=$1
                             ;;
        * )                   echo "Invalid argument: $1"
                             exit 1
                             ;;
    esac
    shift
done
if [ -z "$ROLE_ARN" ] || [ -z "$SESSION_NAME" ] || [ -z "$PACKER_FILE" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Error: --role-arn, --role-session-name, --packer-file, and --environment are required."
    exit 1
fi
CREDS=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "$SESSION_NAME" --output json)
AWS_ACCESS_KEY_ID=$(echo "$CREDS" | jq -r '.Credentials.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | jq -r '.Credentials.SecretAccessKey')
AWS_SESSION_TOKEN=$(echo "$CREDS" | jq -r '.Credentials.SessionToken')
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN

#Run the Packer Build Process
packer init "$PACKER_FILE"
packer build \
    -var "environment=$ENVIRONMENT" \
    -var "vpcid=$VPC" \
    -var "source_name=$SOURCE" \
    -var "subnetid=$SUBNET" \
    -var "securitygroupid=$SECURITYGROUP" \
    -var "parameterstore=$PARAMETERSTORE" \
    "$PACKER_FILE"
