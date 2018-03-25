# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-

from sensitive_tree import SensitiveTree


class SensitiveFilter(object):

    def __init__(self, sensitive_tree=None, excludes=[]):
        if not sensitive_tree:
            st = SensitiveTree()
            sensitive_tree = st.fetch_sensitive_tree()
        self.sensitive_tree = sensitive_tree
        self.excludes = excludes

    def sensitive_words_count(self, txt):
        txt = self.clear_words(txt)
        match_tree = self.sensitive_tree.copy()
        match_count = 0
        for word in txt:
            match = match_tree.get(word)
            if not match:
                match_tree = self.sensitive_tree.copy()
                continue
            if match.get("is_end"):
                match_count += 1
                match_tree = self.sensitive_tree.copy()
            else:
                match_tree = match
        return match_count

    def find_sensitive_words(self, txt):
        txt = self.clear_words(txt)
        match_tree = self.sensitive_tree.copy()
        for word in txt:
            match = match_tree.get(word)
            if not match:
                match_tree = self.sensitive_tree.copy()
                continue
            if match.get("is_end"):
                return True
            else:
                match_tree = match
        return False

    def replace_sensitive_words(self, txt, replace="*"):
        if not type(replace) is str or replace == "":
            raise Exception("value error: the param replace " /
                            "only support string type and not blank")

        txt = self.clear_words(txt)
        match_tree = self.sensitive_tree.copy()
        replace_list = []
        cache_value = ""
        for word in txt:
            match = match_tree.get(word)
            if not match:
                cache_value = ""
                match_tree = self.sensitive_tree.copy()
                continue

            cache_value += word
            if match.get("is_end"):
                match_tree = self.sensitive_tree.copy()
                replace_list.append(cache_value)
                cache_value = ""
            else:
                match_tree = match

        for sensitive_word in replace_list:
            txt = txt.replace(sensitive_word, replace*len(sensitive_word))
        return txt

    def clear_words(self, txt):
        for letter in self.excludes:
            txt = txt.replace(letter, "")
        return txt


if __name__ == "__main__":
    check_value = "h&图, dsfdf援交"
    sf = SensitiveFilter(excludes=["&"])
    print(sf.sensitive_words_count(check_value))
    print(sf.find_sensitive_words(check_value))
    print(sf.replace_sensitive_words(check_value))
