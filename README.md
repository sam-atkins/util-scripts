# Utility Scripts

A collection of scripts to automate repeated and mundane tasks. Some of these could be set-up as aliases but this keeps everything organised in one repo.

## Table of Contents

- [Utility Scripts](#utility-scripts)
  - [Table of Contents](#table-of-contents)
  - [Script Usage](#script-usage)
  - [Git Hooks](#git-hooks)
  - [Links to other scripts](#links-to-other-scripts)

## Script Usage

Check each script's documentation for usage instructions.

## Git Hooks

To use at a global level run this command:

```bash
git config --global core.hooksPath /path/to/git_hooks
```

This results in `~/.gitconfig` being updated like this

```
[core]
  hooksPath = /path/to/git_hooks
```

Ensure the git hook is executable e.g.

```bash
chmod +x /path/to/git_hooks/prepare-commit-msg
```


## Links to other scripts

Other util scripts, usually written in Python, have their own repo. Links below:

- [CookieCutter: Python CLI app](https://github.com/sam-atkins/cookiecutter-python-cli)
- [Currency converter](https://github.com/sam-atkins/fx)
- [Get AWS MFA Creds](https://github.com/sam-atkins/awscrd-cli)
- [Add boilerplate repo config](https://github.com/sam-atkins/repoconf)
- [Todoist API wrapper](https://github.com/sam-atkins/todo-cli)
