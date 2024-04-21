## Create Virtual Environment
```bash
pip install virtualenv
virtualenv -p python3 blog
source blog/bin/activate # py -m venv blog blog\Scripts\activate
deactivate
```
```bash
# https://docs.anaconda.com/free/anaconda/install/windows/
# Anaconda Prompt
conda env list
conda create -n blog python # conda create -n blog python=3.8 --no-default-packages --no-deps
conda activate blog
conda deactivate
```

## List Packages
```bash
pip freeze
```

## Create requirements.txt
```bash
pip freeze > requirements.txt
```

## Installing Packages
```bash
pip install -r requirements.txt
```

## HTTP Requests
- GET: to fetch data from a resource
- POST: to create a new resource
- PUT/PATCH: to update a resource
- DELETE: to delete a resource

## Command Prompt
```bash
dir # - to list the current directory
mkdir NEW_DIRECTORY_NAME # - to make a new directory
cd DIRECTORY_NAME # - to change the current working directory to DIRECTORY_NAME
```

## HTTP Response Codes
- 200: Success
- 500: Internal Server Error
- 404: Not Found
- 401: Unauthorized
- 403: Forbidden
- 201: Created Successfully
- 504: Gateway Timeout
- 422: Unprocessable Entity

## Branching Scheme
```bash
git branch testing
git branch staging
git branch production

git switch testing
git push -u origin testing
git switch staging
git push -u origin staging
git switch production
git push -u origin production

git switch production
git branch feature/NAME_OF_THE_FEATURE
git branch fix/NAME_OF_THE_FIX
git branch hotfix/NAME_OF_THE_HOTFIX
git switch THE_NEWLY_CREATED_BRANCH
git add .
git commit -m "MESSAGE"
git push -u origin THE_NEWLY_CREATED_BRANCH
```