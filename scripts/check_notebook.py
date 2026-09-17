"""Проверка ноутбука на воспроизводимость: синтаксис + порядок определения имён.

Запуск:  python scripts/check_notebook.py notebooks/final_solution_15541.ipynb
"""
import ast
import builtins
import json
import sys


class Collect(ast.NodeVisitor):
    """Собирает имена, определяемые и используемые на верхнем уровне ячейки.
    Имена внутри функций не считаются использованными: они разрешаются при вызове."""

    def __init__(self):
        self.defs, self.uses, self.local = set(), set(), [set()]

    def visit_FunctionDef(self, n):
        self.defs.add(n.name)
        args = {a.arg for a in n.args.args + n.args.kwonlyargs}
        if n.args.vararg:
            args.add(n.args.vararg.arg)
        if n.args.kwarg:
            args.add(n.args.kwarg.arg)
        self.local.append(args)
        for s in n.body:
            self.visit(s)
        self.local.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, n):
        self.local.append({a.arg for a in n.args.args})
        self.visit(n.body)
        self.local.pop()

    def visit_ClassDef(self, n):
        self.defs.add(n.name)
        self.local.append(set())
        for s in n.body:
            self.visit(s)
        self.local.pop()

    def _comp(self, n, is_dict=False):
        self.local.append(set())
        for g in n.generators:
            self.visit(g.iter)
            for t in ast.walk(g.target):
                if isinstance(t, ast.Name):
                    self.local[-1].add(t.id)
            for f in g.ifs:
                self.visit(f)
        if is_dict:
            self.visit(n.key); self.visit(n.value)
        else:
            self.visit(n.elt)
        self.local.pop()

    def visit_ListComp(self, n): self._comp(n)
    visit_SetComp = visit_GeneratorExp = visit_ListComp
    def visit_DictComp(self, n): self._comp(n, True)

    def visit_Name(self, n):
        if isinstance(n.ctx, ast.Store):
            (self.local[-1] if len(self.local) > 1 else self.defs).add(n.id)
        elif not any(n.id in s for s in self.local[1:]):
            self.uses.add(n.id)

    def visit_Import(self, n):
        for a in n.names:
            self.defs.add((a.asname or a.name).split('.')[0])

    def visit_ImportFrom(self, n):
        for a in n.names:
            self.defs.add(a.asname or a.name)

    def visit_For(self, n):
        for t in ast.walk(n.target):
            if isinstance(t, ast.Name):
                (self.local[-1] if len(self.local) > 1 else self.defs).add(t.id)
        self.generic_visit(n)

    def visit_ExceptHandler(self, n):
        if n.name:
            self.defs.add(n.name)
        self.generic_visit(n)

    def visit_withitem(self, n):
        if n.optional_vars:
            for t in ast.walk(n.optional_vars):
                if isinstance(t, ast.Name):
                    (self.local[-1] if len(self.local) > 1 else self.defs).add(t.id)
        self.visit(n.context_expr)

    def visit_arg(self, n):
        pass


def check(path):
    nb = json.load(open(path, encoding='utf-8'))
    defined = set(dir(builtins)) | {'display', 'get_ipython', '__name__'}
    syntax_errors, order_problems = [], []

    for i, c in enumerate(nb['cells']):
        if c['cell_type'] != 'code':
            continue
        src = ''.join(c['source'])
        # строки shell-магии не являются питоном
        src = '\n'.join('#' + l if l.lstrip().startswith(('!', '%')) else l
                        for l in src.split('\n'))
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            syntax_errors.append((i, str(e)))
            continue
        col = Collect()
        for st in tree.body:
            col.visit(st)
        missing = sorted(u for u in col.uses if u not in defined and u not in col.defs)
        if missing:
            order_problems.append((i, missing))
        defined |= col.defs

    print(f'{path}: {len(nb["cells"])} ячеек')
    print(f'синтаксических ошибок: {len(syntax_errors)}')
    for i, e in syntax_errors:
        print(f'  ячейка {i}: {e}')
    print(f'имён, использованных до определения: {len(order_problems)}')
    for i, m in order_problems:
        print(f'  ячейка {i}: {m}')
    return not syntax_errors


if __name__ == '__main__':
    ok = check(sys.argv[1] if len(sys.argv) > 1 else 'notebooks/final_solution_15541.ipynb')
    sys.exit(0 if ok else 1)
