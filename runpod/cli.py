from __future__ import absolute_import, print_function, unicode_literals
import argparse
import importlib
import os.path
import pkgutil
import six
import sys

class Cli(object):
    def __init__(self):
        self.cmds = {}

        self.parser = argparse.ArgumentParser()
        self._init_parser()
        self.subparsers = self.parser.add_subparsers(dest='target_cmd', description="Choose an action to perform")

        self._load_cmds()

    def _init_parser(self):
        def dir_validator(directory):
            if directory:
                out_dir = os.path.abspath(directory)
                if os.path.isdir(out_dir):
                    return out_dir
            raise argparse.ArgumentTypeError("'{}' is not a valid directory".format(directory))

        self.parser.add_argument("-f", "--file", type=argparse.FileType(), default="runpod.yaml", help="Specify the pod source file")
        self.parser.add_argument("-p", "--project-name", metavar="NAME", help="Specify the project name")
        self.parser.add_argument("--project-directory", type=dir_validator, metavar="PATH", help="Specify the working directory for the project")

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
        self._process_args(args)
        self.cmds[self.opts.target_cmd][1](self.opts)

    def _process_args(self, args=None):
        self.opts = self.parser.parse_args(args)

        if self.opts.project_directory is None:
            if os.path.isfile(self.opts.file.name):
                self.opts.project_directory = os.path.dirname(os.path.abspath(self.opts.file.name))
            else:
                self.opts.project_directory = os.getcwd()
        if self.opts.project_name is None:
            self.opts.project_name = os.path.basename(self.opts.project_directory)
        elif not self.opts.project_name:
            self.parser.error("project name is required")

        if not self.opts.target_cmd:
            self.parser.error("subcommand is required")
        elif self.opts.target_cmd not in self.cmds:
            self.parser.error("'{}' is not a valid subcommand".format(self.opts.target_cmd))