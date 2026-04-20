# Changelog

## v0.1.1

- 切为彻底独立运行版
- 不再默认复用旧插件配置文件
- 不再默认复用旧插件数据目录
- 不再接管外部 qzone 插件发帖流程
- 插件配置页移除旧配置复用相关选项
- README 与 sidecar 改为独立版说明

## v0.1.0

- 新增单插件整合版 `astrbot_plugin_selfie_suite`
- 内嵌 `life_scheduler_enhanced` 的数据、生成器和固定窗口调度能力
- 内嵌 `gitee_aiimg` 的自拍参考图改图核心链路
- 内嵌 `qzone` 的发布 model / session / api 底层
- 主入口基于 `qzone_selfie_bridge` 改造，覆盖自拍说说主链、QQ 空间登录预检、失败恢复、结果通知、定时发布
