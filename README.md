# inventory_management_service

## Developer's Guidelines
### Run locally
Prerequisite: python3-venv and mysql is installed.

1. Install virtual environment in the project folder, i.e., folder that contains 'app'
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install python packages:
    ```shell
    pip3 install -r app/requirements/local.txt
    ```
3. Run the project with command:
    ```shell
    export FLASK_ENV=local
    python3 app/main.py --settings=settings.local,settings.base
    ```

```shell
pre-commit install #To install the pre-commit hook
pre-commit install --hook-type commit-msg #To install the commit message hook
pre-commit run --all-files
```


To run the formatter,linter and all the test altogether navigate to inventory_management_service folder:

```shell
python3 scripts/cross_os.py
```

Testing
navigate to the root folder
To run all the tests:
```shell
python3 -m pytest tests
```

To check the code coverage of the tests:
```shell
python3 -m pytest --cov-report term-missing --cov=app
```
Git commit message format: git commit -m "feat: :gitemoji: title" -m "message"
for git emoji, please refer: https://gitmoji.dev/
