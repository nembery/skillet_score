import os

from skilletlib.skilletLoader import SkilletLoader

output_format = os.environ.get('skillet_output', 'table')
directory = os.environ.get('skillet_directory', '~/.pan_cnc/panhandler/repositories/')
sl = SkilletLoader()

if '~' in directory:
    d = os.path.expanduser('~/.pan_cnc/panhandler/repositories/')
else:
    d = directory

skillets = sl.load_all_skillets_from_dir(d)

if output_format == 'table':
    print('_' * 132)
    print(f'|{"Skillet":^90}|{"Type":^15}|{"Vars":^4}|{"Snippets":^8}|{"Lines of Config":^15}|')
    print('_' * 132)
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

    if output_format == 'table':
        print(f'|{s.label:90}|{s.type:15}|{num_vars:4}|{num_snippets:8}|{num_xml_lines:15}|')
    else:
        print(f'{s.name},{s.type},{num_vars},{num_snippets},{num_xml_lines}')

if output_format == 'table':
    print('-' * 132)
