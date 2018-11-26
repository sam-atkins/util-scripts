import argparse
import json
import os
import shlex
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

AWS_USER = os.getenv("AWS_USER")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_IAM_ACCOUNT_NUMBER = os.getenv("AWS_IAM_ACCOUNT_NUMBER")
GIT_TOKEN = os.getenv("GIT_TOKEN")
FILE = os.getenv("SOURCE_FILE")


def get_mfa_token():
    parser = argparse.ArgumentParser(description="Parse MFA token")
    parser.add_argument("token")
    args = parser.parse_args()
    print(f"Proceeding with mfa_token: {args.token}")
    return args.token


def get_creds(mfa_token):
    aws_str = f"aws sts get-session-token --serial-number arn:aws:iam::{AWS_IAM_ACCOUNT_NUMBER}:mfa/{AWS_USER} --token-code {mfa_token} --duration-seconds 129600"  # noqa
    aws_cmd = shlex.split(aws_str)
    print("Requesting creds...")
    aws_cli_response = subprocess.run(aws_cmd, stdout=subprocess.PIPE)
    if aws_cli_response.stdout is not None:
        return aws_cli_response.stdout
    else:
        print("Oh dear, AWS CLI response did not include credentials.")
        sys.exit()


def parse_creds_response(creds_response):
    json_creds = json.loads(creds_response).get('Credentials')
    if json_creds is not None:
        secret_access_key = json_creds.get('SecretAccessKey')
        session_token = json_creds.get('SessionToken')
        access_key_id = json_creds.get('AccessKeyId')
        print("Creds received and parsed...")
        return secret_access_key, session_token, access_key_id
    else:
        print("Oh dear, AWS CLI response did not include credentials.")
        sys.exit()


def write_creds_to_file(creds):
    with open(FILE, "w") as text_file:
        print(f"export AWS_SECRET_ACCESS_KEY={creds[0]}", file=text_file)
        print(f"export AWS_SESSION_TOKEN={creds[1]}", file=text_file)
        print(f"export AWS_ACCESS_KEY_ID={creds[2]}", file=text_file)
    print("Adding creds to file...")
    print("Creds added to file.")


def control():
    mfa_token = get_mfa_token()
    creds = get_creds(mfa_token)
    print(creds)
    parsed_creds = parse_creds_response(creds)
    write_creds_to_file(parsed_creds)


if __name__ == '__main__':
    control()
