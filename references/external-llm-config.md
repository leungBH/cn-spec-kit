# 外部大模型评审配置参考 (external-llm-config)

本参考文档列出常见外部大模型的 API 配置方式，帮助用户正确填写 `.cn-spec-kit-llm.json`。

---

## 配置文件格式

项目根目录下创建 `.cn-spec-kit-llm.json`：

```json
{
  "reviewers": [
    {
      "name": "评审员名称（自定义，便于识别）",
      "url": "API基础URL（不含 /chat/completions）",
      "key": "API密钥",
      "model": "模型名称"
    }
  ]
}
```

---

## 重要：URL 规则

cn-spec-kit 在调用时会将 `url` + `/chat/completions` 拼接为完整请求地址。

**关键发现**：不同 API 代理平台的 URL 格式可能不同，请根据实际测试确定：

| 平台 | 正确的 url 格式 | 说明 |
|------|----------------|------|
| bayesdl 代理（GLM 模型） | `https://token.bayesdl.com/api/maas/v1` | 不含 `/anthropic`，直接拼接 `/chat/completions` |
| OpenAI 官方 | `https://api.openai.com/v1` | 直接拼接 `/chat/completions` |
| DeepSeek 官方 | `https://api.deepseek.com/v1` | 直接拼接 `/chat/completions` |

**如果 url 已以 `/chat/completions` 结尾**，则不再追加路径。

**建议**：配置完成后，先用 curl 测试连通性：

```bash
curl -s -X POST "<url>/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <key>" \
  -d '{"model": "<model>", "messages": [{"role": "user", "content": "连通性测试"}], "max_tokens": 50}'
```

---

## 已测试可用的配置示例

### 智谱 GLM-5.1（通过 bayesdl 代理）✅ 已验证

```json
{
  "reviewers": [
    {
      "name": "GLM-5.1评审员1",
      "url": "https://token.bayesdl.com/api/maas/v1",
      "key": "sk-897f460487844814b5f71bf02816be75",
      "model": "glm-5.1"
    }
  ]
}
```

### OpenAI GPT 系列

```json
{
  "reviewers": [
    {
      "name": "GPT-4o评审",
      "url": "https://api.openai.com/v1",
      "key": "sk-xxxxxx",
      "model": "gpt-4o"
    }
  ]
}
```

### DeepSeek 系列

```json
{
  "reviewers": [
    {
      "name": "DeepSeek评审",
      "url": "https://api.deepseek.com/v1",
      "key": "sk-xxxxxx",
      "model": "deepseek-chat"
    }
  ]
}
```

---

## 多评审员配置示例（已验证）

```json
{
  "reviewers": [
    {
      "name": "GLM-5.1评审员1",
      "url": "https://token.bayesdl.com/api/maas/v1",
      "key": "sk-897f460487844814b5f71bf02816be75",
      "model": "glm-5.1"
    },
    {
      "name": "GLM-5.1评审员2",
      "url": "https://token.bayesdl.com/api/maas/v1",
      "key": "sk-7ec4b88276ed4ed6a445c39a64c976e8",
      "model": "glm-5.1"
    }
  ]
}
```

多评审员时，每个评审员独立评审，≥50% 通过即视为通过。

---

## 安全提醒

- `.cn-spec-kit-llm.json` 包含 API 密钥，**不要提交到 Git**
- 建议在 `.gitignore` 中添加：`.cn-spec-kit-llm.json`
- API 密钥仅在评审调用时使用，不会写入任何产物文档
- 评审调用失败时不会阻塞流程（跳过外部评审继续）
- **配置前务必先测试 API 连通性**，避免因 URL 格式错误导致评审失败