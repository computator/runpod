from __future__ import absolute_import, print_function, unicode_literals
import argparse
import importlib
import pkgutil
import six
import sys

class Cli(object):
    def __init__(self):
        self.cmds = {}
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(dest='target_cmd', description="Choose an action to perform")

        self._load_cmds()

    def _load_cmds(self):
        cmdpkg = importlib.import_module('..cmd', __name__)
        for finder, modname, _ in pkgutil.iter_modules(cmdpkg.__path__, cmdpkg.__name__ + '.'):
            try:
                mod = finder.find_module(modname).load_module(modname)
            except (ImportError, SyntaxError):
                continue
            self._process_cmd_module(mod)


    def _process_cmd_module(self, mod):
        if not hasattr(mod, 'get_cmd_names'):
            raise RuntimeError

        if hasattr(mod, 'init_cmd'):
            try:
                mod.init_cmd()
            except:
                raise RuntimeError
        try:
            mod_cmdnames = mod.get_cmd_names()
        except:
            raise RuntimeError
        if len(mod_cmdnames) == 0:
            return
        try:
            for cmdname in mod_cmdnames:
                if cmdname in self.cmds:
                    raise RuntimeError("Duplicate command '{}' already exists".format(cmdname))
                if not hasattr(mod, 'cmd_' + cmdname):
                    raise RuntimeError("Method 'cmd_{0}' not defined for command '{0}'".format(cmdname))
        except RuntimeError as e:
            raise RuntimeError(e)

        if hasattr(mod, 'init_cmd_subparsers'):
            try:
                mod.init_cmd_subparsers(self.subparsers.add_parser)
            except:
                six.raise_from(RuntimeError, sys.exc_info()[1])
        else:
            for cmdname in mod_cmdnames:
                self.subparsers.add_parser(cmdname)

        self.cmds.update((cmdname, (mod, getattr(mod, 'cmd_' + cmdname))) for cmdname in mod_cmdnames)

    def call(self, args=None):
        opts = self.parser.parse_args(args)
        print(opts)
        if opts.target_cmd and opts.target_cmd in self.cmds:
            self.cmds[opts.target_cmd][1](opts)