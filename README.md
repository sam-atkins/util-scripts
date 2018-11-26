# Utility Scripts

A collection of scripts to automate repeated and mundane tasks. Some of these could be set-up as aliases but this keeps everything organised in one repo.

## Table of Contents

- [Script Usage](#script-usage)
- [Installation](#installation)
- [Tests](#tests)

## Script Usage

### Set AWS Creds

```bash
# run from dir where AWS creds are required
creds <mfa-token>
```

### Foreign Currency Exchange

```bash
fx
# and follow the prompts. Script is fairly basic at the moment so make sure to
# type currency abbreviations correctly
```

### Git Fetch and Pull from Remote Current Branch

```bash
gfb
```

### Git Fetch and Pull from Remote Master

```bash
# note, this switches branch to master
gfm
```

### Git Log Graph Pretty

```bash
glogg
```

### Git Prune Branches

```bash
# run from dir where you want to prune branches
prune [-d|-D]
```

### Movie

```bash
movie <film title>

# example, single word film title
movie jaws

# example, multi-word film title
movie 'star wars'
```

### Pyclean

```bash
# run from dir where you want to clean .pyo .pyc __pycache__
pyclean
```

### Trash

```bash
# empties the Trash on MacOS
trash
```

### Weather

```bash
# Usage: `weather CITYNAME` or just `weather` to use IP location.
weather <city>
```

## Installation

### Pre-requisites

* Python 3
* Poetry

(And for the AWS credentials script)

* AWS CLI
* AWS credentials file per [this](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/)

### Git clone and add to $PATH

* Git clone the repo to a local directory.
* Add the directory to path so all scripts can be called from any location.
  * in `~/.bashrc` for the bash shell
  * in `~/.zshrc` for the zsh shell

```bash
export PATH=$PATH:~/{code-directory}/util-scripts
```

* Make the scripts executable

```bash
chmod u+x ./{script_name}
```

### Python set-up

Create a virtualenv

```bash
virtualenv -p python3 env
```

Install Python dependencies using [Poetry](https://poetry.eustace.io/docs/cli/):

```bash
poetry install
```

### AWS creds set-up

Set-up `~/.aws/credentials` file and add the id and key e.g.

```txt
[default]
aws_access_key_id = someId
aws_secret_access_key = someSecret
```

### Add an `.env` file
Convert the `.env.template` to an `.env` file and populate the details with AWS credentials.


## Tests

To run tests:

```bash
# activate virtual env
source env/bin/activate

# run tests
pytest

# run tests with verbosity
pytest -vv

# run tests with code coverage
pytest --cov
```
