"""
移除项目中的无用代码
"""



import os
from typing import Sequence
import re
from functools import lru_cache


def _java_files(root: str) -> Sequence[str]:
    for base, _, files in os.walk(root):
        yield from (os.path.join(base, file) for file in files if file.endswith(".java"))


def _res_files(root: str) -> Sequence[str]:
    for base, _, files in os.walk(root):
        yield from (os.path.join(base, file) for file in files if file.endswith('.xml'))


def _extract_res_ref(file: str) -> Sequence[str]:
    with open(file, encoding='utf-8') as f:
        content = f.read()

        return set(re.findall(r'<\s*([\w.]+)\b', content))

@lru_cache(10)
def _extract_package(content: str) -> str:
    _match_package = re.search(f'^package\s+([\w.]+)', content)
    if not _match_package:
        return

    return _match_package.group(1)


def _extract_class(content: str) -> Sequence[str]:
    if not content:
        return

    _package = _extract_package(content)
    if not _package:
        return

    _classes = re.findall(r'public\s+class\s+(\w+)\b', content)
    return list(f'{_package}.{_clazz}' for _clazz in _classes)[:1]


def _extract_imports(content: str) -> Sequence[str]:
    return re.findall(r'import\s+([\w.]+)', content)


def _gen_fake_imports(content: str) -> Sequence[str]:
    _package = _extract_package(content)

    content = re.sub(r"\s+class\s+\w+\s+", '', content)
    content = re.sub(r'^.*\s+TAG\s+=.*$', '', content)
    content = re.sub(r'\s*public\s+\w+\s*\(', '', content)

    yield from (f'{_package}.{_item}' for _item in re.findall(r'\b(\w+)\b', content)
                if _item
                and _item[0].upper() == _item[0]
                and re.match(r'[A-Z]\w+', _item))


def _remove_file(file: str):
    os.remove(file)


def main(root: str):
    j_imports = set()
    j_classes = set()
    class_file_map = {}

    for java_file in _java_files(root):
        with open(java_file, encoding='utf-8') as f:
            content = f.read()
            classes = _extract_class(content)
            if classes:
                j_classes |= set(classes)

                for clazz in classes:
                    class_file_map[clazz] = java_file
            j_imports |= set(_extract_imports(content))
            j_imports |= set(_gen_fake_imports(content))

    for res_file in _res_files(root):
        refs = _extract_res_ref(res_file)
        j_imports |= refs

    print('**' * 20)

    print(len(j_classes), len(j_imports))

    print('==' * 20)

    for clz in j_classes:
        if clz not in j_imports:
            file = class_file_map[clz]
            print('class:', clz)

            if (input(f'delete class {clz} ? [y/n]. ').strip() != 'n'):
                _remove_file(file)

            # _remove_file(file)


if __name__ == '__main__':
    root = os.path.join(os.path.abspath(os.curdir), 'app', 'src')
    main(root)