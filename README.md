# Web Dev Agent POC

> Phase 1 单角色交付 POC：一个基于 YiNengFactory 的开发 Agent，根据自然语言需求生成单文件 HTML 页面。

## 版本

当前版本：**v0.1.2**

## 安装

```bash
uv pip install -e .
```

开发依赖：

```bash
uv pip install -e '.[dev]'
```

## 运行

```bash
yineng-factory run --config agent.yaml \
  --input '{"requirement": "创建一个 YiNengFactory 的深色主题落地页，包含标题、副标题和 CTA 按钮"}'
```

## 测试

```bash
pytest tests/ -v
```

6 个测试覆盖：

- `test_agent_yaml_is_valid`：agent.yaml schema 校验
- `test_graph_loadable`：LangGraph 编译与加载
- `test_file_writer_tool`：文件写入工具
- `test_system_prompt_exists`：prompt 文件完整性
- `test_dev_agent_end_to_end`：完整 LLM 调用链路（需设置 `AGENT_LITELLM_MASTER_KEY`）
- `test_agent_config_reads_agent_prefixed_env`：`AGENT_` 前缀环境变量读取

## 输出

生成的 HTML 文件位于 `outputs/index.html`。

## 目录结构

```
web-dev-agent-poc/
├── agent.yaml              # Agent 配置
├── pyproject.toml          # 项目依赖
├── graphs/main.py          # LangGraph 状态机
├── tools/file_writer.py    # 文件写入工具
├── prompts/system.md       # 开发者系统 prompt
├── tests/                  # pytest 测试套件
└── outputs/index.html      # 生成的页面（不提交）
```

## 配置注意

项目 `.env` 必须使用 `AGENT_` 前缀：

```bash
AGENT_LITELLM_MASTER_KEY=sk-...
AGENT_LITELLM_BASE_URL=http://localhost:4000
```
