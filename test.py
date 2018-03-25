# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-

from .sensitive_filter import SensitiveFilter

if __name__ == "__main__":
    check_value = "h&图, dsfdf援交"
    sf = SensitiveFilter(excludes=["&"])
    print(sf.sensitive_words_count(check_value))
    print(sf.find_sensitive_words(check_value))
    print(sf.replace_sensitive_words(check_value))
    print(sf.replace_sensitive_words("我没有任何问题"))
