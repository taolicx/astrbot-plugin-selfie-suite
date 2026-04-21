# astrbot_plugin_selfie_suite

这是“日常自拍发布助手”的独立版。

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

## 注意

- `生成自拍` 和 `发布自拍说说` 走的是参考图改图，不是文生图
- 如果没有参考图，改图链路不会工作
- 如果没有可用的 qzone cookies，`发布自拍说说` 无法发布
- 如果和旧版 `life_scheduler / gitee_aiimg / qzone / qzone_selfie_bridge` 共存，优先使用这里这一套新命令，不要再混用旧命令
- 这版强调的是“独立运行 + 尽量共存避冲突”，不是继续绑定旧插件生态
