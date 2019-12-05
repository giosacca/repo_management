# repo_management

Manage you repositories.

## Creating a new repository with repo_initialiser

The repo_initialiser module can be used to create a repo with the following strucuture.

```bash
/repo
│───docs
│───package
│   │───__init__.py
│   └───module.py
│───tests
│   └───context.py
│───.gitignore
│───LICENSE.md
│───README.md 
│───requirements.txt
└───setup.py
```

- Change in `repo_management/config.ini` the path to your repos.

```
[paths]
repos = path/to/repos
```

- Run `jupyter lab` or `jupyter notebook` in the root folder of this repo.

- Open the notebook in `notebooks/repo_initialiser.ipynb` and execute it changing values where required.

**Attetion!**: this will not add a README to your new repo.