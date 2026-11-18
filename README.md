# 护理培训如何改变真实服务能力

本项目用于研究原始资料的核对、留存与查询，数据含义见 docs/data-contract.md。analysis_core/records.py 读取和校验资料形状，archive.py 保存独立修订，workforce.py 提供领域原始查询。研究方案可使用 options 保留独立设置。

运行环境为 Python 3.11 及以上。当前运行和测试仅依赖标准库，无需联网或连接外部系统。合成资料不含真实个人信息，不用于临床决定。

在项目根目录运行已有资料核对入口：

```sh
python -m analysis_core examples/study.json
```

可选 --archive 指定本地 SQLite 路径，原始内容按摘要归档。输出包含资料摘要、每张表的记录数量和已有领域查询结果。

运行现有契约测试及语法构建检查：

```sh
python -m unittest discover -v
python -m compileall -q analysis_core tests
```

无需安装即可从源码运行。需要发行包时，构建工具版本固定在 pyproject.toml；运行库不依赖该工具。
