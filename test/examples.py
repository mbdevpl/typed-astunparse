# Copyright 2016-2017  Mateusz Bysiek  http://mbdev.pl/
# This file is part of typed-astunparse.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Examples used in unit tests."""

import os
import platform
import sys

import typed_ast.ast3
import typed_astunparse

MODES = ['exec', 'eval', 'single']

EXAMPLES = {
    'function definiton': {
        'code': "def negation(arg):\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'negation',
            typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('arg', None, None)],
                None, [], [], None, []),
            [typed_ast.ast3.Return(typed_ast.ast3.UnaryOp(
                typed_ast.ast3.Not(), typed_ast.ast3.Name('arg', typed_ast.ast3.Load())))],
            [], None, None),
        'dump':
            "FunctionDef(name='negation',args=arguments("
            "args=[arg(arg='arg',annotation=None,type_comment=None)],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))],"
            "decorator_list=[],returns=None,type_comment=None)"},
    'function definition with type annotations': {
        'code': "def negation(arg: bool) -> bool:\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'negation',
            typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('arg', typed_ast.ast3.Name('bool', typed_ast.ast3.Load()), None)],
                None, [], [], None, []),
            [typed_ast.ast3.Return(typed_ast.ast3.UnaryOp(
                typed_ast.ast3.Not(), typed_ast.ast3.Name('arg', typed_ast.ast3.Load())))],
            [], typed_ast.ast3.Name('bool', typed_ast.ast3.Load()), None),
        'dump':
            "FunctionDef(name='negation',args=arguments("
            "args=[arg(arg='arg',annotation=Name(id='bool',ctx=Load()),type_comment=None)],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))],"
            "decorator_list=[],returns=Name(id='bool',ctx=Load()),type_comment=None)"},
    'function definiton with type comment': {
        'code': "def negation(arg):\n    # type: (bool) -> bool\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'negation',
            typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('arg', None, None)],
                None, [], [], None, []),
            [typed_ast.ast3.Return(typed_ast.ast3.UnaryOp(
                typed_ast.ast3.Not(), typed_ast.ast3.Name('arg', typed_ast.ast3.Load())))],
            [], None, '(bool) -> bool'),
        'dump':
            "FunctionDef(name='negation',args=arguments("
            "args=[arg(arg='arg',annotation=None,type_comment=None)],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))],"
            "decorator_list=[],returns=None,type_comment='(bool)->bool')"},
    'decorated function with type comment': {
        'code': '@deco\ndef do_nothing():\n    # type: () -> None\n    pass',
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            name='do_nothing',
            args=typed_ast.ast3.arguments([], None, [], [], None, []),
            body=[typed_ast.ast3.Pass()],
            decorator_list=[typed_ast.ast3.Name(id='deco', ctx=typed_ast.ast3.Load())],
            returns=None, type_comment='() -> None'),
        'dump':
            "FunctionDef("
            "name='do_nothing',"
            "args=arguments("
            "args=[],vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[Name(id='deco',ctx=Load())],"
            "returns=None,type_comment='()->None')"},
    'function with type comment and annotations': {
        'code': 'def do_nothing() -> None:\n    # type: () -> None\n    pass',
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            name='do_nothing',
            args=typed_ast.ast3.arguments([], None, [], [], None, []),
            body=[typed_ast.ast3.Pass()], decorator_list=[],
            returns=typed_ast.ast3.NameConstant(value=None), type_comment='() -> None'),
        'dump':
            "FunctionDef("
            "name='do_nothing',"
            "args=arguments("
            "args=[],vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[],"
            "returns=NameConstant(value=None),type_comment='()->None')"},
    'assignment': {
        'code': "my_string = None",
        'is_expression': False,
        'tree': typed_ast.ast3.Assign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None), None),
        'dump':
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None),"
            "type_comment=None)"},
    'assignment with type comment': {
        'code': "my_string = None # type: str",
        'is_expression': False,
        'tree': typed_ast.ast3.Assign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None), 'str'),
        'dump':
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None),"
            "type_comment='str')"},
    'tuple unpacking assignment with type comment': {
        'code': "(my_string, my_int) = my_list # type: str, int",
        'is_expression': False,
        'tree': typed_ast.ast3.Assign(
            [typed_ast.ast3.Tuple(
                [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
                 typed_ast.ast3.Name('my_int', typed_ast.ast3.Store())],
                typed_ast.ast3.Store())],
            typed_ast.ast3.Name('my_list', typed_ast.ast3.Load()),
            'str, int'),
        'dump':
            "Assign("
            "targets=[Tuple(elts=["
            "Name(id='my_string',ctx=Store()),Name(id='my_int',ctx=Store())"
            "],ctx=Store())],"
            "value=Name(id='my_list',ctx=Load()),"
            "type_comment='str,int')"},
    'assignment with type annotation': {
        'code': "my_string: str = None",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()),
            typed_ast.ast3.NameConstant(None), 1),
        'dump':
            "AnnAssign(target=Name(id='my_string',ctx=Store()),"
            "annotation=Name(id='str',ctx=Load()),value=NameConstant(value=None),simple=1)"},
    'variable declaration with type annotation': {
        'code': "my_string: str",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()), None, 1),
        'dump':
            "AnnAssign(target=Name(id='my_string',ctx=Store()),"
            "annotation=Name(id='str',ctx=Load()),value=None,simple=1)"},
    'for-else loop': {
        'code': "for i in [0, 4, 2, 42]:\n    print(i)\nelse:\n    print('hmm')",
        'is_expression': False,
        'tree': typed_ast.ast3.For(
            typed_ast.ast3.Name('i', typed_ast.ast3.Store()),
            typed_ast.ast3.List([
                typed_ast.ast3.Num(0), typed_ast.ast3.Num(4), typed_ast.ast3.Num(2),
                typed_ast.ast3.Num(42)], typed_ast.ast3.Load()),
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Name('i', typed_ast.ast3.Load())], []))],
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Str('hmm')], []))],
            None),
        'dump':
            "For("
            "target=Name(id='i',ctx=Store()),"
            "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load()),"
            "body=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Name(id='i',ctx=Load())],keywords=[]))],"
            "orelse=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Str(s='hmm')],keywords=[]))],type_comment=None)"},
    'for loop with type comment': {
        'code': "for i in [0, 4, 2, 42]: # type: int\n    print(i)",
        'is_expression': False,
        'tree': typed_ast.ast3.For(
            typed_ast.ast3.Name('i', typed_ast.ast3.Store()),
            typed_ast.ast3.List([
                typed_ast.ast3.Num(0), typed_ast.ast3.Num(4), typed_ast.ast3.Num(2),
                typed_ast.ast3.Num(42)], typed_ast.ast3.Load()),
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Name('i', typed_ast.ast3.Load())], []))],
            [], 'int'),
        'dump':
            "For("
            "target=Name(id='i',ctx=Store()),"
            "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load()),"
            "body=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Name(id='i',ctx=Load())],keywords=[]))],"
            "orelse=[],type_comment='int')"},
    'for-else loop with type comment': {
        'code': "for i in [0, 4, 2, 42]: # type: int\n    print(i)\nelse:\n    print('hmm')",
        'is_expression': False,
        'tree': typed_ast.ast3.For(
            typed_ast.ast3.Name('i', typed_ast.ast3.Store()),
            typed_ast.ast3.List([
                typed_ast.ast3.Num(0), typed_ast.ast3.Num(4), typed_ast.ast3.Num(2),
                typed_ast.ast3.Num(42)], typed_ast.ast3.Load()),
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Name('i', typed_ast.ast3.Load())], []))],
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Str('hmm')], []))],
            'int'),
        'dump':
            "For("
            "target=Name(id='i',ctx=Store()),"
            "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load()),"
            "body=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Name(id='i',ctx=Load())],keywords=[]))],"
            "orelse=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Str(s='hmm')],keywords=[]))],type_comment='int')"},
    'if-elif-else': {
        'code': "if False:\n    pass\nelif True:\n    pass\nelse:\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.If(
            test=typed_ast.ast3.NameConstant(value=False),
            body=[typed_ast.ast3.Pass()],
            orelse=[typed_ast.ast3.If(
                test=typed_ast.ast3.NameConstant(value=True), body=[typed_ast.ast3.Pass()],
                orelse=[typed_ast.ast3.Pass()])]),
        'dump':
            "If("
            "test=NameConstant(value=False),body=[Pass()],"
            "orelse=[If(test=NameConstant(value=True),body=[Pass()],orelse=[Pass()])]"
            ")"},
    'with statement': {
        'code': "with open('setup.py') as f:\n    print(f.read())",
        'is_expression': False,
        'tree': typed_ast.ast3.With(
            [typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str(s='setup.py')], []),
                typed_ast.ast3.Name('f', typed_ast.ast3.Store()))],
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Call(typed_ast.ast3.Attribute(
                    typed_ast.ast3.Name('f', typed_ast.ast3.Load()), 'read',
                    typed_ast.ast3.Load()), [], [])],
                []))],
            None),
        'dump':
            "With("
            "items=[withitem(context_expr=Call(func=Name(id='open',ctx=Load()),"
            "args=[Str(s='setup.py')],keywords=[]),"
            "optional_vars=Name(id='f',ctx=Store()))],"
            "body=[Expr(value=Call("
            "func=Name(id='print',ctx=Load()),"
            "args=[Call("
            "func=Attribute(value=Name(id='f',ctx=Load()),attr='read',ctx=Load()),"
            "args=[],keywords=[])],"
            "keywords=[]))],"
            "type_comment=None)"},
    'with statement with type comment': {
        'code': "with open('setup.py') as f: # type: typing.io.TextIO\n    print(f.read())",
        'is_expression': False,
        'tree': typed_ast.ast3.With(
            [typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str(s='setup.py')], []),
                typed_ast.ast3.Name('f', typed_ast.ast3.Store()))],
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Call(typed_ast.ast3.Attribute(
                    typed_ast.ast3.Name('f', typed_ast.ast3.Load()), 'read',
                    typed_ast.ast3.Load()), [], [])],
                []))],
            'typing.io.TextIO'),
        'dump':
            "With("
            "items=[withitem(context_expr=Call(func=Name(id='open',ctx=Load()),"
            "args=[Str(s='setup.py')],keywords=[]),"
            "optional_vars=Name(id='f',ctx=Store()))],"
            "body=[Expr(value=Call("
            "func=Name(id='print',ctx=Load()),"
            "args=[Call("
            "func=Attribute(value=Name(id='f',ctx=Load()),attr='read',ctx=Load()),"
            "args=[],keywords=[])],"
            "keywords=[]))],"
            "type_comment='typing.io.TextIO')"},
    'multi-context with statement with type comment': {
        'code':
            "with open('setup.py') as f1, open('README.rst') as f2:"
            " # type: typing.io.TextIO, typing.io.TextIO\n"
            "    print(f1.read())\n    print(f2.read())",
        'is_expression': False,
        'tree': typed_ast.ast3.With(
            [typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str(s='setup.py')], []),
                typed_ast.ast3.Name('f1', typed_ast.ast3.Store())),
             typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str(s='README.rst')], []),
                typed_ast.ast3.Name('f2', typed_ast.ast3.Store()))],
            [typed_ast.ast3.Expr(typed_ast.ast3.Call(
                typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                [typed_ast.ast3.Call(typed_ast.ast3.Attribute(
                    typed_ast.ast3.Name('f1', typed_ast.ast3.Load()), 'read',
                    typed_ast.ast3.Load()), [], [])],
                [])),
             typed_ast.ast3.Expr(typed_ast.ast3.Call(
                 typed_ast.ast3.Name('print', typed_ast.ast3.Load()),
                 [typed_ast.ast3.Call(typed_ast.ast3.Attribute(
                     typed_ast.ast3.Name('f2', typed_ast.ast3.Load()), 'read',
                     typed_ast.ast3.Load()), [], [])],
                 []))],
            'typing.io.TextIO, typing.io.TextIO'),
        'dump':
            "With("
            "items=[withitem(context_expr=Call(func=Name(id='open',ctx=Load()),"
            "args=[Str(s='setup.py')],keywords=[]),"
            "optional_vars=Name(id='f1',ctx=Store())),"
            "withitem(context_expr=Call(func=Name(id='open',ctx=Load()),"
            "args=[Str(s='README.rst')],keywords=[]),"
            "optional_vars=Name(id='f2',ctx=Store()))],"
            "body=[Expr(value=Call("
            "func=Name(id='print',ctx=Load()),"
            "args=[Call("
            "func=Attribute(value=Name(id='f1',ctx=Load()),attr='read',ctx=Load()),"
            "args=[],keywords=[])],"
            "keywords=[])),"
            "Expr(value=Call("
            "func=Name(id='print',ctx=Load()),"
            "args=[Call("
            "func=Attribute(value=Name(id='f2',ctx=Load()),attr='read',ctx=Load()),"
            "args=[],keywords=[])],"
            "keywords=[]))],"
            "type_comment='typing.io.TextIO,typing.io.TextIO')"},
    'addition': {
        'code': "(a + b)",
        'is_expression': True,
        'tree': typed_ast.ast3.BinOp(
            typed_ast.ast3.Name('a', typed_ast.ast3.Load()), typed_ast.ast3.Add(),
            typed_ast.ast3.Name('b', typed_ast.ast3.Load())),
        'dump':
            "BinOp(left=Name(id='a',ctx=Load()),op=Add(),right=Name(id='b',ctx=Load()))"},
    'attribute of integer literal': {
        'code': "3 .__abs__()",
        'is_expression': True,
        'tree': typed_ast.ast3.Call(
            func=typed_ast.ast3.Attribute(
                value=typed_ast.ast3.Num(n=3),
                attr='__abs__', ctx=typed_ast.ast3.Load()),
            args=[], keywords=[]),
        'dump':
            "Call(func=Attribute(value=Num(n=3),attr='__abs__',ctx=Load()),args=[],keywords=[])"}}

