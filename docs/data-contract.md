# 资料交换约定

资料为 UTF-8 JSON，根对象包含 name、tables 和 options。tables 的每张表都必须出现，允许空表；记录中的约定字段必须存在，显式 null 保留来源未知的含义，不能与字段缺失混淆。额外字段及 options 可承载研究方案。金额和时间的具体口径如下。

| 表 | 字段 |
| --- | --- |
| roster | person, facility, district, share, planned_hours, actual_hours |
| certificates | person, skill, start, end |
| training | person, course, start, end, passed, retained_at |
| tasks | district, month, task, hours, combinations |
| commitments | facility, month, task, hours |

资质和培训时间均为左闭右开本地日期区间，end=null 表示尚未结束。share 为合同全职比例，planned_hours/actual_hours 为月工时；actual_hours=null 表示尚未报送。combinations 为可互相替代的协作组合，每个内层列表为同时在场的不同人员所需技能，hours 是服务时长，每位成员均占相同时长。

roster 可附加 month 指定月度记录，未给时 options.roster_month 为整表月份。training 可附加 course_skill 表明成功后新增技能；passed=null 为结果未知，retained_at 为留任观测的日期而非永久在岗标志。历史留任可附加 departed_at 及 observation_end 表达右删失；无此证据时限制对长期留任的判断。

analysis_core/workforce.py 中的公开函数用于原始核对。active_certificates 保留当前参数及返回语义。原始资料查询不代表已经完成统计识别或政策判断。examples/study.json 是可读的合成资料，数值不表示真实地区或人群。

Archive 用 name 和完整内容摘要区分原始资料修订。相同内容重复存入不会增加修订，不同内容不会覆盖旧资料；read 以精确摘要读取。Study.tables 和 Study.options 每次返回独立副本。group_rows 用属性是否存在与属性值共同分组；numeric_summary 分别报告条数、有效数值及空值。已有资料结构、原始查询及归档读取继续对外可用。
