# astrbot_plugin_selfie_suite

这是“日常自拍发布助手”的独立版。

## 仓库信息

- 作者：`taolicx`
- 仓库地址：[https://github.com/taolicx/astrbot-plugin-selfie-suite](https://github.com/taolicx/astrbot-plugin-selfie-suite)
- 安装地址：[https://github.com/taolicx/astrbot-plugin-selfie-suite](https://github.com/taolicx/astrbot-plugin-selfie-suite)
- 当前版本：`v0.1.8`

## 现在的定位

- 只装这一个插件即可运行自拍说说主链
- 不再运行时导入其他自拍相关插件
- 不再探测、接管、绑定外部 qzone 插件
- 不再默认复用旧插件的配置文件和数据目录
- 如果旧三件套仍然保留安装，这版默认使用这一套新命令并抑制重复状态注入，尽量减少冲突

## 内置能力

- 固定窗口生活日程生成
- 6 段细化日程和分时段穿搭
- 自拍参考图管理
- 自拍改图链路
- QQ 空间登录预检、cookie 刷新、直发说说
- 定时自拍说说
- 结果通知
- LLM 状态注入
- 自拍动作/镜头/表情/道具变体池，降低重复感

## 常用命令

- `日常状态`
- `刷新日常状态`
- `日常刷新时间 07:30`
- `自拍参考图`
- `自拍参考图 查看`
- `自拍参考图 清空`
- `生成自拍`
- `发布自拍说说`

## 配置方式

本插件默认只读自己的配置文件：

- `astrbot_plugin_selfie_suite_life_config.json`
- `astrbot_plugin_selfie_suite_qzone_config.json`
- `astrbot_plugin_selfie_suite_aiimg_config.json`

也可以直接在插件配置页里填写：

- `embedded_life_config_json`
- `embedded_qzone_config_json`
- `embedded_aiimg_config_json`

填写后会写入本插件自己的配置文件，不依赖旧插件。

文案相关补充配置：

- `publish_caption_enabled`
  - 控制 `发布自拍说说` 时是否把生成文案一并发到 QQ 空间
  - 关闭后只发图片，不带说说文字
- `caption_prompt_template`
  - 控制自拍说说文案的生成风格
- `fallback_caption_template`
  - 当文案模型不可用或输出异常时，本地兜底会基于这个模板生成更自然的短句

改图接口相关补充配置：

- `aiimg_provider_type`
  - 直接选择改图接口类型，常用 OpenAI 兼容接口建议选 `openai_chat` 或 `openai_images`
- `aiimg_base_url`
  - 直接填改图接口地址
- `aiimg_api_keys`
  - 直接填 API Key，支持一行一个或用逗号分隔多个 key
- `aiimg_model`
  - 直接填模型名
- `aiimg_timeout`
  - 改图超时秒数
- `aiimg_default_output`
  - 可选输出尺寸，例如 `1024x1024`

如果上面这些常用字段不够，再用：

- `embedded_aiimg_config_json`
  - 适合高级链路、多个 provider、特殊字段

## 安装方式

在 AstrBot 插件安装页直接填写：

- `https://github.com/taolicx/astrbot-plugin-selfie-suite`

安装完成后，优先使用这一套新命令，不要和旧版同类插件命令混用。

## 注意

- `生成自拍` 和 `发布自拍说说` 走的是参考图改图，不是文生图
- 如果没有参考图，改图链路不会工作
- 如果没有可用的 qzone cookies，`发布自拍说说` 无法发布
- 如果和旧版 `life_scheduler / gitee_aiimg / qzone / qzone_selfie_bridge` 共存，优先使用这里这一套新命令，不要再混用旧命令
- 这版强调的是“独立运行 + 尽量共存避冲突”，不是继续绑定旧插件生态
