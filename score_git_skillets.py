import os
from pathlib import Path
from uuid import uuid4

from skilletlib.skilletLoader import SkilletLoader

uuid = str(uuid4())
repo_url = os.environ.get('repo_url', 'https://github.com/nembery/Skillets.git')
repo_name = os.environ.get('repo_name', uuid)
repo_branch = os.environ.get('repo_branch', 'master')
directory = os.environ.get('skillet_directory', '/tmp')
output_format = os.environ.get('skillet_format', 'table')

sl = SkilletLoader()

if '~' in directory:
    d = os.path.expanduser(directory)
else:
    d = directory

skillets = sl.load_from_git(repo_url, repo_name, repo_branch, local_dir=directory)

if output_format == 'table':
    print('_' * 138)
    print(f'|{"Skillet":^90}|{"Type":^15}|{"Vars":^4}|{"Snippets":^8}|{"Lines of Config":^15}|')
    print('_' * 138)
else:
    print('Skillet,Type,Variables,Snippets,Lines of Config')

for s in skillets:
    num_vars = len(s.variables)
    num_snippets = len(s.snippet_stack)
    num_xml_lines = 0
    if 'pan' in s.type:
        for snippet in s.get_snippets():
            if 'element' in snippet.metadata:
                num_xml_lines += len(snippet.metadata['element'].split('\n'))

    elif 'template' in s.type:
        for snippet in s.get_snippets():
            num_xml_lines += len(snippet.template_str.split('\n'))

    elif 'python3' in s.type:
        for snippet in s.get_snippets():
            if 'file' in snippet.metadata:
                p_path = Path(s.path).joinpath(snippet.metadata['file'])
                if p_path.exists():
                    with p_path.open() as python_file:
                        num_xml_lines += len(python_file.readlines())

    elif s.type == 'terraform':
        for f in Path(s.path).rglob('*.tf'):
            if f.exists():
                with f.open() as terraform_file:
                    num_xml_lines += len(terraform_file.readlines())

    if output_format == 'table':
        print(f'|{s.label:90}|{s.type:15}|{num_vars:4}|{num_snippets:8}|{num_xml_lines:15}|')
    else:
        print(f'{s.name},{s.type},{num_vars},{num_snippets},{num_xml_lines}')

if output_format == 'table':
    print('-' * 138)
