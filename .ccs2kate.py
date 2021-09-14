#!/usr/bin/python3

# I hate CCS so much
# This is like my 2nd day here and I hate it so much I would rather waste time making this script
# Noorquacker, 2021-09-12
# Converts a Formula Electric CCS project into a .kateproject with clangd LSP n stuff
# If you like vscode, add your own fanciness

import os, sys

def search_dir():
	project_dir = False
	for d in os.scandir():
		if d.is_dir():
			for d2 in os.scandir(d.path):
				if d2.name == '.ccsproject':
					project_dir = d.path
	if not project_dir:
		print('Could not find a ccsproject in any directory. Are you in the right path?', file=sys.stderr)
		return False
	# Strip the ./ from the beginning
	return project_dir.strip('./')

def gen_builddirs(project_dir, debug=True, release=True):
	if debug:
		os.makedirs(f'{project_dir}/Debug', exist_ok=True)
	if release:
		os.makedirs(f'{project_dir}/Release', exist_ok=True)
	return True

def recursive_source_lookup(path):
	paths = []
	for i in os.scandir(path):
		if i.is_dir() and not i.name.startswith('.'):
			print(f'Recursing into {i.path}')
			paths.extend(recursive_source_lookup(i.path))
		elif i.name.endswith('.cpp') or i.name.endswith('.c') or i.name.endswith('.h'):
			paths.append(i.path)
	return paths

def find_sources(project_dir):
	'''
	Might be prone to breaking
	'''
	# TODO: actually make a good build system! This is crap!
	sources = {'include_dir': None, 'source_dir': None}
	all_sources = recursive_source_lookup(project_dir)
	for i in all_sources:
		if i.endswith('.h'):
			sources['include'] = '/'.join(i.split('/')[:-1])
	return sources

def main():
	project_dir = search_dir()
	if not project_dir:
		return False
	print(f'Found project directory "{project_dir}"')
	print(find_sources(project_dir))


if __name__ == '__main__':
	if not main():
		sys.exit(1)
