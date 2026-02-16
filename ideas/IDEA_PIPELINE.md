# Idea Pipeline System
## For Ryan's Endless Stream of Ideas

---

## 🎯 Philosophy

**Every idea gets captured. Every idea gets evaluated. Most ideas die gracefully.**

This system prevents:
- Idea abandonment (forgotten before evaluation)
- Shiny object syndrome (starting before vetting)
- Analysis paralysis (endless research without decision)
- Context bloat (keeping half-baked ideas in working memory)

---

## 📁 Directory Structure

```
ideas/
├── queue/           # Raw ideas waiting for research
│   └── YYYYMMDD-idea-name.md
├── research/        # Deep-dive completed ideas
│   └── idea-name.md
├── archived/        # Rejected/paused ideas (searchable)
│   └── idea-name.md
└── active/          # Currently building
    └── idea-name/
```

---

## 🔄 The Pipeline Flow

### Stage 1: CAPTURE (2 minutes)
**Trigger:** "I have an idea..."
**Action:** Quick template fill → drops into `queue/`
**No research yet. Just capture.**

### Stage 2: RESEARCH (30-60 min, async)
**Trigger:** "Research this idea" or cron/auto-pick from queue
**Action:** Spawn sub-agent → Deep analysis → Moves to `research/`
**Output:** Full viability report with scores

### Stage 3: DECISION (5 min)
**Trigger:** Research complete
**Action:** Review scores → Go/No-Go/Park
- **GO** → Move to `active/`, add to build queue
- **NO-GO** → Move to `archived/`, tag with reason
- **PARK** → Move to `archived/`, tag for future review

### Stage 4: BUILD (ongoing)
**Active project** → App factory, tracked separately

---

## 📊 Scoring Rubric (0-10 each)

### 1. VIABILITY (Can we build it?)
- 10 = We have all skills/resources now
- 5 = Doable with learning curve
- 0 = Requires impossible tech/partnerships

### 2. MARKETABILITY (Will people pay?)
- 10 = Clear pain point, proven demand, easy to reach customers
- 5 = Solution looking for problem OR saturated market
- 0 = No identifiable market

### 3. MONETIZATION (How does it make money?)
- 10 = Obvious revenue model, high margins, recurring
- 5 = One-time sales OR low margins OR unclear path
- 0 = No monetization strategy

### 4. TIME TO MARKET (How fast?)
- 10 = MVP in <2 weeks
- 7 = MVP in 1 month
- 5 = MVP in 2-3 months
- 0 = 6+ months to anything shippable

### 5. HOURS-TO-DOLLARS (Efficiency)
- 10 = Low hours, high revenue potential
- 5 = Linear time/money trade
- 0 = High hours, low reward

---

## 🏆 Composite Scores

**TOTAL SCORE** (0-50): Sum of all 5 categories

**RANKINGS:**
- 45-50 = **TIER 1**: Build immediately
- 38-44 = **TIER 2**: Strong candidate, queue for next
- 30-37 = **TIER 3**: Viable but not urgent
- 20-29 = **TIER 4**: Weak, probably archive
- <20 = **TIER 5**: Archive unless strategic reason

**QUICK-WIN SCORE** (Time × Money): 
`(Time to Market score × Monetization score × Hours-to-Dollars score)`
- High = Fast money, prioritize

---

## 🔍 Finding Related Ideas

All idea files are indexed by `memory_search`. To find connections:

**You say:** "Find ideas related to [topic]"
**I do:** Semantic search across queue/research/archived → Surface related concepts

**You say:** "What ideas use [technology]?"
**I do:** Search for tech keywords → Cross-reference

**You say:** "Show me all Tier 1 ideas"
**I do:** Filter research/ folder by score → Display ranked list

---

## 🚫 Anti-Patterns (Avoid These)

❌ **Keeping ideas in your head** → They die or distract
❌ **Researching immediately** → Sucks energy from current work
❌ **No-go without documentation** → You'll revisit the same bad idea
❌ **No cross-referencing** → You'll rebuild the same component 3 times
❌ **Queue growing forever** → Review weekly, archive stale ideas

✅ **DO**: Capture fast, research async, decide quickly, build focused

---

## 📋 Weekly Ritual (15 min)

Every Monday:
1. Review `queue/` — anything urgent capture?
2. Check `research/` — any decisions pending?
3. Scan `active/` — on track?
4. Archive ideas >30 days old in queue with no research

---

## 🎯 Current Focus Rule

**ONE active idea at a time.** Research can run parallel (async), but building happens sequentially.

Why? Because you have 20 projects at 80%. We finish now.

---

*Last updated: 2026-02-16*
