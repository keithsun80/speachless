
# 敏感词过滤 python3
```
  测试过滤效果
  python -m speachless.test

  输出json文件 至 dist
  python -m speachless.sensitive_tree
```

## 简介
* speachless/lib 敏感词库, 三个种类，涉政, 色情, 自定义.
* speachless/sensitive_tree.SensitiveTree 根据词库中的敏感词构造检测tree
* speachless/sensitive_filter.SensitiveFilter 检测输入内容是否与敏感词匹配


## 使用


git archive master | tar -x -C /project/xxx/speachless



** 应该将以下对象 作为全局变量避免每次重新初始化 tree 造成额外开销 **

```
sensitive_tree = SensitiveTree().fetch_sensitive_tree()

sf = SensitiveFilter(sensitive_tree=sensitive_tree,
                                   excludes=["&", "*", "$", " "])


check_value = "h&图, dsfdf援交"
sf.sensitive_words_count(check_value)
sf.find_sensitive_words(check_value)
sf.replace_sensitive_words(check_value)
sf.replace_sensitive_words("我没有任何问题")
```

# to do

```
  相似性匹配, 譬如haha图, 设定跨度值为1, 可以match h'*'图
  跨度值合理范围？
```
