""" repo_initialiser module

This module is to initialise a repo.
"""

import git
import pathlib as pl
import datetime as dt
import subprocess as sp
import time

import pexpect.popen_spawn as pops

import repo_management as rm

class RepoInitialiser(object):
	"""
	A class used to initialise a repo.

	Attributes
	----------
	name : string
		The name of the repo.
	link : string
		The https link to the repo.
	"""

	config = rm.Configuration()
	logger = rm.RepoLogger()

	def __init__(self, name, link, owner):

		self.name = name
		self.link = link
		self.owner = owner
		self.modules = []

		self.add_path()

	def add_path(self):
		"""
		Adds the path to the object.
		"""

		self.path = (
			pl.Path(self.config.parser['paths'].get('repos'))
			/ self.name
			)
		
		self.logger.logger.info(f'The path of the repo is {self.path}')

	def clone_from_bitbucket(self):
		"""
		Clones the repo from Bitbucket.
		"""

		self.repo = git.Repo.clone_from(self.link, self.path)
		
		self.logger.logger.info(
			f'The repos has been cloned from Bitbucket'
			)


	def add_gitignore(self):
		"""
		Adds a standard .gitignore file to the repo.
		"""

		template = self.config.parser['templates'].get('gitignore')

		with open(template, 'r') as f:
			ignore = f.read()

		self.gitignore = self.path / '.gitignore'

		with open(self.gitignore, 'w') as f:
			f.write(ignore)
		
		self.logger.logger.info(
			f'The .gitignore file has been added to the repo'
			)

	def add_license(self, license):
		"""
		Adds a license to repo.

		license : string
			The type of license you want to use (MIT or GNU).
		"""

		self.license = license
		template = self.config.parser['licenses'].get(license)

		with open(template, 'r') as f:
			text = f.read()

		year = dt.date.today().year
		text = text.format(year = year, fullname = self.owner)
		license_file = self.path / 'LICENSE.md'

		with open(license_file, 'w') as f:
			f.write(text)
		
		self.logger.logger.info(
			f'The {self.license} license has been added to the repo'
			)

	def add_package_folder(self):
		"""
		Adds the folder for the main package.
		"""

		self.packege_path = self.path / self.name
		self.packege_path.mkdir()
		
		self.logger.logger.info(
			f'The {self.name} folder has been added to the repo'
			)

	def add_package_init(self):
		"""
		Adds the __init__.py file for the main package.
		"""

		init = self.packege_path / '__init__.py'
		open(init, 'a').close()
		
		self.logger.logger.info(
			f'The __init__.py file has been added to the repo'
			)

	def add_package(self):
		"""
		Creates an empty package with an empty __init__.py file.
		"""

		self.add_package_folder()
		self.add_package_init()
		
		self.logger.logger.info(
			f'The {self.name} package has been added to the repo'
			)

	def add_module(self, name):
		"""
		Adds a module to the main package.

		Parameters
		----------
		name : string
			The name of the module.
		"""

		self.modules.append(name)

		template = self.config.parser['templates'].get('module')

		with open(template, 'r') as f:
			head = f.read()

		module = self.packege_path / '{}.py'.format(name)

		with open(module, 'w') as f:
			f.write(head)
		
		self.logger.logger.info(
			f'The {name} module has been added to the repo'
			)

	def add_requirements(self):
		"""
		Adds a requirements.txt file.
		"""

		requirements = self.path / 'requirements.txt'
		open(requirements, 'a').close()
		
		self.logger.logger.info(
			f'The requirements.txt file has been added to the repo'
			)

	def add_setup(self):
		"""
		Adds a setup.py file.
		"""
		
		template = self.config.parser['templates'].get('setup')

		with open(template, 'r') as f:
			text = f.read()

		text = text.format(
			package = self.name,
			modules = self.modules,
			license = self.license,
			)
		setup = self.path / 'setup.py'

		with open(setup, 'w') as f:
			f.write(text)
		
		self.logger.logger.info(
			f'The setup.py file has been added to the repo'
			)

	def add_tests_folder(self):
		"""
		Adds the folder for the tests.
		"""

		self.tests_path = self.path / 'tests'
		self.tests_path.mkdir()
		
		self.logger.logger.info(
			f'The test folder has been added to the repo'
			)

	def add_tests_context(self):
		"""
		Adds the context.py file to the tests.
		"""

		template = self.config.parser['templates'].get('context')

		with open(template, 'r') as f:
			text = f.read()

		text = text.format(package = self.name)
		context = self.tests_path / 'context.py'

		with open(context, 'w') as f:
			f.write(text)
		
		self.logger.logger.info(
			f'The context.py has been added to the repo'
			)

	def add_tests(self):
		"""
		Adds the tests to the repo.
		"""

		self.add_tests_folder()
		self.add_tests_context()
		
		self.logger.logger.info(
			f'The tests have been added to the repo'
			)

	def add_docs_folder(self):
		"""
		Adds the folder for the documentation.
		"""

		self.docs_path = self.path / 'docs'
		self.docs_path.mkdir()
		
		self.logger.logger.info(
			f'The docs folder has been added to the repo'
			)

	def add_docs_quickstart(self):
		"""
		Generates all the documentation by using sphinx-quickstart.
		"""

		ps = pops.PopenSpawn('powershell', timeout = 3)
		ps.expect('>')
		ps.sendline('cd {}'.format(self.docs_path))
		ps.expect('>')
		ps.sendline('sphinx-quickstart')
		ps.expect(':')
		ps.sendline('y')
		ps.expect(':')
		ps.sendline(self.name)
		ps.expect(':')
		ps.sendline(self.owner)
		ps.expect(':')
		ps.sendline('0.1dev')
		ps.expect(':')
		ps.sendline('en')
		ps.expect('>')
		ps.sendline('dir')
		
		self.logger.logger.info('The sphinx-quickstart script was run successfully')

	def add_docs_conf(self):
		"""
		Modifies the conf.py file.
		"""

		conf_file = self.docs_path / 'source' / 'conf.py'
		
		count = 0
		while (count < 10):
			try:
				with open(conf_file, 'r') as f:
					text = f.read()
				count = 10
			except FileNotFoundError:
				count += 1
				time.sleep(0.5)

		text = text.replace('# import os', 'import os')
		text = text.replace('# import sys', 'import sys')

		path_string = '{}\n{}'.format(
			'import pathlib',
			'sys.path.insert(0, str(pathlib.Path.cwd().parent.parent))'
			)
		text = text.replace(
			"# sys.path.insert(0, os.path.abspath('.'))",
			path_string
			)

		extension_string = "extensions = [\n\t'{}',\n\t'{}',".format(
			'sphinx.ext.autodoc',
			'sphinx.ext.napoleon',
			)
		text = text.replace('extensions = [', extension_string)

		text = text.replace('alabaster', 'sphinxdoc')

		with open(conf_file, 'w') as f:
			f.write(text)

		self.logger.logger.info(f'The conf.py file has been modified')

	def add_docs_index(self):
		"""
		Modifies the index.rst file.
		"""

		index_file = self.docs_path / 'source' / 'index.rst'

		count = 0
		while (count < 10):
			try:
				with open(index_file, 'r') as f:
					text = f.read()
				count = 10
			except FileNotFoundError:
				count += 1
				time.sleep(0.5)
		insert = text.find('Indices') - 2
		
		modules_string = ''
		for mod in self.modules:
			modules_string = modules_string.join(
				'.. {}:: {}.{}\n\t:{}:\n\n'.format(
					'automodule',
					self.name,
					mod,
					'members',
					)
				)

		text = text[:insert] + modules_string + text[insert:]

		with open(index_file, 'w') as f:
			f.write(text)

		self.logger.logger.info(
				f'The index.rst file has been modified'
			)

	def add_docs_html(self):
		"""
		Makes the html documentation.
		"""

		ps = pops.PopenSpawn('powershell', timeout = 3)
		ps.expect('>')
		ps.sendline('cd {}'.format(self.docs_path))
		ps.expect('>')
		ps.sendline('make html')
		ps.expect('>')
		ps.sendline('dir')

		self.logger.logger.info(
				f'The html documentation has been generated'
			)

	def add_docs(self):
		"""
		Adds the documentation to the repo.
		"""

		self.add_docs_folder()
		self.add_docs_quickstart()
		self.add_docs_conf()
		self.add_docs_index()
		self.add_docs_html()

		self.logger.logger.info(
				f'The documentation has been added'
			)