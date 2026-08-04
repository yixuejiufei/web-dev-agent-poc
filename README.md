# Web Dev Agent POC

> Phase 1 单角色交付 POC：一个基于 YiNengFactory 的开发 Agent，根据自然语言需求生成单文件 HTML 页面。

## 安装

```bash
uv pip install -e .
```

## 运行

```bash
yineng-factory run --config agent.yaml --input '{"requirement": "\u521b\u5efa\u4e00\u4e2a YiNengFactory \u7684\u6df1\u8272\u4e3b\u9898\u843d\u5730\u9875\uff0c\u5305\u542b\u6807\u9898\u3001\u526f\u6807\u9898\u548c CTA \u6309\u94ae"}'
```

## 输出

\u751f\u6210\u7684 HTML \u6587\u4ef6\u4f4d\u4e8e `outputs/index.html`。

## 目\u5f55\u7ed3\u6784

```
web-dev-agent-poc/
├── agent.yaml          # Agent \u914d\u7f6e
├── pyproject.toml      # \u9879\u76ee\u4f9d\u8d56
├── graphs/main.py      # LangGraph \u72b6\u6001\u673a
├── tools/file_writer.py # \u6587\u4ef6\u5199\u5165\u5de5\u5177
├── prompts/system.md  # \u5f00\u53d1\u8005\u7cfb\u7edf prompt
└── outputs/index.html # \u751f\u6210\u7684\u9875\u9762
```
