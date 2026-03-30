from typing import NamedTuple

import boto3

from utils.flatten import flatten

UserAccount = NamedTuple("UserAccount", [("account_id", str), ("account_name", str), ("role_name", str)])

def get_accounts_for_user(session: boto3.Session, instance_arn: str, user_id: str) -> list[UserAccount]:
    client = session.client("sso-admin")

    paginator = client.get_paginator("list_account_assignments_for_principal")

    response = flatten(
        [
            page["AccountAssignments"]
            for page in paginator.paginate(
                InstanceArn=instance_arn,
                PrincipalId=user_id,
                PrincipalType="USER"
            )
        ]
    )

    results = []

    for account_assignment in response:
        account_id = account_assignment["AccountId"]

        permission_set_name = client.describe_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=account_assignment["PermissionSetArn"]
        )["PermissionSet"]["Name"]

        account_client = session.client("organizations")
        account_name = account_client.describe_account(AccountId=account_id)["Account"]["Name"]

        results.append(UserAccount(
            account_id=account_id,
            account_name=account_name,
            role_name=permission_set_name
        ))

    return results
