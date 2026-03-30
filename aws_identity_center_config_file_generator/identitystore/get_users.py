import os

import boto3

from utils.flatten import flatten

def get_users(session: boto3.Session) -> list[str]:
    identity_store_id = os.environ["IDENTITY_STORE_ID"]
    identity_store_client = session.client("identitystore")

    list_users_paginator = identity_store_client.get_paginator("list_users")

    return flatten(
        [
            page["Users"]
            for page in list_users_paginator.paginate(
                IdentityStoreId=identity_store_id
            )
        ]
    )