INVALID_EXAMPLES = {
    # 'chained assignment with type annotation': {
    #     'code': "my_string: str = my_string2 = None",
    #     'is_expression': False,
    #     'tree': typed_ast.ast3.AnnAssign(
    #         [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
    #          typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
    #         typed_ast.ast3.NameConstant(None),
    #         typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
    #     'dump': "None"},
    # 'tuple unpacking assignment with one type annotation': {
    #     'code': "my_string, my_string2: str = my_tuple",
    #     'is_expression': False,
    #     'tree': typed_ast.ast3.AnnAssign(
    #         [typed_ast.ast3.Tuple(
    #             [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
    #              typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
    #             typed_ast.ast3.Store())],
    #         typed_ast.ast3.Name('my_tuple', typed_ast.ast3.Load()),
    #         typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
    #     'dump': "None"},
    # 'tuple unpacking assignment with multiple type annotations': {
    #     'code': "my_string: str, my_string2: str = my_tuple",
    #     'is_expression': False,
    #     'tree': typed_ast.ast3.AnnAssign(
    #         [typed_ast.ast3.Tuple(
    #             [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
    #              typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
    #             typed_ast.ast3.Store())],
    #         typed_ast.ast3.Name('my_tuple', typed_ast.ast3.Load()),
    #         typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
    #     'dump': "None"},
    # 'assignment with type comment and annotation': {
    #     'code': "my_string: str = None # type: str",
    #     'is_expression': False,
    #     'tree': typed_ast.ast3.AnnAssign(
    #         [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
    #         typed_ast.ast3.NameConstant(None),
    #         typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
    #     'dump': "None"}
    }


