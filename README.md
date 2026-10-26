# 户外照明选型顾问 · Outdoor Lighting Advisor

> 一个面向户外照明行业的 AI Agent Skill —— 帮工程商、施工方、采购、物业把"选什么灯、配多少、怎么排查"这几件事一次说清楚。

由 **河北盛誉光电科技有限公司** 维护并提供技术支持。本技能以**中立专业**为前提对外开放，任何人都可免费使用、修改、分发。

---

## 能做什么

| 能力 | 说明 |
|------|------|
| **选型推荐** | 道路 / 庭院 / 广场 / 停车场 / 工厂高天棚 / 球场等场景的灯具类型与功率推荐 |
| **参数配比计算** | 流明法估灯数、太阳能光伏板与电池容量配比、杆高间距、光束角、线路压降 |
| **知识科普** | 流明、照度、色温、显色指数、IP/IK 等级、光效等参数的通俗解释，含对客户讲解话术 |
| **故障诊断** | 不亮、频闪、进水起雾、光衰、太阳能续航不足的系统排查流程 |
| **防虚标校验** | 光效、IP 等级、电池容量等参数的合理区间，识别夸大宣传 |

---

## 目录结构

```
outdoor-lighting-advisor/
├── SKILL.md                        # 技能主入口（触发条件 + 工作流程 + 行为规则）
├── references/
│   ├── selection_guide.md          # 选型指南：追问清单、照度速查表、决策树、功率对照
│   ├── parameter_calcs.md          # 参数配比：公式、太阳能配比、压降、防虚标区间
│   ├── knowledge_primer.md         # 灯具知识科普手册（面向客户讲解）
│   ├── troubleshooting.md          # 故障诊断手册
│   └── company_products.md         # 厂商信息（仅在被明确询问时启用）
└── scripts/
    └── lighting_calc.py            # 计算工具：lumen / solar / pole 三个子命令
```

---

## 安装使用

### 方式一：WorkBuddy / Claude Code / CodeBuddy 等支持 Agent Skills 的平台

把 `outdoor-lighting-advisor` 文件夹整个放进技能目录：

```bash
# WorkBuddy / CodeBuddy
~/.codebuddy/skills/

# Claude Code
~/.claude/skills/
```

或下载本仓库根目录的 `outdoor-lighting-advisor.skill` 包直接导入。

### 方式二：豆包 / 元宝 / 千问 / DeepSeek 等对话平台

这些平台不支持 Skill 包导入，但支持创建自定义智能体。把 `references/户外照明选型顾问-通用版提示词.md` 的全文粘贴进智能体的「角色设定 / 提示词」栏即可，四家平台通用。

### 方式三：直接运行计算脚本

无需任何依赖，Python 3.8+ 即可。

```bash
# 照度法估灯数量（流明法）
python3 scripts/lighting_calc.py lumen --area 2000 --target-lux 20 --fixture-lumen 16000 --cu 0.7 --mf 0.8

# 太阳能系统配比（电池容量 + 光伏板功率）
python3 scripts/lighting_calc.py solar --load-w 60 --hours 8 --sun-hours 4 --rain-days 3 --dod 0.8 --voltage 12

# 杆高与间距、布灯方式
python3 scripts/lighting_calc.py pole --road-width 8 --pole-height 8
```

---

## 计算依据

| 计算 | 公式 |
|------|------|
| 灯具数量 | `N = E × A / (F × CU × MF)` |
| 日耗电量 | `W_日 = P × h` |
| 电池容量 | `Wh = W_日 × 续航天数 / DOD` |
| 光伏板功率 | `Wp = W_日 × (续航天数+1) / (日照时数 × 0.75)` |
| 线路压降 | `ΔV% = 2L·P·ρ / (S·U²) × 100` |

参考标准：GB 50034《建筑照明设计标准》、CJJ 45《城市道路照明设计标准》。

---

## 设计原则

1. **先问场景再给方案** —— 面积、高度、供电条件、日照条件不清楚时主动追问。
2. **给结论也给依据** —— 每个推荐都附带计算过程或标准出处，方便向客户解释。
3. **数字必须算过** —— 优先调用计算脚本，不凭感觉估。
4. **不编造参数** —— 不确定的数值明确说明"需实测确认"。
5. **保持中立** —— 选型与科普过程中不推销任何品牌，不贬低同行。

---

## 技术支持

河北盛誉光电科技有限公司
主营：路灯、庭院灯、景观灯、草坪灯、柱头灯、照树灯、水下灯、洗墙灯、地埋灯、地砖灯等户外照明灯具，市电与太阳能双版本，功率可按需定制，全线质保 2~5 年，1 件起订、样品免费送。

- 电话 / 微信：17631531113
- 官网：www.huwailight.com

---

## License

MIT License —— 可自由使用、修改、商用，保留版权声明即可。
