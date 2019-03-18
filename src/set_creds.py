import argparse
import json
import os
import shlex
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

GIT_TOKEN = os.getenv("GIT_TOKEN")
DESTINATION_CREDS_FILE = os.getenv("DESTINATION_CREDS_FILE")


def get_profile_input_from_user():
    """Parses user CLI input from the user

    Returns:
        dict: AWS profile with MFA token
    """
    parser = argparse.ArgumentParser(description="Parse MFA token")
    parser.add_argument("profile")
    parser.add_argument("token")
    args = parser.parse_args()
    profile = get_aws_profile_info(args.profile)
    print(f"Proceeding with profile {args.profile} and mfa_token {args.token}")
    profile['mfa_token'] = args.token
    return profile


def get_aws_profile_info(profile):
    """Creates a profile dict, pulling in info from .env

    Args:
        profile (str): profile name provided by user as cli arg

    Returns:
        dict: profile specific info
    """
    profile_list = os.getenv("PROFILE_LIST")
    if profile.upper() not in profile_list:
        print(f'Profile {profile} is not configured, please set it up or try again')
        sys.exit()
    aws_iam_account_number = os.getenv(f"{profile.upper()}_AWS_IAM_ACCOUNT_NUMBER")
    aws_user = os.getenv(f"{profile.upper()}_AWS_USER")
    aws_default_region = os.getenv(f"{profile.upper()}_AWS_DEFAULT_REGION")
    return {
        'aws_iam_account_number': aws_iam_account_number,
        'aws_user': aws_user,
        'aws_default_region': aws_default_region
    }


def get_creds(profile):
    """Requests session token via AWS CLI

    Args:
        profile (dict): profile specific info

    Returns:
        tuple: AWS creds provided by AWS CLI request
    """
    aws_iam_account_number = profile.get('aws_iam_account_number', None)
    aws_user = profile.get('aws_user', None)
    mfa_token = profile.get('mfa_token', None)
    aws_default_region = profile.get('aws_default_region', None)

    print("Requesting creds...")
    aws_str = f"aws sts get-session-token --serial-number arn:aws:iam::{aws_iam_account_number}:mfa/{aws_user} --token-code {mfa_token} --duration-seconds 129600"  # noqa
    aws_cmd = shlex.split(aws_str)
    aws_cli_response = subprocess.run(aws_cmd, stdout=subprocess.PIPE)
    if aws_cli_response.returncode == 255:
        print("Incorrect profile or MFA?")
        sys.exit()

    json_creds = json.loads(aws_cli_response.stdout).get('Credentials', None)
    if json_creds is not None:
        secret_access_key = json_creds.get('SecretAccessKey')
        session_token = json_creds.get('SessionToken')
        access_key_id = json_creds.get('AccessKeyId')
        print("Creds received and parsed...")
        return secret_access_key, session_token, access_key_id, aws_default_region
    else:
        print("Oh dear, AWS CLI response did not include credentials.")
        sys.exit()


def write_creds_to_file(creds):
    """Takes AWS CLI response and writes to the destination creds file

    Args:
        creds (tuple): the AWS creds to be written to the creds file
    """
    with open(DESTINATION_CREDS_FILE, "w") as text_file:
        print(f"export AWS_SECRET_ACCESS_KEY={creds[0]}", file=text_file)
        print(f"export AWS_SESSION_TOKEN={creds[1]}", file=text_file)
        print(f"export AWS_ACCESS_KEY_ID={creds[2]}", file=text_file)
        print(f"export GIT_TOKEN={GIT_TOKEN}", file=text_file)
        print(
            f"export AWS_DEFAULT_REGION={creds[3]}", file=text_file)
    print("Adding creds to file...")
    print("Creds added to file.")
    print("Credentials set.")


def main():
    profile = get_profile_input_from_user()
    creds = get_creds(profile)
    print(creds)
    write_creds_to_file(creds)


if __name__ == '__main__':
    main()