def _generate_variants(example: dict):
    if example['is_expression']:
        example['trees'] = {
            'exec': typed_ast.ast3.Module([typed_ast.ast3.Expr(example['tree'])], []),
            'eval': typed_ast.ast3.Expression(example['tree']),
            'single': typed_ast.ast3.Interactive([typed_ast.ast3.Expr(example['tree'])])}
        example['dumps'] = {
            'exec': 'Module(body=[Expr(value={})],type_ignores=[])'.format(example['dump']),
            'eval': 'Expression(body={})'.format(example['dump']),
            'single': 'Interactive(body=[Expr(value={})])'.format(example['dump'])}
    else:
        example['trees'] = {
            'exec': typed_ast.ast3.Module([example['tree']], []),
            'eval': None,
            'single': typed_ast.ast3.Interactive([example['tree']])}
        example['dumps'] = {
            'exec': 'Module(body=[{}],type_ignores=[])'.format(example['dump']),
            'eval': None,
            'single': 'Interactive(body=[{}])'.format(example['dump'])}

for _, _example in EXAMPLES.items():
    _generate_variants(_example)

for _, _example in INVALID_EXAMPLES.items():
    _generate_variants(_example)

# verify examples
if __debug__:
    _MSG = '''example for {} in '{}' mode is incorrect:
"""
{}
"""
tree from source (above) != example tree (below)
"""
{}
"""'''
    for _description, _example in EXAMPLES.items():
        for mode in MODES:
            if _example['trees'][mode] is None:
                try:
                    tree_from_source = typed_ast.ast3.parse(
                        source=_example['code'], filename='<string>', mode=mode)
                except SyntaxError:
                    tree_from_source = None
                example_tree = None
            else:
                tree_from_source = typed_astunparse.dump(
                    typed_ast.ast3.parse(source=_example['code'], filename='<string>', mode=mode)
                    ).replace('\n', '').replace(' ', '')
                example_tree = typed_astunparse.dump(
                    _example['trees'][mode]).replace('\n', '').replace(' ', '')
            assert tree_from_source == example_tree, _MSG.format(
                _description, mode, tree_from_source, example_tree)

_ROOT_DIRECTORY_PARTS = [getattr(sys, 'real_prefix', sys.prefix), 'lib']
if platform.system() != 'Windows':
    _ROOT_DIRECTORY_PARTS.append('python{}.{}'.format(*sys.version_info[:2]))

_ROOT_DIRECTORY = os.path.join(*_ROOT_DIRECTORY_PARTS)

# verify root directory
if __debug__:
    assert isinstance(_ROOT_DIRECTORY, str), _ROOT_DIRECTORY
    assert len(_ROOT_DIRECTORY) > 0
    assert os.path.isdir(_ROOT_DIRECTORY), _ROOT_DIRECTORY

PATHS = sorted([
    os.path.join(_ROOT_DIRECTORY, n)
    for n in os.listdir(_ROOT_DIRECTORY)
    if n.endswith('.py') and not n.startswith('bad')])

# verify found paths
if __debug__:
    # On Ubuntu, Python built from source: 169 in 3.5.2, 170 in 3.6.0
    assert len(PATHS) > 150, len(PATHS)
