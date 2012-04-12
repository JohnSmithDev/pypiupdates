"""
Custom Django template tags

Written by John Smith 2010-2012 | http://www.john-smith.me
Copyright Menboku Ltd 2010-2012 | http://www.menboku.co.uk
Licenced under GPL v2

"""

from django.template import Library
register = Library()

from django.template import Node, VariableDoesNotExist, \
    TemplateSyntaxError, NodeList, resolve_variable

import logging

def iflengthequal(parser, token):
    """
    Usage {% iflengthequal list 1 %}Only 1 member{% endiflengthequal %}
    Loosely derived from http://djangosnippets.org/snippets/302/
    """

    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r takes 2 arguments" % (bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfLengthEqualNode(bits[1], bits[2], nodelist_true, nodelist_false)

class IfLengthEqualNode(Node):
    def __init__(self, listarg, numarg, nodelist_true, nodelist_false):
        self.listarg = listarg
        self.numarg = numarg
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def __repr__(self):
        return "<IfLengthEqualNode>"

    def render(self, context):
        try:
            list_val = resolve_variable(self.listarg, context)
        except VariableDoesNotExist:
            list_val = self.listarg
        try:
            num_val = resolve_variable(self.numarg, context)
        except VariableDoesNotExist:
            num_val = int(self.numarg)

        # logging.debug("list_val='%s'" % (list_val))
        # logging.debug("type(list_val)=%s" % (type(list_val)))
        # logging.debug("len(list_val)=%d" % (len(list_val)))
        # logging.debug("num_val=%d" % (num_val))

        if len(list_val) == num_val:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

iflengthequal = register.tag(iflengthequal)

def resource_path(val):
    """
    Outputs the URL to access the passed BlogPostResource
    Usage (in Django template): bpr|resourcepath

    """
    if val.parent_post:
        return "/Resource/" + val.parent_post.slugified_title + \
            "/" + val.filename
    else:
        return "/Resource/Standalone/" + val.slugified_title + \
            "-" + val.filename
register.filter("resourcepath", resource_path)


def datastore_key_name(entity):
    return entity.key().id_or_name()

register.filter("datastorekeyname", datastore_key_name)

def ifpackagefamily(parser, token):
    """
    Usage {% ifpackagefamily thing %}Only 1 member{% endifpackagefamily %}
    Convenience function when iterating through the list of Packages/
    PackageFamilies
    """

    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError, "%r takes 1 argument" % (bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfPackageFamilyNode(bits[1], nodelist_true, nodelist_false)

class IfPackageFamilyNode(Node):
    def __init__(self, thingarg, nodelist_true, nodelist_false):
        self.thingarg = thingarg
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def __repr__(self):
        return "<IfPackageFamilyNode>"

    def render(self, context):
        try:
            thing_val = resolve_variable(self.thingarg, context)
        except VariableDoesNotExist:
            thing_val = self.thingarg

        # logging.debug("list_val='%s'" % (list_val))
        # logging.debug("type(list_val)=%s" % (type(list_val)))
        # logging.debug("len(list_val)=%d" % (len(list_val)))
        # logging.debug("num_val=%d" % (num_val))

        if hasattr(thing_val, "packages"):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

ifpackagefamily = register.tag(ifpackagefamily)
