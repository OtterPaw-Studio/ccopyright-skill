# 官方来源与规则快照（中文）

最后人工核对：2026-09-01

要求可能变化，登记门户也可能需要登录或阻止自动访问。本文件不能替代申请人当前
看到的门户要求。中国版权保护中心下列办事页面未见明确的页面发布日期或更新
日期，因此只记录实际访问日期。

## 来源类型

1. 法律、条例和规章用于确定制度与材料基线；
2. 中国版权保护中心具体办事指南和 FAQ 用于解释公开操作口径；
3. 申请人本次实际核对的登录后门户文字用于动态字段和上传行为；
4. 第三方材料或推断不能单独证明官方要求。

在 `facts/requirements-snapshot.md` 中记录直达网址、实际访问/核对日期和申请人
确认。来源冲突时暂停最终生成，以当前官方页面和本次门户为准，并更新工作区配置。

[门户表单校验配置](portal-form.md)只包含结构化字段、分支和字数门禁，是实现兼容
性数据，不属于上述来源类型。

## 中国版权保护中心办事页面

以下页面均于 2026-09-01 人工访问：

| 页面 | 用途 |
|---|---|
| [软件登记指南入口](https://www.ccopyright.com.cn/index.php?optionid=1030) | 定位官方办事内容 |
| [申请须知](https://www.ccopyright.com.cn/index.php?optionid=1057) | 在线办理、自助/委托、确认页、证书与通知概览 |
| [办理步骤](https://www.ccopyright.com.cn/index.php?optionid=1079) | 公开步骤 |
| [所需文件](https://www.ccopyright.com.cn/index.php?optionid=1080) | 主要文件和条件证明类别 |
| [申请表填写说明](https://www.ccopyright.com.cn/index.php?optionid=1081) | 字段语义 |
| [审查流程](https://www.ccopyright.com.cn/index.php?optionid=1082) | 受理与审查环节 |
| [办理时限](https://www.ccopyright.com.cn/index.php?optionid=1084) | 当前页面展示的时限口径 |
| [登记办理机构](https://www.ccopyright.com.cn/index.php?optionid=1085) | 办理机构信息 |
| [常见问题第 1 页](https://www.ccopyright.com.cn/index.php?optionid=1087&page=1) | 自助/代理、登记意义和一般流程 |
| [常见问题第 2 页](https://www.ccopyright.com.cn/index.php?optionid=1087&page=2) | 名称、开发和材料问题 |
| [常见问题第 3 页](https://www.ccopyright.com.cn/index.php?optionid=1087&page=3) | 合作、委托和职务开发问题 |
| [停止收取软件著作权登记费通知](https://www.ccopyright.com.cn/index.php?optionid=1571) | 官方登记费政策依据线索；第三方服务费另行区分 |

## 维护的法规基线

- 全国人大：[《中华人民共和国著作权法》](https://www.npc.gov.cn/c2/c30834/202011/t20201119_308796.html)
- 国家行政法规库：[《计算机软件保护条例》现行整合文本（含 2011、2013 年修订）](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581)

官方[《计算机软件著作权登记办法》](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)包括以下普通流程基线：

- 申请材料包括申请表、软件鉴别材料和相关证明文件；
- 鉴别材料包括程序和文档；
- 普通方式采用前、后各连续 30 页，不足 60 页时提交全部材料；
- 除规定的特殊情形外，程序每页不少于 50 行，文档每页不少于 30 行；
- 申请文件使用 A4 纸张；
- 法规另有例外交存方式。

本生成器只覆盖普通方式。涉及例外交存、封存、涉密/军用或其他特殊处理时必须停止并转入专业流程。

## 快照确认清单

把 `confirmations.requirements.current` 设为 `true` 前，至少确认：

- 申请字段的精确名称与可选值；
- 当前普通鉴别材料的页数与行数规则；
- 接受的 PDF 格式、页面方向、大小和命名限制；
- 当前申请人类型所需的证明材料及签字/确认页；
- 多著作权人、委托/合作开发、转让、继承、外文文件或修改软件是否有额外要求；
- 本次确属普通、非涉密申请。

只查看内置校验配置时应保持 `requirements.captured_at` 为空；申请人实际打开当前
门户并完成核对后，再填写真实核对日期并确认规则当前有效。

不得在仓库工作目录中保存门户账号、会话 Cookie、身份证明扫描件或签名。
