#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2017, Data61
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# ABN 41 687 119 230.
#
# This software may be distributed and modified according to the terms of
# the BSD 2-Clause license. Note that NO WARRANTY is provided.
# See "LICENSE_BSD2.txt" for details.
#
# @TAG(DATA61_BSD)
#

'''Brief wrapper around the jinja2 templating engine.'''

from __future__ import absolute_import, division, print_function, \
    unicode_literals
from camkes.internal.seven import cmp, filter, map, zip

from .Context import new_context
from camkes.internal.mkdirp import mkdirp
from camkes.internal.version import version
from camkes.templates import TemplateError, TEMPLATES

import jinja2, os, platform, six, sys

# Jinja is setup by default for HTML templating. We tweak the delimiters to
# make it more suitable for C.
START_BLOCK = '/*-'
END_BLOCK = '-*/'
START_VARIABLE = '/*?'
END_VARIABLE = '?*/'
START_COMMENT = '/*#'
END_COMMENT = '#*/'

def get_leaves(d):
    '''Generator that yields the leaves of a hierarchical dictionary. See usage
    below.'''
    assert isinstance(d, dict)
    for v in d.values():
        if isinstance(v, dict):
            # We're at an intermediate node. Yield all leaves below it.
            for x in get_leaves(v):
                yield x
        else:
            # We're at a leaf node.
            yield v

class Renderer(object):
    def __init__(self, templates):
        # This function constructs a Jinja environment for our templates.

        self.templates = templates

        loaders = []

        # Source templates.
        loaders.extend(jinja2.FileSystemLoader(os.path.abspath(x)) for x in
            templates.get_roots())

        self.env = jinja2.Environment(
            loader=jinja2.ChoiceLoader(loaders),
            extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
            block_start_string=START_BLOCK,
            block_end_string=END_BLOCK,
            variable_start_string=START_VARIABLE,
            variable_end_string=END_VARIABLE,
            comment_start_string=START_COMMENT,
            comment_end_string=END_COMMENT,
            auto_reload=False,
            undefined=jinja2.StrictUndefined)

    def render(self, me, assembly, template, render_state, state_key, outfile_name,
            **kwargs):
        context = new_context(me, assembly, render_state, state_key, outfile_name,
            self.templates, **kwargs)

        t = self.env.get_template(template)
        try:
            return t.render(context)
        except TemplateError:
            raise
        except Exception as e:
            # Catch and re-cast any other exceptions to allow the runner to
            # handle them as usual and prevent us barfing stack traces when
            # exceptions aren't our fault.
            six.reraise(TemplateError, TemplateError('unhandled exception in '
                'template %s: %s' % (template, e)), sys.exc_info()[2])
