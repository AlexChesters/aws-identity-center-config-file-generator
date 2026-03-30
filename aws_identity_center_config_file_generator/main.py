import os
from pathlib import Path

from dotenv import load_dotenv
import boto3
import inquirer
from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils.validate_environment import validate_environment
from identitystore.get_users import get_users
from identitystore.get_accounts_for_user import get_accounts_for_user

load_dotenv()
validate_environment()

jinja_env = Environment(
    loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"),
    autoescape=select_autoescape()
)

def main() -> None:
    profile_name = os.environ["AWS_PROFILE"]
    region_name = os.environ["AWS_REGION"]

    session = boto3.Session(profile_name=profile_name, region_name=region_name)

    questions = [
        inquirer.List(
            "user",
            message="Select a user to generate the config file for",
            choices=[(user["UserName"], user["UserId"]) for user in get_users(session)],
        )
    ]
    answers = inquirer.prompt(questions)

    sso_instance = session.client("sso-admin").list_instances()["Instances"][0]
    instance_id = sso_instance["InstanceArn"].split("/")[-1]

    accounts = get_accounts_for_user(session, sso_instance["InstanceArn"], answers["user"])

    template = jinja_env.get_template("config.jinja")
    rendered_template = template.render(
        region_name=region_name,
        sso_start_url=f"https://{instance_id}.portal.{region_name}.app.aws",
        accounts=accounts
    )

    with open("config", "w") as f:
        f.write(rendered_template)


if __name__ == "__main__":
    main()
