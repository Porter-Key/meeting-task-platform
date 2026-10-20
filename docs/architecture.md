# 架构说明

## 目录结构

```text
src/
├── domain/
│   └── models/
├── application/
│   ├── <业务模块>
│   └── gate/
│       ├── dependency/
│       └── function/
├── infra/
├── orchestration/
└── interface/
```

---

## 分层职责

| 目录 | 职责 |
|---|---|
| `domain/` | 存放领域模型与业务概念 |
| `domain/models/` | 存放核心模型、状态、枚举、领域规则 |
| `application/` | 存放实际业务实现模块 |
| `application/<业务模块>` | 承载具体业务逻辑 |
| `application/gate/` | application 的访问边界 |
| `application/gate/dependency/` | 定义 application 需要的依赖抽象 |
| `application/gate/function/` | 对外提供 application 业务调用入口 |
| `infra/` | 提供 dependency 所需的具体实现 |
| `orchestration/` | 调度 interface 与 gate/function 之间的业务流程 |
| `interface/` | 系统入口层，承接外部调用 |

---

## 调用关系

```text
interface
    ↓
orchestration
    ↓
application/gate/function
    ↓
application/<业务模块>
    ↓
application/gate/dependency
    ↑
infra
```

---

## 层级说明

### `domain/`

领域层。
用于放置系统中的核心业务概念。

---

### `application/`

应用层。
用于放置真正的业务实现。

`application/` 下的业务模块直接平铺，不再额外嵌套一层业务目录。

---

### `application/gate/`

应用访问边界。
用于隔离外部调度与 application 内部业务实现。

---

### `application/gate/dependency/`

依赖定义区。
用于声明 application 执行业务时需要的外部能力。

---

### `application/gate/function/`

业务入口区。
用于接收 orchestration 的调用，并进入 application 内部业务模块。

---

### `infra/`

基础设施层。
用于提供 `application/gate/dependency/` 所定义依赖的具体实现。

---

### `orchestration/`

调度层。
用于连接 `interface` 和 `application/gate/function`。

---

### `interface/`

入口层。
用于承接外部系统、框架、协议或运行环境的调用。

---

## 核心结构关系

```text
外部调用进入 interface
interface 交给 orchestration
orchestration 调用 gate/function
gate/function 调用 application 业务模块
application 业务模块通过 dependency 使用外部能力
infra 提供 dependency 的具体实现
```
