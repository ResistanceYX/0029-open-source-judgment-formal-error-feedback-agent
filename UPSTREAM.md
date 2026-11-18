# UPSTREAM.md —— 上游参考与许可核对记录

> 本项目（#0029 节点开源实现）**全部代码为重新实现，未复制任何上游仓库代码**。
> 本文件记录思想来源、核对过的上游 commit 与许可状态，以满足"复制必登记"的纪律；
> 由于采取零复制策略，没有需要标注版权行的复制文件。

## 核查日期与基线

- 核查日期：2026-11-18
- 复测基线：2026-11-16 快照 + 2026-11-17 澄樾本地复测（见下）

## 三个上游仓库（同一作者 lcfactorization）

| 仓库 | 默认分支 | 核查时 HEAD commit | LICENSE 文件 | 结论 |
|---|---|---|---|---|
| judicial-doc-anomaly-mcp | main | 98905fe63c50e5346351330321688081c1301120（2026-06-27） | 有，MIT，Copyright (c) 2026 Justice-and-Equity | 只借鉴思想，不复制代码 |
| legal-hallucination-mcp | master | 3780004da584bdb4232853195f5dfe1b24a1f38e（2026-06-27） | **无**（pyproject 元数据声明 MIT，但无许可证文本文件） | **法律上默认保留所有权利，代码不可复制**；只借鉴思想 |
| judicial-doc-quality-mcp | master | 7b436e4dd0a952b9de712f032ca80bcbf9f327d3（2026-06-27） | 有，MIT，Copyright (c) 2026 Justice and Equity | 只借鉴思想，不复制代码 |

## 2026-11-17 本地复测记录（澄樾）

三仓库默认分支项目自带 tests 本地运行：异常检测 169 项通过；质量评估 162 项通过；
幻觉检测 30 项通过、1 项报告格式测试失败。该结果只作部分工程行为核验，
不是独立真实文书检出率、司法效果或安全审计。

## 云端 CI 与活动状态（2026-11-18 核查）

- anomaly-mcp：默认分支 HEAD 的 Tests 在 6 个 OS/Python 环境全部 failure；2026-10-26 的
  PR #1（claim-support D17 + red-flag escalation）云端 CI 失败，与作者自述"194 测试全绿"矛盾，
  以云端为准；PR 未合并。
- hallucination-mcp：默认分支 HEAD 的 lint-and-test（3.11）failure、（3.12）cancelled；
  PR #1（H-7/H-8 dimensions + red-flag critical floor）未合并。
- quality-mcp：全仓库仅 1 次 Actions 运行（dependabot 依赖图更新），无任何测试 CI；
  PR #1（claim_support 8th dimension + red-flag veto）未合并。
- 三个仓库最后一次活动均为 2026-10-26（开 PR），此后近一个月无更新。

## 借鉴的思想零件（非代码）

| 思想来源 | 借鉴内容 | 本项目实现位置 |
|---|---|---|
| judicial-doc-anomaly-mcp | Skills 文件化、分阶段 pipeline、结构化报告、token 估算的思路 | 规则包分层（parser/rules/report/review/feedback）、报告 Schema 版本化 |
| legal-hallucination-mcp | 正则与数值确定性检查、证据清单→合法输入登记的思路 | parser/* 全部确定性解析、input_registry |
| judicial-doc-quality-mcp | 文书分段、时间线与前后一致性对照的思路 | parser/segment.py、规则 DATE-03/NUM-01 |

## 明确放弃的上游内容

- 三个仓库的全部代码与测试（许可或 CI 状态不支持直接复制）
- 三个 2026-10-26 未合并 PR 的能力（claim_support、red-flag 等实质性异常判断，超出本项目"形式异常线索"边界）
- 加密案例 PDF、cases/、vault_mirror/ 等素材（密码另行告知的受控材料，一律不进入本项目）
- anomaly 的 write_skill 写功能（上游 PR 自述存在路径穿越加固需求，本项目不实现写功能，规避该风险）
