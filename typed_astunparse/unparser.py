"""Class: Unparser."""

import ast

import astunparse
from astunparse.unparser import interleave
import typed_ast.ast3


class Unparser(astunparse.Unparser):
    """Partial rewrite of Unparser from astunparse to handle typed_ast.ast3-based trees.

    The unparser aims at compatibility with native AST, as well as typed AST.

    Quoting grammar file[1] used by CPython, below is copy of the file for Python 3.6:

    "
    -- ASDL's 7 builtin types are:
    -- identifier, int, string, bytes, object, singleton, constant
    --
    -- singleton: None, True or False
    -- constant can be None, whereas None means "no value" for object.

    module Python
    {
        mod = Module(stmt* body)
            | Interactive(stmt* body)
            | Expression(expr body)

            -- not really an actual node but useful in Jython's typesystem.
            | Suite(stmt* body)

        stmt = FunctionDef(identifier name, arguments args,
                           stmt* body, expr* decorator_list, expr? returns)
             | AsyncFunctionDef(identifier name, arguments args,
                                stmt* body, expr* decorator_list, expr? returns)

             | ClassDef(identifier name, expr* bases, keyword* keywords,
                        stmt* body, expr* decorator_list)
             | Return(expr? value)

             | Delete(expr* targets)
             | Assign(expr* targets, expr value)
             | AugAssign(expr target, operator op, expr value)
              -- 'simple' indicates that we annotate simple name without parens
             | AnnAssign(expr target, expr annotation, expr? value, int simple)

              -- use 'orelse' because else is a keyword in target languages
             | For(expr target, expr iter, stmt* body, stmt* orelse)
             | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse)
             | While(expr test, stmt* body, stmt* orelse)
             | If(expr test, stmt* body, stmt* orelse)
             | With(withitem* items, stmt* body)
             | AsyncWith(withitem* items, stmt* body)

             | Raise(expr? exc, expr? cause)
             | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
             | Assert(expr test, expr? msg)

             | Import(alias* names)
             | ImportFrom(identifier? module, alias* names, int? level)

             | Global(identifier* names)
             | Nonlocal(identifier* names)
             | Expr(expr value)
             | Pass | Break | Continue

              -- col_offset is the byte offset in the utf8 string the parser uses
              attributes (int lineno, int col_offset)

              -- BoolOp() can use left & right?
        expr = BoolOp(boolop op, expr* values)
             | BinOp(expr left, operator op, expr right)
             | UnaryOp(unaryop op, expr operand)
             | Lambda(arguments args, expr body)
             | IfExp(expr test, expr body, expr orelse)
             | Dict(expr* keys, expr* values)
             | Set(expr* elts)
             | ListComp(expr elt, comprehension* generators)
             | SetComp(expr elt, comprehension* generators)
             | DictComp(expr key, expr value, comprehension* generators)
             | GeneratorExp(expr elt, comprehension* generators)
             -- the grammar constrains where yield expressions can occur
             | Await(expr value)
             | Yield(expr? value)
             | YieldFrom(expr value)
             -- need sequences for compare to distinguish between
             -- x < 4 < 3 and (x < 4) < 3
             | Compare(expr left, cmpop* ops, expr* comparators)
             | Call(expr func, expr* args, keyword* keywords)
             | Num(object n) -- a number as a PyObject.
             | Str(string s) -- need to specify raw, unicode, etc?
             | FormattedValue(expr value, int? conversion, expr? format_spec)
             | JoinedStr(expr* values)
             | Bytes(bytes s)
             | NameConstant(singleton value)
             | Ellipsis
             | Constant(constant value)

             -- the following expression can appear in assignment context
             | Attribute(expr value, identifier attr, expr_context ctx)
             | Subscript(expr value, slice slice, expr_context ctx)
             | Starred(expr value, expr_context ctx)
             | Name(identifier id, expr_context ctx)
             | List(expr* elts, expr_context ctx)
             | Tuple(expr* elts, expr_context ctx)

              -- col_offset is the byte offset in the utf8 string the parser uses
              attributes (int lineno, int col_offset)

        expr_context = Load | Store | Del | AugLoad | AugStore | Param

        slice = Slice(expr? lower, expr? upper, expr? step)
              | ExtSlice(slice* dims)
              | Index(expr value)

        boolop = And | Or

        operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift
                     | RShift | BitOr | BitXor | BitAnd | FloorDiv

        unaryop = Invert | Not | UAdd | USub

        cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn

        comprehension = (expr target, expr iter, expr* ifs, int is_async)

        excepthandler = ExceptHandler(expr? type, identifier? name, stmt* body)
                        attributes (int lineno, int col_offset)

        arguments = (arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults,
                     arg? kwarg, expr* defaults)

        arg = (identifier arg, expr? annotation)
               attributes (int lineno, int col_offset)

        -- keyword arguments supplied to call (NULL identifier for **kwargs)
        keyword = (identifier? arg, expr value)

        -- import name with optional 'as' alias.
        alias = (identifier name, identifier? asname)

        withitem = (expr context_expr, expr? optional_vars)
    }
    "

    Quoting the current docstring of "typed_ast/ast3.py"[2] from typed-ast repository:

    "
    The `ast3` module helps Python applications to process trees of the Python
    abstract syntax grammar.  The abstract syntax itself might change with
    each Python release; this module helps to find out programmatically what
    the current grammar looks like and allows modifications of it.  The
    difference between the `ast3` module and the builtin `ast` module is
    that `ast3` is version-independent and provides PEP 484 type comments as
    part of the AST.

    Specifically, these changes are made to the latest Python 3 AST:
    - The `FunctionDef`, `AsyncFunctionDef`, `Assign`, `For`, `AsyncFor`,
      `With`, `AsyncWith`, and `arg` classes all have a `type_comment` field
      which contains a `str` with the text of the associated type comment, if
      any.
    - `parse` has been augmented so it can parse function signature types when
      called with `mode=func_type`.
    - `parse` has an additional argument `feature_version`, which disables
      newer Python syntax features.
    - `Module` has a `type_ignores` field which contains a list of
      lines which have been `# type: ignore`d.
    - `Str` has a `kind` string field which preserves the original string
      prefix, so that `ast3.parse('u"test"').body[0].value.kind == 'u'`.

    An abstract syntax tree can be generated by using the `parse()`
    function from this module.  The result will be a tree of objects whose
    classes all inherit from `ast3.AST`.

    Additionally various helper functions are provided that make working with
    the trees simpler.  The main intention of the helper functions and this
    module in general is to provide an easy to use interface for libraries
    that work tightly with the python syntax (template engines for example).
    "

    [1]: https://hg.python.org/cpython/file/tip/Parser/Python.asdl
    [2]: https://github.com/python/typed_ast/blob/master/typed_ast/ast3.py#L5
    """

    def _write_string_or_dispatch(self, value):
        """If value is str, write it. Otherwise, dispatch it."""
        if isinstance(value, str):
            self.write(value)
        else:
            self.dispatch(value)

    def _fill_type_comment(self, type_comment):
        """Unparse type comment, adding it on the next line."""
        self.fill('# type: ')
        self._write_string_or_dispatch(type_comment)

    def _write_type_comment(self, type_comment):
        """Unparse type comment, appending it to the end of the current line."""
        self.write('  # type: ')
        self._write_string_or_dispatch(type_comment)

    def _write_raw_literal(self, text: str):
        delimiter = None
        for _ in ("'", '"', "'''", '"""'):
            if _ not in text:
                delimiter = _
                break
        if delimiter is None:
            delimiter = '"""'
        assert delimiter is not None
        if '\n' in text and delimiter in {'"', "'"}:
            delimiter = {'"': '"""', "'": "'''"}[delimiter]
        if delimiter in text:
            escaped_delimiter = ''.join(['\\{}'.format(_) for _ in delimiter])
            text = text.replace(delimiter, escaped_delimiter)
        self.write(delimiter)
        self.write(text)
        self.write(delimiter)

    def _ClassDef(self, t):
        if isinstance(t, ast.ClassDef):
            super()._ClassDef(t)
            return

        self.write("\n")
        for deco in t.decorator_list:
            self.fill("@")
            self.dispatch(deco)
        self.fill("class " + t.name)
        self.write("(")
        comma = False
        for base in t.bases:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(base)
        for keyword in t.keywords:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(keyword)
        self.write(")")
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _generic_FunctionDef(self, t, async_=False):
        """Unparse FunctionDef or AsyncFunctionDef node.

        Rather than handling:

        FunctionDef/AsyncFunctionDef(
            identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns)

        handle:

        FunctionDef/AsyncFunctionDef(
            identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns,
            string? type_comment)
        """
        if not hasattr(t, 'type_comment') or t.type_comment is None:
            super()._generic_FunctionDef(t, async_)
            return

        self.write("\n")
        for deco in t.decorator_list:
            self.fill("@")
            self.dispatch(deco)
        self.fill(("async " if async_ else "") + "def " + t.name + "(")
        self.dispatch(t.args)
        self.write(")")
        if getattr(t, "returns", False):
            self.write(" -> ")
            self.dispatch(t.returns)
        self.enter()
        self._fill_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()

    def _Assign(self, t):
        """Unparse Assign node.

        Rather than handling just:

        Assign(expr* targets, expr value)

        handle:

        Assign(expr* targets, expr value, string? type_comment)
        """
        super()._Assign(t)
        if hasattr(t, 'type_comment') and t.type_comment is not None:
            self._write_type_comment(t.type_comment)

    def _generic_For(self, t, async_=False):
        """Unparse For or AsyncFor node.

        Rather than handling just:

        For/AsyncFor(expr target, expr iter, stmt* body, stmt* orelse)

        handle:

        For/AsyncFor(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        """
        if not hasattr(t, 'type_comment') or t.type_comment is None:
            super()._generic_For(t, async_)
            return

        self.fill("async for " if async_ else "for ")
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        self.enter()
        self._write_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _If(self, t):
        self.fill("if ")
        self.dispatch(t.test)
        self.enter()
        self.dispatch(t.body)
        self.leave()
        # collapse nested ifs into equivalent elifs.
        while t.orelse and len(t.orelse) == 1 \
                and isinstance(t.orelse[0], (ast.If, typed_ast.ast3.If)):
            t = t.orelse[0]
            self.fill("elif ")
            self.dispatch(t.test)
            self.enter()
            self.dispatch(t.body)
            self.leave()
        # final else
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _generic_With(self, t, async_=False):
        """Unparse With or AsyncWith node.

        Rather than handling just:

        With/AsyncWith(withitem* items, stmt* body)

        handle:

        With/AsyncWith(withitem* items, stmt* body, string? type_comment)
        """
        if not hasattr(t, 'type_comment') or t.type_comment is None:
            super()._generic_With(t, async_)
            return

        self.fill("async with " if async_ else "with ")
        interleave(lambda: self.write(", "), self.dispatch, t.items)
        self.enter()
        self._write_type_comment(t.type_comment)
        self.dispatch(t.body)
        self.leave()

    def _Bytes(self, tree):
        if hasattr(tree, 'kind') and tree.kind:
            self.write(tree.kind)
            if 'r' in tree.kind.lower():
                self._write_raw_literal(tree.s.decode())
            else:
                self.write(repr(tree.s)[1:])
            return
        super()._Bytes(tree)

    def _Str(self, tree):
        if hasattr(tree, 'kind') and tree.kind:
            self.write(tree.kind)
            if 'r' in tree.kind.lower():
                self._write_raw_literal(tree.s)
                return
        super()._Str(tree)

    boolops = {'And': 'and', 'Or': 'or'}

    def _BoolOp(self, syntax):
        # TODO: push this to astunparse (upstream)
        self.write('(')
        op_ = ' {} '.format(self.boolops[syntax.op.__class__.__name__])
        interleave(lambda: self.write(op_), self.dispatch, syntax.values)
        self.write(')')

    def _Attribute(self, t):
        self.dispatch(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(t.value, (ast.Num, typed_ast.ast3.Num)) and isinstance(t.value.n, int):
            self.write(" ")
        self.write(".")
        self.write(t.attr)

    def _Call(self, t):
        if isinstance(t, ast.Call):
            super()._Call(t)
            return

        self.dispatch(t.func)
        self.write("(")
        comma = False
        for arg in t.args:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(arg)
        for keyword in t.keywords:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(keyword)
        self.write(")")

    def _arguments(self, t):
        first = True
        latest_comment = None
        # normal arguments
        defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
        for arg, default in zip(t.args, defaults):
            if first:
                first = False
            else:
                self.write(',')
                if latest_comment is not None:
                    self._write_type_comment(latest_comment)
                    self.fill('        ')
                    latest_comment = None
                else:
                    self.write(' ')
            self.dispatch(arg)
            if default:
                self.write("=")
                self.dispatch(default)
            latest_comment = getattr(arg, 'type_comment', None)

        # varargs, or bare '*' if no varargs but keyword-only arguments present
        if t.vararg or getattr(t, "kwonlyargs", False):
            if first:
                first = False
            else:
                self.write(',')
                if latest_comment is not None:
                    self._write_type_comment(latest_comment)
                    self.fill('        ')
                    latest_comment = None
                else:
                    self.write(' ')
            self.write("*")
            if t.vararg:
                self.write(t.vararg.arg)
                if t.vararg.annotation:
                    self.write(": ")
                    self.dispatch(t.vararg.annotation)
                latest_comment = getattr(t.vararg, 'type_comment', None)

        # keyword-only arguments
        if getattr(t, "kwonlyargs", False):
            for kwarg, default in zip(t.kwonlyargs, t.kw_defaults):
                self.write(',')
                if latest_comment is not None:
                    self._write_type_comment(latest_comment)
                    self.fill('        ')
                    latest_comment = None
                else:
                    self.write(' ')
                self.dispatch(kwarg)
                if default:
                    self.write("=")
                    self.dispatch(default)
                latest_comment = getattr(kwarg, 'type_comment', None)

        # kwargs
        if t.kwarg:
            if first:
                first = False
            else:
                self.write(',')
                if latest_comment is not None:
                    self._write_type_comment(latest_comment)
                    self.fill('        ')
                    latest_comment = None
                else:
                    self.write(' ')
            self.write("**"+t.kwarg.arg)
            if t.kwarg.annotation:
                self.write(": ")
                self.dispatch(t.kwarg.annotation)
            latest_comment = getattr(t.kwarg, 'type_comment', None)

        if latest_comment is not None:
            self._write_type_comment(latest_comment)
            self.fill('        ')
