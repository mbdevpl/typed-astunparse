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
                [typed_ast.ast3.arg(
                    'arg', typed_ast.ast3.Name('bool', typed_ast.ast3.Load()), None)],
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
    'function definiton with per-argument type comment': {
        'code':
            "def negation(arg  # type: bool\n"
            "        ):\n    # type: (...) -> bool\n    return (not arg)",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'negation',
            typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('arg', None, 'bool')],
                None, [], [], None, []),
            [typed_ast.ast3.Return(typed_ast.ast3.UnaryOp(
                typed_ast.ast3.Not(), typed_ast.ast3.Name('arg', typed_ast.ast3.Load())))],
            [], None, '(...) -> bool'),
        'dump':
            "FunctionDef(name='negation',args=arguments("
            "args=[arg(arg='arg',annotation=None,type_comment='bool')],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Return(value=UnaryOp(op=Not(),operand=Name(id='arg',ctx=Load())))],"
            "decorator_list=[],returns=None,type_comment='(...)->bool')"},
    'function definiton with several per-argument type comments': {
        'code':
            "def lovely(spam,  # type: bool\n"
            "        eggs=None,  # type: int\n"
            "        ham=None  # type: str\n"
            "        ):\n    # type: (...) -> bool\n    return spam",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'lovely', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('spam', None, 'bool'),
                 typed_ast.ast3.arg('eggs', None, 'int'),
                 typed_ast.ast3.arg('ham', None, 'str')],
                None, [], [], None, [
                    typed_ast.ast3.NameConstant(value=None),
                    typed_ast.ast3.NameConstant(value=None)]),
            [typed_ast.ast3.Return(typed_ast.ast3.Name('spam', typed_ast.ast3.Load()))],
            [], None, '(...) -> bool'),
        'dump':
            "FunctionDef(name='lovely',args=arguments("
            "args=[arg(arg='spam',annotation=None,type_comment='bool'),"
            "arg(arg='eggs',annotation=None,type_comment='int'),"
            "arg(arg='ham',annotation=None,type_comment='str')],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=["
            "NameConstant(value=None),NameConstant(value=None)]),"
            "body=[Return(value=Name(id='spam',ctx=Load()))],"
            "decorator_list=[],returns=None,type_comment='(...)->bool')"},
    'function definiton with per-argument type comments and annotations': {
        'code':
            "def fun(a,  # type: int\n"
            "        b: float, c  # type: str\n"
            "        ):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('a', None, 'int'), typed_ast.ast3.arg(
                    'b', typed_ast.ast3.Name(id='float', ctx=typed_ast.ast3.Load()), None),
                 typed_ast.ast3.arg('c', None, 'str')],
                None, [], [], None, []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[arg(arg='a',annotation=None,type_comment='int'),"
            "arg(arg='b',annotation=Name(id='float',ctx=Load()),type_comment=None),"
            "arg(arg='c',annotation=None,type_comment='str')],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with some arguments typed': {
        'code':
            "def fun(a, b,  # type: float\n"
            "        c=''  # type: str\n"
            "        ):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('a', None, None), typed_ast.ast3.arg('b', None, 'float'),
                 typed_ast.ast3.arg('c', None, 'str')],
                None, [], [], None, [typed_ast.ast3.Str('', '')]),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[arg(arg='a',annotation=None,type_comment=None),"
            "arg(arg='b',annotation=None,type_comment='float'),"
            "arg(arg='c',annotation=None,type_comment='str')],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[Str(s='',kind='')]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with some keyword-only arguments typed': {
        'code':
            "def fun(a, *, b,  # type: float\n"
            "        c=''  # type: str\n"
            "        ):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('a', None, None)], None,
                [typed_ast.ast3.arg('b', None, 'float'), typed_ast.ast3.arg('c', None, 'str')],
                [None, typed_ast.ast3.Str('', '')], None, []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[arg(arg='a',annotation=None,type_comment=None)],"
            "vararg=None,kwonlyargs=["
            "arg(arg='b',annotation=None,type_comment='float'),"
            "arg(arg='c',annotation=None,type_comment='str')],"
            "kw_defaults=[None,Str(s='',kind='')],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with normal and keyword-only arguments typed': {
        'code':
            "def fun(a,  # type: int\n"
            "        *args, b,  # type: float\n"
            "        c='',  # type: str\n"
            "        **kwargs):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('a', None, 'int')],
                typed_ast.ast3.arg(arg='args', annotation=None, type_comment=None),
                [typed_ast.ast3.arg('b', None, 'float'), typed_ast.ast3.arg('c', None, 'str')],
                [None, typed_ast.ast3.Str('', '')],
                typed_ast.ast3.arg(arg='kwargs', annotation=None, type_comment=None), []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[arg(arg='a',annotation=None,type_comment='int')],"
            "vararg=arg(arg='args',annotation=None,type_comment=None),kwonlyargs=["
            "arg(arg='b',annotation=None,type_comment='float'),"
            "arg(arg='c',annotation=None,type_comment='str')],"
            "kw_defaults=[None,Str(s='',kind='')],"
            "kwarg=arg(arg='kwargs',annotation=None,type_comment=None),defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with only varargs and per-argument type comment': {
        'code':
            "def fun(*args: 'blahblahblah'  # type: tuple\n"
            "        ):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [], typed_ast.ast3.arg(
                    arg='args', annotation=typed_ast.ast3.Str('blahblahblah', ''),
                    type_comment='tuple'),
                [], [], None, []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[],vararg=arg(arg='args',annotation=Str(s='blahblahblah',kind=''),"
            "type_comment='tuple'),"
            "kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with only kwargs and per-argument type comment': {
        'code':
            "def fun(**kwargs: 'blahblahblah'  # type: dict\n"
            "        ):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [], None, [], [], typed_ast.ast3.arg(
                    arg='kwargs', annotation=typed_ast.ast3.Str('blahblahblah', ''),
                    type_comment='dict'), []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[],vararg=None,kwonlyargs=[],kw_defaults=[],"
            "kwarg=arg(arg='kwargs',annotation=Str(s='blahblahblah',kind=''),type_comment='dict'),"
            "defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
    'function definiton with last argument not typed': {
        'code':
            "def fun(a, b,  # type: float\n"
            "        c):\n    pass",
        'is_expression': False,
        'tree': typed_ast.ast3.FunctionDef(
            'fun', typed_ast.ast3.arguments(
                [typed_ast.ast3.arg('a', None, None), typed_ast.ast3.arg('b', None, 'float'),
                 typed_ast.ast3.arg('c', None, None)],
                None, [], [], None, []),
            [typed_ast.ast3.Pass()],
            [], None, None),
        'dump':
            "FunctionDef(name='fun',args=arguments("
            "args=[arg(arg='a',annotation=None,type_comment=None),"
            "arg(arg='b',annotation=None,type_comment='float'),"
            "arg(arg='c',annotation=None,type_comment=None)],"
            "vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[]),"
            "body=[Pass()],decorator_list=[],returns=None,type_comment=None)"},
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
        'code': "my_string = None  # type: str",
        'is_expression': False,
        'tree': typed_ast.ast3.Assign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None), 'str'),
        'dump':
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None),"
            "type_comment='str')"},
    'tuple unpacking assignment with type comment': {
        'code': "(my_string, my_int) = my_list  # type: str, int",
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
                [typed_ast.ast3.Str('hmm', '')], []))],
            None),
        'dump':
            "For("
            "target=Name(id='i',ctx=Store()),"
            "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load()),"
            "body=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Name(id='i',ctx=Load())],keywords=[]))],"
            "orelse=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Str(s='hmm',kind='')],keywords=[]))],type_comment=None)"},
    'for loop with type comment': {
        'code': "for i in [0, 4, 2, 42]:  # type: int\n    print(i)",
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
        'code': "for i in [0, 4, 2, 42]:  # type: int\n    print(i)\nelse:\n    print('hmm')",
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
                [typed_ast.ast3.Str('hmm', '')], []))],
            'int'),
        'dump':
            "For("
            "target=Name(id='i',ctx=Store()),"
            "iter=List(elts=[Num(n=0),Num(n=4),Num(n=2),Num(n=42)],ctx=Load()),"
            "body=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Name(id='i',ctx=Load())],keywords=[]))],"
            "orelse=[Expr(value=Call(func=Name(id='print',ctx=Load()),"
            "args=[Str(s='hmm',kind='')],keywords=[]))],type_comment='int')"},
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
                    [typed_ast.ast3.Str('setup.py', '')], []),
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
            "args=[Str(s='setup.py',kind='')],keywords=[]),"
            "optional_vars=Name(id='f',ctx=Store()))],"
            "body=[Expr(value=Call("
            "func=Name(id='print',ctx=Load()),"
            "args=[Call("
            "func=Attribute(value=Name(id='f',ctx=Load()),attr='read',ctx=Load()),"
            "args=[],keywords=[])],"
            "keywords=[]))],"
            "type_comment=None)"},
    'with statement with type comment': {
        'code': "with open('setup.py') as f:  # type: typing.io.TextIO\n    print(f.read())",
        'is_expression': False,
        'tree': typed_ast.ast3.With(
            [typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str('setup.py', '')], []),
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
            "args=[Str(s='setup.py',kind='')],keywords=[]),"
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
            "  # type: typing.io.TextIO, typing.io.TextIO\n"
            "    print(f1.read())\n    print(f2.read())",
        'is_expression': False,
        'tree': typed_ast.ast3.With(
            [typed_ast.ast3.withitem(
                typed_ast.ast3.Call(
                    typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                    [typed_ast.ast3.Str('setup.py', '')], []),
                typed_ast.ast3.Name('f1', typed_ast.ast3.Store())),
             typed_ast.ast3.withitem(
                 typed_ast.ast3.Call(
                     typed_ast.ast3.Name('open', typed_ast.ast3.Load()),
                     [typed_ast.ast3.Str('README.rst', '')], []),
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
            "args=[Str(s='setup.py',kind='')],keywords=[]),"
            "optional_vars=Name(id='f1',ctx=Store())),"
            "withitem(context_expr=Call(func=Name(id='open',ctx=Load()),"
            "args=[Str(s='README.rst',kind='')],keywords=[]),"
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
    'raw bytes': {
        'code': "br'''1\"\"\"2\'3\"4\\'\\'\\'\\n'''",
        'is_expression': True,
        'tree': typed_ast.ast3.Bytes(b'1\"\"\"2\'3\"4\\\'\\\'\\\'\\n', 'br'),
        'dump': "Bytes(s=b'1\"\"\"2\\'3\"4\\\\\\'\\\\\\'\\\\\\'\\\\n',kind='br')"},
    'raw string': {
        'code': "r'spam'",
        'is_expression': True,
        'tree': typed_ast.ast3.Str('spam', 'r'),
        'dump': "Str(s='spam',kind='r')"},
    'raw string variant': {
        'code': "R'spam'",
        'is_expression': True,
        'tree': typed_ast.ast3.Str('spam', 'R'),
        'dump': "Str(s='spam',kind='R')"},
    'unicode string': {
        'code': "u'spam'",
        'is_expression': True,
        'tree': typed_ast.ast3.Str('spam', 'u'),
        'dump': "Str(s='spam',kind='u')"},
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

UNVERIFIED_EXAMPLES = {
    'assignment with type comment stored as AST': {
        'code': "my_string = None  # type: str",
        'is_expression': False,
        'tree': typed_ast.ast3.Assign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None), typed_ast.ast3.Name('str', typed_ast.ast3.Load())),
        'dump':
            "Assign(targets=[Name(id='my_string',ctx=Store())],value=NameConstant(value=None),"
            "type_comment=Name(id='str',ctx=Load()))"},
    }

# 'raw bytes': {
#     'code': "rb'spam'",
#     'is_expression': True,
#     'tree': typed_ast.ast3.Bytes(b'spam'),
#     'dump': "Bytes(s='spam')"},
# 'raw bytes inverted prefix': {
#     'code': "br'spam'",
#     'is_expression': True,
#     'tree': typed_ast.ast3.Bytes(b'spam'),
#     'dump': "Bytes(s='spam')"},

# 'f-string': {
#     'code': """f'len("lalala")={6}{42:0}{3.1415:2f}{3.1415:"{2}f"}'""",
#     'is_expression': True,
#     'tree': typed_ast.ast3.JoinedStr([
#         typed_ast.ast3.Str('len("lalala")='),
#         typed_ast.ast3.FormattedValue(typed_ast.ast3.Num(6), -1, None),
#         typed_ast.ast3.FormattedValue(typed_ast.ast3.Num(42), -1, typed_ast.ast3.Num(0)),
#         typed_ast.ast3.FormattedValue(typed_ast.ast3.Num(3.1415), -1, typed_ast.ast3.Str('2f')),
#         typed_ast.ast3.FormattedValue(typed_ast.ast3.Num(3.1415), -1, typed_ast.ast3.JoinedStr([
#             typed_ast.ast3.Str('"'),
#             typed_ast.ast3.FormattedValue(typed_ast.ast3.Num(2), -1, None),
#             typed_ast.ast3.Str('f"')]))]),
#     'dump':
#         "JoinedStr(values=["
#         """Str(s='len("lalala")='),"""
#         "FormattedValue(value=Num(n=6),conversion=-1,format_spec=None),"
#         "FormattedValue(value=Num(n=42),conversion=-1,format_spec=Str(s='0')),"
#         "FormattedValue(value=Num(n=3.1415),conversion=-1,format_spec=Str(s='2f')),"
#         "FormattedValue(value=Num(n=3.1415),conversion=-1,format_spec=JoinedStr(values=["
#         """Str(s='"'),FormattedValue(value=Num(n=2),conversion=-1,format_spec=None),"""
#         """Str(s='f"')]))])"""}

INVALID_EXAMPLES = {
    'chained assignment with type annotation': {
        'code': "my_string: str = my_string2 = None",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
             typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
        'dump': "None"},
    'tuple unpacking assignment with one type annotation': {
        'code': "my_string, my_string2: str = my_tuple",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            [typed_ast.ast3.Tuple(
                [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
                 typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
                typed_ast.ast3.Store())],
            typed_ast.ast3.Name('my_tuple', typed_ast.ast3.Load()),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
        'dump': "None"},
    'tuple unpacking assignment with multiple type annotations': {
        'code': "my_string: str, my_string2: str = my_tuple",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            [typed_ast.ast3.Tuple(
                [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store()),
                 typed_ast.ast3.Name('my_string2', typed_ast.ast3.Store())],
                typed_ast.ast3.Store())],
            typed_ast.ast3.Name('my_tuple', typed_ast.ast3.Load()),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
        'dump': "None"},
    'assignment with type comment and annotation': {
        'code': "my_string: str = None  # type: str",
        'is_expression': False,
        'tree': typed_ast.ast3.AnnAssign(
            [typed_ast.ast3.Name('my_string', typed_ast.ast3.Store())],
            typed_ast.ast3.NameConstant(None),
            typed_ast.ast3.Name('str', typed_ast.ast3.Load()), True),
        'dump': "None"}
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

for _, _example in UNVERIFIED_EXAMPLES.items():
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
    assert _ROOT_DIRECTORY
    assert os.path.isdir(_ROOT_DIRECTORY), _ROOT_DIRECTORY

PATHS = sorted([
    os.path.join(_ROOT_DIRECTORY, n)
    for n in os.listdir(_ROOT_DIRECTORY)
    if n.endswith('.py') and not n.startswith('bad')])

# verify found paths
if __debug__:
    # On Ubuntu, Python built from source: 169 in 3.5.2, 170 in 3.6.0
    assert len(PATHS) > 150, len(PATHS)
