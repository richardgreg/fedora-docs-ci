from fedora_messaging import api, config
from build import post_comment


null = "null"
false = False
true = True

# A sample PR message object for testing the build script.
topic = "io.pagure.prod.pagure.pull-request.new"
body = {
    "agent": "richardgreg",
    "pullrequest": {
        "assignee": null,
        "branch": "master",
        "branch_from": "typo_fix",
        "cached_merge_status": "unknown",
        "closed_at": null,
        "closed_by": null,
        "comments": [],
        "commit_start": "2be761e03c828fc2ab8709255d4f2946bb7e0e30",
        "commit_stop": "2be761e03c828fc2ab8709255d4f2946bb7e0e30",
        "date_created": "1614356479",
        "full_url": "https://pagure.io/fedora-docs/quick-docs/pull-request/347",
        "id": 348,
        "initial_comment": "Ignore this PR. It's for testing purposes.",
        "last_updated": "1614356479",
        "project": {
            "access_groups": {
                "admin": [
                    "fedora-docs"
                ],
                "collaborator": [],
                "commit": [
                    "quick-docs-committers"
                ],
                "ticket": []
            },
            "access_users": {
                "admin": [
                    "jflory7",
                    "mattdm"
                ],
                "collaborator": [],
                "commit": [],
                "owner": [
                    "pbokoc"
                ],
                "ticket": []
            },
            "close_status": [
                "complete",
                "duplicate",
                "insufficient data",
                "moved",
                "not possible",
                "out of scope",
                "stale"
            ],
            "custom_keys": [],
            "date_created": "1508967894",
            "date_modified": "1590058045",
            "description": "How-tos and other short-form documentation",
            "full_url": "https://pagure.io/fedora-docs/quick-docs",
            "fullname": "fedora-docs/quick-docs",
            "id": 3273,
            "milestones": {},
            "name": "quick-docs",
            "namespace": "fedora-docs",
            "parent": null,
            "priorities": {
                "": "",
                "10": "needs review",
                "20": "next meeting",
                "30": "waiting on assignee",
                "40": "waiting on external",
                "50": "awaiting triage"
            },
            "tags": [
                "docs",
                "documentation"
            ],
            "url_path": "fedora-docs/quick-docs",
            "user": {
                "full_url": "https://pagure.io/user/pbokoc",
                "fullname": "Petr Bokoc",
                "name": "pbokoc",
                "url_path": "user/pbokoc"
            }
        },
        "remote_git": null,
        "repo_from": {
            "access_groups": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "ticket": []
            },
            "access_users": {
                "admin": [],
                "collaborator": [],
                "commit": [],
                "owner": [
                    "richardgreg"
                ],
                "ticket": []
            },
            "close_status": [],
            "custom_keys": [],
            "date_created": "1602135866",
            "date_modified": "1602135866",
            "description": "How-tos and other short-form documentation",
            "full_url": "https://pagure.io/fork/richardgreg/fedora-docs/quick-docs",
            "fullname": "forks/richardgreg/fedora-docs/quick-docs",
            "id": 8768,
            "milestones": {},
            "name": "quick-docs",
            "namespace": "fedora-docs",
            "parent": {
                "access_groups": {
                    "admin": [
                        "fedora-docs"
                    ],
                    "collaborator": [],
                    "commit": [
                        "quick-docs-committers"
                    ],
                    "ticket": []
                },
                "access_users": {
                    "admin": [
                        "jflory7",
                        "mattdm"
                    ],
                    "collaborator": [],
                    "commit": [],
                    "owner": [
                        "pbokoc"
                    ],
                    "ticket": []
                },
                "close_status": [
                    "complete",
                    "duplicate",
                    "insufficient data",
                    "moved",
                    "not possible",
                    "out of scope",
                    "stale"
                ],
                "custom_keys": [],
                "date_created": "1508967894",
                "date_modified": "1590058045",
                "description": "How-tos and other short-form documentation",
                "full_url": "https://pagure.io/fedora-docs/quick-docs",
                "fullname": "fedora-docs/quick-docs",
                "id": 3273,
                "milestones": {},
                "name": "quick-docs",
                "namespace": "fedora-docs",
                "parent": null,
                "priorities": {
                    "": "",
                    "10": "needs review",
                    "20": "next meeting",
                    "30": "waiting on assignee",
                    "40": "waiting on external",
                    "50": "awaiting triage"
                },
                "tags": [
                    "docs",
                    "documentation"
                ],
                "url_path": "fedora-docs/quick-docs",
                "user": {
                    "full_url": "https://pagure.io/user/pbokoc",
                    "fullname": "Petr Bokoc",
                    "name": "pbokoc",
                    "url_path": "user/pbokoc"
                }
            },
            "priorities": {},
            "tags": [],
            "url_path": "fork/richardgreg/fedora-docs/quick-docs",
            "user": {
                "full_url": "https://pagure.io/user/richardgreg",
                "fullname": "Richard Gregory",
                "name": "richardgreg",
                "url_path": "user/richardgreg"
            }
        },
        "status": "Open",
        "tags": [],
        "threshold_reached": null,
        "title": "Update index page.",
        "uid": "defe5b8c5b9e44b398f84f7a2f4f77b4",
        "updated_on": "1614356479",
        "user": {
            "full_url": "https://pagure.io/user/richardgreg",
            "fullname": "Richard Gregory",
            "name": "richardgreg",
            "url_path": "user/richardgreg"
        }
    }
}


config.conf.setup_logging()
api.publish(api.Message(topic="hello", body={"pullrequest": body}))
