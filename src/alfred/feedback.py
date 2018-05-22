# -*- coding: utf-8 -*-
from xml.etree import ElementTree
import xml.sax.saxutils as saxutils
import os, copy, random
import json

import core

class Item(object):
    def __init__(self, **kwargs):
        self.content = {
            'title'     : kwargs.get('title', ''),
            'subtitle'  : kwargs.get('subtitle', ''),
            'icon'      : kwargs.get('icon', 'icon.png')
        }

        it = kwargs.get('icontype', '').lower()
        self.icon_type = it if it in ['fileicon', 'filetype'] else None

        valid = kwargs.get('valid', None)
        if isinstance(valid, (str, unicode)) and valid.lower() == 'no':
            valid = 'no'
        elif isinstance(valid, bool) and not valid:
            valid = 'no'
        else:
            valid = None

        self.attrb = {
            'uid'           : kwargs.get('uid', '{0}.{1}'.format(core.bundleID(), random.getrandbits(40))),
            'arg'           : kwargs.get('arg', None),
            'valid'         : valid,
            'autocomplete'  : kwargs.get('autocomplete', None),
            'type'          : kwargs.get('type', None)
        }

        for key in self.content.keys():
            if self.content[key] is None:
                del self.content[key]

        for key in self.attrb.keys():
            if self.attrb[key] is None:
                del self.attrb[key]

    def copy(self):
        return copy.copy(self)

    def getXMLElement(self):
        item = self.attrb
        for (k, v) in self.content.iteritems():
            item[k] = v
        return item

class Feedback(object):
    def __init__(self):
        self.items = []
        self.variables = []

    def addItem(self, **kwargs):
        item = kwargs.pop('item', None)
        if not isinstance(item, Item):
            item = Item(**kwargs)
        self.items.append(item)

    def addVariable(self, name, value):
        self.variables.append((name, value))

    def clean(self):
        self.items = []

    def isEmpty(self):
        return not bool(self.items)

    def get(self, unescape = False):
        ele_tree = {}
        ele_items = []
        for item in self.items:
            ele_item = item.getXMLElement()
            ele_items.append(ele_item)
        ele_tree['items'] = ele_items
        if len(self.variables) > 0:
            ele_variables = {}
            for variable in self.variables:
                ele_variables[variable[0]] = variable[1]
            ele_tree['variables'] = ele_variables
        # res = ElementTree.tostring(ele_tree, encoding='utf-8')
        res = json.dumps(ele_tree)
        if unescape:
            return saxutils.unescape(res)
        return res

    def output(self):
        print(self.get())