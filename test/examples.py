# Copyright 2016  Mateusz Bysiek  http://mbdev.pl/
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

"""
Examples used in unit tests.
"""

import typed_ast.ast35
import typed_astunparse

MODES = ['exec', 'eval', 'single']

EXAMPLES = {
    'function definiton': {
        'code': "def negation(arg):\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast35.FunctionDef(
            'negation',
            typed_ast.ast35.arguments(
                [typed_ast.ast35.arg('arg', None)],
                None, [], [], None, []),
            [typed_ast.ast35.Return(typed_ast.ast35.UnaryOp(
                typed_ast.ast35.Not(), typed_ast.ast35.Name('arg', typed_ast.ast35.Load())
                ))],
            [], None, None
            ),
        'dump': \
            "FunctionDef(name='negation',args=arguments(" \
                "args=[arg(arg='arg',annotation=None)]," \
                "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[])," \
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))]," \
            "decorator_list=[],returns=None,type_comment=None)"
        },
    'function definition with type annotations': {
        'code': "def negation(arg: bool) -> bool:\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast35.FunctionDef(
            'negation',
            typed_ast.ast35.arguments(
                [typed_ast.ast35.arg('arg', typed_ast.ast35.Name('bool', typed_ast.ast35.Load()))],
                None, [], [], None, []),
            [typed_ast.ast35.Return(typed_ast.ast35.UnaryOp(
                typed_ast.ast35.Not(), typed_ast.ast35.Name('arg', typed_ast.ast35.Load())
                ))],
            [], typed_ast.ast35.Name('bool', typed_ast.ast35.Load()), None
            ),
        'dump': \
            "FunctionDef(name='negation',args=arguments(" \
                "args=[arg(arg='arg',annotation=Name(id='bool',ctx=Load()))]," \
                "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[])," \
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))]," \
            "decorator_list=[],returns=Name(id='bool',ctx=Load()),type_comment=None)"
        },
    'function definiton with type comment': {
        'code': "def negation(arg):\n    # type: (bool) -> bool\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast35.FunctionDef(
            'negation',
            typed_ast.ast35.arguments(
                [typed_ast.ast35.arg('arg', None)],
                None, [], [], None, []),
            [typed_ast.ast35.Return(typed_ast.ast35.UnaryOp(
                typed_ast.ast35.Not(), typed_ast.ast35.Name('arg', typed_ast.ast35.Load())
                ))],
            [], None, '(bool) -> bool'
            ),
        'dump': \
            "FunctionDef(name='negation',args=arguments(" \
                "args=[arg(arg='arg',annotation=None)]," \
                "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[])," \
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))]," \
            "decorator_list=[],returns=None,type_comment='(bool)->bool')"
        },
    'assignment with type comment': {
        'code': "my_string = None # type: str",
        'is_expression': False,
        'tree': typed_ast.ast35.Assign(
            [typed_ast.ast35.Name('my_string', typed_ast.ast35.Store())],
            typed_ast.ast35.NameConstant(None),
            'str', None),
        'dump': \
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None)," \
            "type_comment='str',annotation=None)"
        },
    'for loop with type comment': {
        'code': "for i in [0, 4, 2, 42]: # type: int\n    print(i)",
        'is_expression': False,
        'tree': typed_ast.ast35.For(
            typed_ast.ast35.Name('i', typed_ast.ast35.Store()),
            typed_ast.ast35.List([
                typed_ast.ast35.Num(0), typed_ast.ast35.Num(4), typed_ast.ast35.Num(2),
                typed_ast.ast35.Num(42)], typed_ast.ast35.Load()),
            [typed_ast.ast35.Expr(typed_ast.ast35.Call(
                typed_ast.ast35.Name('print', typed_ast.ast35.Load()),
                [typed_ast.ast35.Name('i', typed_ast.ast35.Load())], []
                ))],
            [], 'int'
            ),
        'dump': \
            "For(" \
                "target=Name(id='i',ctx=Store())," \
                "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load())," \
                "body=[Expr(value=Call(func=Name(id='print',ctx=Load())," \
                    "args=[Name(id='i',ctx=Load())],keywords=[]))]," \
                "orelse=[],type_comment='int')"
        },
    'with statement with type comment': {
        'code': "with open('setup.py') as f: # type: typing.io.TextIO\n    print(f.read())",
        'is_expression': False,
        'tree': typed_ast.ast35.With(
            [typed_ast.ast35.withitem(
                typed_ast.ast35.Call(
                    typed_ast.ast35.Name('open', typed_ast.ast35.Load()),
                    [typed_ast.ast35.Str(s='setup.py')], []),
                typed_ast.ast35.Name('f', typed_ast.ast35.Store())
                )],
            [typed_ast.ast35.Expr(typed_ast.ast35.Call(
                typed_ast.ast35.Name('print', typed_ast.ast35.Load()),
                [typed_ast.ast35.Call(typed_ast.ast35.Attribute(
                    typed_ast.ast35.Name('f', typed_ast.ast35.Load()), 'read',
                    typed_ast.ast35.Load()), [], [])],
                []
                ))],
            'typing.io.TextIO'
            ),
        'dump': \
            "With(" \
                "items=[withitem(context_expr=Call(func=Name(id='open',ctx=Load())," \
                    "args=[Str(s='setup.py')],keywords=[])," \
                    "optional_vars=Name(id='f',ctx=Store()))]," \
                "body=[Expr(value=Call(" \
                    "func=Name(id='print',ctx=Load())," \
                    "args=[Call(" \
                        "func=Attribute(value=Name(id='f',ctx=Load()),attr='read',ctx=Load())," \
                        "args=[],keywords=[])]," \
                    "keywords=[]))]," \
                "type_comment='typing.io.TextIO')"
        },
    'addition': {
        'code': "(a + b)",
        'is_expression': True,
        'tree': typed_ast.ast35.BinOp(
            typed_ast.ast35.Name('a', typed_ast.ast35.Load()), typed_ast.ast35.Add(),
            typed_ast.ast35.Name('b', typed_ast.ast35.Load())),
        'dump': "BinOp(left=Name(id='a',ctx=Load()),op=Add(),right=Name(id='b',ctx=Load()))"
        }
    }

