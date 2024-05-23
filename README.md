# Github repository request challange

This repository contains the `pr_requests.py` **python** script, which utilizes the GitHub API to retrieve summaries of opened, closed, and in-progress pull requests in the last week for a specified repository and generates an email summary report.

By default, the script is configured with the following repository owner and name:

`REPO_OWNER = octocat`
 ` REPO_NAME = Hello-World`
 
However you can configure it by setting environment variables for both values. Depending on your operating system:

For Windows:

    set REPO_OWNER="some-user"
    set REPO_NAME="some-repo-name"

For Linux:

    export REPO_OWNER="some-user"
    export REPO_NAME="some-repo-name"

------------

You will need the requests library in order to use this script. If you haven't installed it, you can do so using pip:

`$ python -m pip install requests`

The script can be run with the python command: `python pr_requests.py`
