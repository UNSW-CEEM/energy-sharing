There is a bug in current versions of pipenv, that the default pip is an in-development version, with a bug. 
See here for a workaround:https://github.com/pypa/pipenv/issues/2871
In short:

pip install pipenv
pipenv run pip install pip==18.0
pipenv install



# Questions

1. line 152 of parameters.py in create_mike_objects() - whats create_csvs() doing? doesnt look like this function does much. 

