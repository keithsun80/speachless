# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-

from .sensitive_tree import SensitiveTree


class SensitiveFilter(object):

    def __init__(self, sensitive_tree=None, excludes=[]):
        if not sensitive_tree:
            st = SensitiveTree()
            sensitive_tree = st.fetch_sensitive_tree()
        self.sensitive_tree = sensitive_tree
        self.excludes = excludes

    def fetch_node(self, node, keys_queue):
        if not keys_queue:
            return node
        key = keys_queue[0]
        child_node = node.get(key)
        return self.fetch_node(child_node, keys_queue[1:])

    def sensitive_words_count(self, txt):
        txt = self.clear_words(txt)
        match_count = 0
        keys_queue = []
        for word in txt:
            keys_queue.append(word)
            match = self.fetch_node(self.sensitive_tree, keys_queue)
            if not match:
                keys_queue = []
                continue
            if match.get("is_end"):
                keys_queue = []
                match_count += 1

        return match_count

    def find_sensitive_words(self, txt):
        txt = self.clear_words(txt)
        keys_queue = []
        for word in txt:
            keys_queue.append(word)
            match = self.fetch_node(self.sensitive_tree, keys_queue)
            if not match:
                keys_queue = []
                continue
            if match.get("is_end"):
                return True
        return False

    def replace_sensitive_words(self, txt, replace="*"):
        if not type(replace) is str or replace == "":
            raise Exception("value error: the param replace " /
                            "only support string type and not blank")

        txt = self.clear_words(txt)
        keys_queue = []
        replace_list = []
        cache_value = ""
        for word in txt:
            keys_queue.append(word)
            match = self.fetch_node(self.sensitive_tree, keys_queue)
            if not match:
                keys_queue = []
                cache_value = ""
                match_tree = self.sensitive_tree.copy()
                continue

            cache_value += word
            if match.get("is_end"):
                keys_queue = []
                replace_list.append(cache_value)
                cache_value = ""

        for sensitive_word in replace_list:
            txt = txt.replace(sensitive_word, replace*len(sensitive_word))
        return txt

    def clear_words(self, txt):
        for letter in self.excludes:
            txt = txt.replace(letter, "")
        return txt
