from github import Github
import datetime
import os

template = os.environ["TEMPLATE"]
GITHUB_ID = os.environ["GITHUB_ID"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


CIRCLE_BUILD_NUM = os.environ["CIRCLE_BUILD_NUM"]
CIRCLE_SHA1 = os.environ["CIRCLE_SHA1"]
CIRCLE_PROJECT_REPONAME = os.environ["CIRCLE_PROJECT_REPONAME"]
CIRCLE_PROJECT_USERNAME = os.environ["CIRCLE_PROJECT_USERNAME"]
CIRCLE_PULL_REQUESTS = os.environ["CIRCLE_PULL_REQUESTS"]
PR_ID = CIRCLE_PULL_REQUESTS.split("/")[-1]

body = template.format(CIRCLE_BUILD_NUM=CIRCLE_BUILD_NUM,
                       TIME=datetime.datetime.now().isoformat(),
                       COMMIT=CIRCLE_SHA1,
                       GITHUB_ID=GITHUB_ID,
                       CIRCLE_PROJECT_USERNAME=CIRCLE_PROJECT_USERNAME,
                       CIRCLE_PROJECT_REPONAME=CIRCLE_PROJECT_REPONAME,
                       )

g = Github(GITHUB_TOKEN)
repo = g.get_repo("{user}/{repo}".format(user=CIRCLE_PROJECT_USERNAME, repo=CIRCLE_PROJECT_REPONAME))
pr = repo.get_pull(PR_ID)
comments = pr.get_issue_comments()
comment = None
for c in comments:
    if "Create by Comment Bot" in c.body:
        comment = c
        break

if comment is not None:
    comment.edit(body)
    print("Edit Comment Successful")
else:
    pr.create_issue_comment(body)
    print("Create Comment Successful")

# pr.create_issue_comment(
#     "Hello Just a Test :)"
# )
