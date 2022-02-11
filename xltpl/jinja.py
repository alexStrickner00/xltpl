import sys

import six
from jinja2 import Environment, nodes
from jinja2.exceptions import TemplateSyntaxError
from jinja2.ext import Extension
from jinja2.parser import Parser

from .xlext import NodeExtension, SegmentExtension, XvExtension, ImageExtension, ImagexExtension
from .ynext import YnExtension, YnxExtension


class Env(Environment):

    def handle_exception(self, *args, **kwargs):
        exc_type, exc_value, tb = sys.exc_info()
        red_fmt = '\033[31m%s\033[0m'
        blue_fmt = '\033[34m%s\033[0m'
        error_type = red_fmt % ('error type:  %s' % exc_type)
        error_message = red_fmt % ('error message:  %s' % exc_value)
        print(error_type)
        print(error_message)
        if exc_type is TemplateSyntaxError:
            lineno = exc_value.lineno
            source = kwargs['source']
            src_lines = source.splitlines()
            for i, line in enumerate(src_lines):
                if i + 1 == lineno:
                    line_str = red_fmt % ('line %d : %s' % (i + 1, line))
                elif i + 1 in [lineno - 1, lineno + 1]:
                    line_str = blue_fmt % ('line %d : %s' % (i + 1, line))
                else:
                    line_str = 'line %d : %s' % (i + 1, line)
                print(line_str)
        Environment.handle_exception(self, *args, **kwargs)

    def set_node_map(self, node_map):
        self.node_map = node_map


class JinjaEnv(Env):

    def __init__(self, node_map, user_extensions=[]):
        exts = [NodeExtension, SegmentExtension, YnExtension, XvExtension, ImageExtension]
        exts.extend(user_extensions)
        Env.__init__(self, extensions=exts)
        self.node_map = node_map


class JinjaEnvx(Env):

    def __init__(self, node_map, user_extensions=[]):
        exts = [NodeExtension, SegmentExtension, YnxExtension, XvExtension, ImagexExtension]
        exts.extend(user_extensions)
        Env.__init__(self, extensions=exts)
        self.node_map = node_map


class XlExtension(Extension):
    arg_names = []

    def parse(self, parser: Parser):
        lineno = next(parser.stream).lineno
        args = []
        try:
            while True:
                arg: nodes.Expr = parser.parse_expression()
                if arg is None:
                    break
                args.append(arg)
                parser.stream.skip_if('comma')
        finally:
            return nodes.CallBlock(self.call_method('_handle_callback', args), [], [], []).set_lineno(
                lineno)

    def get_value(self, **kwargs):
        pass

    def _get_kwargs(self, args):
        arg_map = {}
        for i in range(0, min(len(args), len(self.arg_names))):
            arg_name = self.arg_names[i]
            arg_map[arg_name] = args[i]
        return arg_map

    def get_type(self, args, kwargs, val=None):
        if val is None:
            val = self.get_value(**kwargs)
        return six.text_type(val)

    def _handle_callback(self, *args, caller=None):
        kwargs = self._get_kwargs(args)
        key = args[-1]
        val = self.get_value(**kwargs)
        if key != 1:
            node = self.environment.node_map.get_node(key)
            node.rv = val
        return self.get_type(args, kwargs, val=val)
