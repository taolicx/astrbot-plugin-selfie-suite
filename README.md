# astrbot_plugin_selfie_suite

这是“自拍说说一体化套件”的独立版。

## 现在的定位

- 只装这一个插件即可运行自拍说说主链
- 不再运行时导入其他自拍相关插件
- 不再探测、接管、绑定外部 qzone 插件
- 不再默认复用旧插件的配置文件和数据目录

## 内置能力

- 固定窗口生活日程生成
- 自拍参考图管理
- 自拍改图链路
- QQ 空间登录预检、cookie 刷新、直发说说
- 定时自拍说说
- 结果通知
- LLM 状态注入

## 常用命令

- `查看日程`
- `重写日程`
- `日程时间 07:30`
- `自拍参考`
- `自拍参考 查看`
- `自拍参考 清空`
- `自拍`
- `自拍说说`

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

- `自拍` 和 `自拍说说` 走的是参考图改图，不是文生图
- 如果没有参考图，改图链路不会工作
- 如果没有可用的 qzone cookies，`自拍说说` 无法发布
- 这版强调的是“独立运行”，不是“兼容旧插件生态”
