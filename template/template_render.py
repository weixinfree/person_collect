import re

TEMPLATE_PATTERN = re.compile("{{(?P<var>.*?)}}|{%(?P<code>.*?)%}")


def parse_template(template):
    start = 0
    find_pattern = TEMPLATE_PATTERN.search(template, 0)

    while find_pattern:
        segment = template[start: find_pattern.start()]
        var = find_pattern.group('var')
        _code = find_pattern.group('code')

        yield segment, var, _code

        start = find_pattern.end()
        find_pattern = TEMPLATE_PATTERN.search(template, start)

    yield template[start:], None, None


class CodeBuilder:
    INDENT = ' ' * 4

    def __init__(self):
        self.codes = []
        self.cur_intent = 0
        pass

    def __repr__(self):
        return '\n'.join(self.codes)

    def add(self, string):
        self.codes.append(self.cur_intent * CodeBuilder.INDENT + string)
        return self

    def indent(self):
        self.cur_intent += 1
        return self

    def dedent(self):
        self.cur_intent -= 1
        return self


def compile_2_code(template):
    builder = CodeBuilder()

    builder.add('def gen_code(idl):')
    builder.indent()

    builder.add('render_result = []')
    builder.add('__append = render_result.append')

    for segment, var, _code in parse_template(template):

        builder.add(f"__append('''{segment}''')")
        if var:
            builder.add(f'__append({var.strip()})')
        if _code:
            if _code.strip() == 'end':
                builder.dedent()
            else:
                builder.add(f'{_code.strip()}')
                builder.indent()

    builder.add('java_code = "".join(render_result)')
    builder.add('return java_code')
    builder.dedent()
    return repr(builder)


if __name__ == '__main__':
    with open('track_code.schema', encoding='utf-8') as f:
        print(compile_2_code(f.read()), file=open('gen_code.py', 'w'))
