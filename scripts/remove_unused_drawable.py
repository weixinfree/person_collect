import os
import re

PATH = os.path.abspath('.')

res_files = [os.path.join(base, file) for base, _, files in os.walk(PATH) if 'build' not in base and 'src' in base for
             file in files if file.endswith('.java') or file.endswith('.xml')]

# pprint(res_files)

drawable_files = {file[:-4]: os.path.join(base, file) for base, _, files in os.walk(PATH)
                  if 'build' not in base and 'src' in base and 'drawable' in base
                  for file in files if file.endswith('.png') and not file.endswith('.9.png')}

refs = set()
for file in res_files:
    with open(file, encoding='utf-8') as f:
        for line in f:

            if line.lstrip().startswith('#'): continue

            match = re.findall(r'R\.drawable\.(\w+)\b', line)
            if match:
                refs.update(set(match))

            match = re.findall(r'@drawable/(\w+)\b', line)
            if match:
                refs.update(set(match))

unused = drawable_files.keys() - refs
from pprint import pprint

for _un_use_img in unused:
    print(f'deleting {_un_use_img}')
    os.remove(drawable_files[_un_use_img])