def _generate_variants(example: dict):
    if example['is_expression']:
        example['trees'] = {
            'exec': typed_ast.ast35.Module([typed_ast.ast35.Expr(example['tree'])], []),
            'eval': typed_ast.ast35.Expression(example['tree']),
            'single': typed_ast.ast35.Interactive([typed_ast.ast35.Expr(example['tree'])])
            }
        example['dumps'] = {
            'exec': 'Module(body=[Expr(value={})],type_ignores=[])'.format(example['dump']),
            'eval': 'Expression(body={})'.format(example['dump']),
            'single': 'Interactive(body=[Expr(value={})])'.format(example['dump'])
            }
    else:
        example['trees'] = {
            'exec': typed_ast.ast35.Module([example['tree']], []),
            'eval': None,
            'single': typed_ast.ast35.Interactive([example['tree']])
            }
        example['dumps'] = {
            'exec': 'Module(body=[{}],type_ignores=[])'.format(example['dump']),
            'eval': None,
            'single': 'Interactive(body=[{}])'.format(example['dump'])
            }

for _, _example in EXAMPLES.items():
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
                    tree_from_source = typed_ast.ast35.parse(
                        source=_example['code'], filename='<string>', mode=mode)
                except SyntaxError:
                    tree_from_source = None
                example_tree = None
            else:
                tree_from_source = typed_astunparse.dump(
                    typed_ast.ast35.parse(source=_example['code'], filename='<string>', mode=mode)
                    ).replace('\n', '').replace(' ', '')
                example_tree = typed_astunparse.dump(
                    _example['trees'][mode]).replace('\n', '').replace(' ', '')
            assert tree_from_source == example_tree, _MSG.format(
                _description, mode, tree_from_source, example_tree)
