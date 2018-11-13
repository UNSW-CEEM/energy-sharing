There is a bug in current versions of pipenv, that the default pip is an in-development version, with a bug. 
See here for a workaround:https://github.com/pypa/pipenv/issues/2871
In short:

pip install pipenv
pipenv run pip install pip==18.0
pipenv install

