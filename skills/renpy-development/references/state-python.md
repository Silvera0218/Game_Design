# 状态、Python、存档与回滚

## 目录

- 三类状态
- 初始化和命名空间
- 存档与读档
- 回滚
- 持久化数据
- 文件与外部副作用
- 生命周期与迁移

## 三类状态

### 常量和配置

使用 `define`：

```renpy
define yuri = Character("尤莉")
define ROUTE_THRESHOLD = 5
```

初始化之后不要修改。

### 可存档、可回滚的游戏状态

使用 `default`：

```renpy
default affection = 0
default unlocked_clues = set()
```

这些值属于 store，会进入存档并参与回滚。

### 跨周目持久状态

使用 `persistent`：

```renpy
default persistent.seen_true_ending = False
default persistent.schema_version = 1
```

只存放明确需要跨存档、跨周目保留的解锁和设置。

## 初始化和命名空间

```renpy
init -10 python:
    class RouteInfo:
        def __init__(self, name, threshold):
            self.name = name
            self.threshold = threshold
```

初始化优先级决定声明顺序。普通项目应尽量使用 `define`、`default` 和无优先级 `init python`，仅在库、框架或明确依赖顺序时设置优先级。

可使用命名 store 隔离模块数据，但需保持脚本和 screen 引用一致。不要覆盖 Ren'Py 预留名或常用 store 名。

## 存档与读档

Ren'Py 会保存可回滚 store 状态、执行位置及其他运行状态。设计原则：

- 保存简单、可 pickle/序列化且版本稳定的数据。
- 不要把打开的文件、网络连接、线程、生成器、系统窗口句柄等放入游戏状态。
- 不要假设加载后会重新运行所有 Python 初始化逻辑。
- 对新增字段提供 `default` 或读取时兜底。
- 修改 label/call 结构时保留生成的 `from` 标签，降低旧存档失效风险。

存档 UI 优先使用内置 File Actions 和 File Functions，不要重新实现存档格式。

## 回滚

回滚不仅恢复画面，也恢复可回滚变量。容易破坏回滚的行为：

- 在剧情语句中写外部文件。
- 发起不可逆网络请求。
- 修改全局模块状态但未让 Ren'Py 管理。
- 在 screen 求值或预测阶段修改状态。
- 使用引擎无法追踪的自定义容器。

需要限制回滚时，先判断设计意图：

- 完全允许：默认做法。
- 固定选择：使用 `renpy.fix_rollback()` 等官方机制。
- 暂时或完全阻止：仅用于确有必要的敏感交互，避免损伤玩家体验。

不要用手写“清空历史”代替官方回滚 API。

## 持久化数据

适用场景：

- 已读结局、CG、音乐和成就。
- 全局解锁。
- 跨周目统计。
- 用户级设置。

迁移示例：

```renpy
init python:
    if persistent.schema_version is None:
        persistent.schema_version = 1

    if persistent.schema_version < 2:
        persistent.unlocked_bonus = bool(persistent.seen_true_ending)
        persistent.schema_version = 2
```

合并来自不同设备或版本的 persistent 数据时，需要为字段定义合并策略。不要保存密码、令牌或敏感个人信息。

## 文件与外部副作用

- 读取打包资源时使用 Ren'Py loader/file API。
- 用户生成内容写入 Ren'Py 认可的可写目录。
- 不使用 `C:\...`、`/Users/...` 等硬编码路径。
- 写文件、调用系统、网络请求和启动线程应放在明确的非回滚边界。
- 使用 HTTPS，并验证网络失败、离线、超时和平台限制。
- Web、移动端和沙箱平台的文件与网络能力不同。

## 生命周期与迁移

关注以下时间点：

- 初始化。
- 启动主菜单。
- 新游戏。
- 进入/离开互动。
- 保存与加载。
- 回滚。
- 重载脚本。
- 退出。

版本升级前阅读不兼容变更和 changelog。对发布中的游戏：

1. 复制真实旧存档进行升级测试。
2. 验证旧 label/call 位置。
3. 验证新增 `default` 字段。
4. 验证 persistent 迁移。
5. 验证 GUI 和配置变量变更。

对应官方文档：`python`、`namespaces`、`store_variables`、`statement_equivalents`、`save_load_rollback`、`persistent`、`file_python`、`lifecycle`、`reserved`、`incompatible`。
