# CONTRIBUTING
Contributing to the official buyTogether application
Welcome! We're so excited that you're considering contributing to the official GitHub page for buyTogether.
---
## Prerequisites
Stage 1:
- Install vagrant & Oracle VirtualBox
* [Vagrant](https://www.vagrantup.com/)
* [Oracle VirtualBox](https://www.virtualbox.org/)

Stage 2:
- Fork the repo to make your changes without affecting the original project until you're ready to
propose your code changes.
- Create a working branch.
- Set up a development environment to begin working on the project, all you need to do is 'vagrant up'.
- Start with your changes!
---
## Commiting
Please use the guide below in order to follow our commit message convention:
* [commit convention](https://cbea.ms/git-commit/#seven-rules)
---
## Pull Request
- When you're finished with the changes, create a pull request, also known as a PR.
- If your PR depends on the merging of other PRs, indicate this on the commit message ('depends on #<PR number>').
Specifically, if it contains unmerged commits of any other PRs,
indicate to the reviewers which commits are expected to be reviewed as part of your PR.
- Keep your PRs as small as possible.
Ideally, a single PR should include a single commit.
- The reviewer resolves the conversation to indicate that they are ok with the updated content.
- Be aware that reviewers won't address a PR with any merging issues (Conflict or CI) until those issues have been resolved.
- Changes made as part of the review process (i.e. fixes to the content of the original commit),
should be added to the original commit (e.g. using `commit --amend`), rather than creating a new commit. 
- Please keep in mind that at least two team members of the group should provide a constructive feedback,
and approve the pull request before asking the maintainers to review and merge it.
- Each PR should include tests for the features it presents (Code testing section below),
PR without tests won't be reviewed.
---
## Code Testing
This project uses Pytest as its test framework.

* [Pytest - Quick guide](https://docs.pytest.org/en/7.2.x/getting-started.html)
- Please note that Pytest is already installed in this project's virtual environment.

---
## Review Requirements
- When reviewing, confirm that the code accomplishes the requirements and the acceptance criteria by using one or both ways:
A GitHub issue: the code fixes the problem.
Adding a feature: elaborate in the commit the purpose of the code.
Both cases should have accompanying unit tests that cover all the relevant edge cases.
---
## Your PR is merged!
Congratulations.
Once your PR is merged, your contributions will be publicly visible on GitHub.
---
## Issues:
- If you spot a problem, search if an issue already exists.
If a related issue doesn't exist, you can open a new issue using a relevant issue form.
- Make sure your description is clear.
Screenshots are very helpful in diagnosing issues; please include them whenever possible.
---
## Coding Conventions
Before adding code to our project please note that we use PEP8 standards & Flake8 test checking.
You can read about it in the reference below.
* [PEP8](https://peps.python.org/pep-0008/)
* [Flake8](https://flake8.pycqa.org/en/latest/)
---