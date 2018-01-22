# vim: ts=4:sw=4:sts=4:et
# -*- coding:utf-8 -*-
import json

"""
{'key': {'child_key':{'child_key1': {'is_end': true}}, 'is_end': false}, 'is_end': false}
"""


key_type = "unicode" # utf8 or unicode
output_path = "./dist/"
special_letter_list = [" ", "$", "@", "&", "^"] # basically user should clear sensitive words by themselves.

def read_file2list():
    with open("./lib/sensitive_words.txt") as f:
        return f.readlines()


def recursive_node(node, words):
    if not words:
        return {'is_end': True}
    current_key = words[0]
    if node:
        node[current_key] = recursive_node(node.get(current_key, dict()), words[1:])
        node['is_end'] = False
        return node
    return {current_key: recursive_node(dict(), words[1:]), "is_end": False}


def process_key(key):
    if key_type == "unicode":
        return key.encode("utf8")
    return key


def generate_sensitive_structure(words_list):
    root_node = dict()
    for words in words_list:
        words = clear_words(words.decode("utf8"))
        root_node = recursive_node(root_node, words)
    return root_node


def clear_words(words):
    words = words.replace("\n", "")
    for letter in special_letter_list:
        words = words.replace(letter, "")
    return words


def write2json(stringio):
    wf = open(output_path+"sensitive_words_tree.json", 'wb')
    wf.write(stringio)
    wf.close()


if __name__ == "__main__":
    words_list = read_file2list()
    words_tree = generate_sensitive_structure(words_list)
    json_words_tree = json.dumps(words_tree)
    write2json(json_words_tree)
