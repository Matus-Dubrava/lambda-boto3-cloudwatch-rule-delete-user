# this function is used together with cloudwatch event rule that passes
# CreateUser event to it
# this function automatically deletes such user

import boto3

iam_client = boto3.client('iam')


def lambda_handler(event, context):
    try:
        user_name = event['detail']['responseElements']['user']['userName']

        # try to delete login profile if exists
        try:
            response = iam_client.delete_login_profile(
                UserName=user_name
            )
            print(response)
        except Exception as err:
            print(err)

        # try to delete access keys if exist
        try:
            access_key_ids = iam_client.list_access_keys(
                UserName=user_name
            )['AccessKeyMetadata']

            for key_metadata in access_key_ids:
                response = iam_client.delete_access_key(
                    UserName=user_name,
                    AccessKeyId=key_metadata['AccessKeyId']
                )

            print(response)
        except Exception as err:
            print(err)

        response = iam_client.delete_user(
            UserName=user_name
        )
        print(response)
        print("User {} has been DELETED".format(user_name))

        return None
    except Exception as err:
        print(err)
        return None
