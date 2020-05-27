import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

CIRCLE_BUILD_NUM = os.environ["CIRCLE_BUILD_NUM"]
CIRCLE_SHA1 = os.environ["CIRCLE_SHA1"]
CIRCLE_PROJECT_REPONAME = os.environ["CIRCLE_PROJECT_REPONAME"]
CIRCLE_PROJECT_USERNAME = os.environ["CIRCLE_PROJECT_USERNAME"]
CIRCLE_PROJECT_ID = os.environ["CIRCLE_PROJECT_ID"]

CIRCLE_ROOT = "https://{CIRCLE_BUILD_NUM}-{CIRCLE_PROJECT_ID}-gh.circle-artifacts.com/0".format(
    CIRCLE_BUILD_NUM=CIRCLE_BUILD_NUM,
    CIRCLE_PROJECT_ID=CIRCLE_PROJECT_ID)


def create_deployment(env_name, description, env_url):
    url = "https://api.github.com/repos/{CIRCLE_PROJECT_USERNAME}/{CIRCLE_PROJECT_REPONAME}/deployments".format(
        CIRCLE_PROJECT_USERNAME=CIRCLE_PROJECT_USERNAME,
        CIRCLE_PROJECT_REPONAME=CIRCLE_PROJECT_REPONAME
    )
    data = {"ref": CIRCLE_SHA1,
            "environment": env_name,
            "description": description,
            "transient_environment": True,
            "auto_merge": False,
            "required_contexts": []}
    req = requests.post(url, json=data, headers={
        "Authorization": "bearer {}".format(GITHUB_TOKEN)
    })
    req.raise_for_status()
    deployment = req.json()

    url = "https://api.github.com/repos/{CIRCLE_PROJECT_USERNAME}/{CIRCLE_PROJECT_REPONAME}/deployments/{deployment_id}/statuses".format(
        CIRCLE_PROJECT_USERNAME=CIRCLE_PROJECT_USERNAME,
        CIRCLE_PROJECT_REPONAME=CIRCLE_PROJECT_REPONAME,
        deployment_id=deployment["id"]
    )
    data = {"state": "success",
            "environment": env_name,
            "environment_url": env_url,
            "log_url": "https://circleci.com/gh/dashbase/dashbase/{}".format(CIRCLE_BUILD_NUM),
            }
    req = requests.post(url, json=data, headers={
        "Authorization": "bearer {}".format(GITHUB_TOKEN)
    })
    req.raise_for_status()


create_deployment("ci-home", "auto create static home", "{}/home/index.html".format(CIRCLE_ROOT))
