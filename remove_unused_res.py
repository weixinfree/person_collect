import os
from typing import Sequence, Tuple
import re
from collections import defaultdict
from pprint import pprint


def _java_files(root: str) -> Sequence[str]:
    for base, _, files in os.walk(root):
        yield from (os.path.join(base, file) for file in files if file.endswith(".java")
            or file.endswith('.kt'))


def _extract_code_ref(file: str) -> Sequence[Tuple[str, str]]:
    with open(file, encoding='utf-8') as f:
        content = f.read()

    return set(re.findall(r'R\.(\w+)\.([\w_]+)\b', content))


def _res_files(root: str) -> Sequence[str]:
    for base, _, files in os.walk(root):
        yield from (os.path.join(base, file) for file in files if '/res/' in base or file == 'AndroidManifest.xml')


def _extract_res_file_type(file: str) -> Tuple[str, str]:
    return os.path.split(os.path.dirname(file))[-1].split('-')[0], os.path.basename(file).split('.')[0]


def _extract_res_ref(file: str) -> Sequence[Tuple[str, str]]:

    if not file.endswith('.xml'):
        return set()

    with open(file, encoding='utf-8') as f:
        content = f.read()

        return set(re.findall(r'@(\w+)/([\w_]+)', content))


def _remove_file(file: str):
    os.remove(file)


def main(root: str):

    res = defaultdict(set)
    res_file_map = {}
    res_refs = defaultdict(set)

    for res_file in _res_files(root):
        res_type, res_name = _extract_res_file_type(res_file)
        res_file_map[(res_type, res_name)] = res_file
        res[res_type].add(res_name)

        refs = _extract_res_ref(res_file)

        for ref_type, ref_name in refs:
            res_refs[ref_type].add(ref_name)

    for java_file in _java_files(root):
        refs = _extract_code_ref(java_file)
        for ref_type, ref_name in refs:
            res_refs[ref_type].add(ref_name)

    # pprint(res_refs)
    # return

    index = 0

    for res_type, res_values in res.items():

        if res_type in {'values','xml','debug', 'main', 'mipmap'}:
            continue

        type_refs = res_refs[res_type]

        for res in res_values:

            # react 依赖
            if re.search(r'^react_resource', res):
                continue

            # keep.xml 比较特殊
            if res == 'keep':
                continue

            # manifest
            if 'AndroidManifest' in res:
                continue


            if res not in type_refs:
                index += 1
                file = res_file_map[(res_type, res)]
                print(index, res_type, res, file)
                _remove_file(file)


if __name__ == '__main__':
    root = os.path.join(os.path.abspath(os.curdir), 'app', 'src')
    main(root)
