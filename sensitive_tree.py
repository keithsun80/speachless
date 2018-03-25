# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-
import os
import json
import pkg_resources

resource_package = __name__

porn_resource_path = pkg_resources.resource_filename(__name__, '/'.join(('lib', 'sensitive_porn.txt')))
political_resource_path = pkg_resources.resource_filename(__name__, '/'.join(('lib', 'sensitive_political.txt')))
custom_resource_path = pkg_resources.resource_filename(__name__, '/'.join(('lib', 'sensitive_custom.txt')))


class SensitiveTree(object):
    """
    {'key': {'child_key':{'child_key1': {'is_end': true}},
                          'is_end': false}, 'is_end': false}
    """

    def __init__(self, tree_types=['pron', 'political', 'custom'],
                 excludes=[" ", "$", "@", "&", "^", "\r", "\n"],
                 key2unicode=False):
        self.excludes = excludes
        self.tree_types = tree_types
        self.key2unicode = key2unicode

    def fetch_sensitive_lines(self):
        sensitive_lines = []
        if "pron" in self.tree_types:
            with open(porn_resource_path, 'r', errors='ignore') as f:
                sensitive_lines.extend(f.readlines())
        if "political" in self.tree_types:
            with open(political_resource_path, 'r', errors='ignore') as f:
                sensitive_lines.extend(f.readlines())
        if "custom" in self.tree_types:
            with open(custom_resource_path, 'r', errors='ignore') as f:
                sensitive_lines.extend(f.readlines())

        return sensitive_lines

    def generate_sensitive_structure(self, sensitive_lines):
        root_node = dict()
        for words in sensitive_lines:
            words = self.clear_words(words)
            if self.key2unicode:
                words = words.decode("utf-8")
            root_node = self.recursive_node(root_node, words)
        return root_node

    def recursive_node(self, node, words):
        if not words:
            return {'is_end': True}
        current_key = words[0]
        if node:
            node[current_key] = self.recursive_node(node.get(current_key,
                                                    dict()), words[1:])
            node['is_end'] = False
            return node
        return {current_key: self.recursive_node(dict(), words[1:]),
                "is_end": False}

    def clear_words(self, words):
        for letter in self.excludes:
            words = words.replace(letter, "")
        return words

    def fetch_sensitive_tree(self):
        sensitive_lines = self.fetch_sensitive_lines()
        return self.generate_sensitive_structure(sensitive_lines)

    def write2json_file(self, output_path):
        words_tree = self.fetch_sensitive_tree()
        wf = open(output_path+"sensitive_words_tree.json", 'wb')
        json.dump(words_tree, wf)
        wf.close()


if __name__ == "__main__":
    st = SensitiveTree(key2unicode=True)
    st.write2json_file("./dist/")
