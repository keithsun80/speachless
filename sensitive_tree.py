# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-
import os
import json
import pkg_resources

resource_package = __name__


class SensitiveTree(object):
    """
    {'key': {'child_key':{'child_key1': {'is_end': true}},
                          'is_end': false}, 'is_end': false}
    """

    def __init__(self, tree_types=['pron', 'political', 'custom'],
                 excludes=[" ", "$", "@", "&", "^", "\r", "\n"]):
        self.excludes = excludes
        self.tree_types = tree_types

    def fetch_sensitive_lines(self):
        sensitive_lines = []
        if "pron" in self.tree_types:
            from .lib import porn_arr
            sensitive_lines.extend(porn_arr)
        if "political" in self.tree_types:
            from .lib import political_arr
            sensitive_lines.extend(political_arr)
        if "custom" in self.tree_types:
            from .lib import custom_arr
            sensitive_lines.extend(custom_arr)

        return sensitive_lines

    def generate_sensitive_structure(self, sensitive_lines):
        root_node = dict()
        for words in sensitive_lines:
            words = self.clear_words(words)
            root_node = self.recursive_node(root_node, words)
        return root_node

    def recursive_node(self, node, words):
        if not words:
            return {'is_end': True}
        current_key = words[0]
        if node:
            node[current_key] = self.recursive_node(node.get(current_key,
                                                    dict()), words[1:])
            if not node.get('is_end'):
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
        wf.write(json.dumps(words_tree).encode("utf-8"))
        wf.close()


if __name__ == "__main__":
    st = SensitiveTree()
    st.write2json_file("./speachless/dist/")
