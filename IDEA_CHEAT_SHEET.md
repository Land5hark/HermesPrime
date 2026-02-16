# 🎯 Ryan's Idea Pipeline Cheat Sheet
## How to Feed Me Your Ideas Without Drowning Us Both

---

## ⚡ QUICK COMMANDS

### Capture a New Idea
> **"I have an idea: [describe it]"**

I create a capture file in `ideas/queue/` with today's date. 2 minutes, no research yet.

---

### Research an Idea
> **"Research this idea: [name or describe]"**

I spawn a sub-agent to do deep dive:
- Market analysis
- Competitor research  
- Monetization strategy
- Time/cost estimates
- Full scoring (0-50)

Takes 30-60 min. Reports back with recommendation.

---

### Find Related Ideas
> **"Find ideas like [topic]"**

Semantic search across all ideas. Shows connections you forgot about.

---

### See Ranked Ideas
> **"Show me Tier 1 ideas"** or **"What should I build next?"**

Displays all researched ideas ranked by score.

---

### Make a Decision
> **"Go on [idea name]"** → Moves to active build queue
> **"Kill [idea name]"** → Archives with reason
> **"Park [idea name]"** → Archives for later review

---

## 🧠 THE PIPELINE

```
YOUR BRAIN → CAPTURE → RESEARCH → DECIDE → BUILD
     ↓           ↓          ↓         ↓       ↓
   Spark      2 min     30-60 min   5 min   Weeks
   of idea    Queue      Async       Go/     Focused
                         Sub-agent   No-Go   Work
```

**Rule: ONE active build at a time.** Research runs parallel. Building happens sequential.

---

## 📊 THE SCORING (0-50 total)

I evaluate every idea on:

| Factor | Weight | Question |
|--------|--------|----------|
| **Viability** | 1.0x | Can we build it? |
| **Marketability** | 1.2x | Will people pay? |
| **Monetization** | 1.2x | How does it make money? |
| **Time to Market** | 1.5x | How fast to MVP? |
| **Hours-to-$** | 1.0x | Efficient use of time? |

**Tiers:**
- **45-50**: Build immediately
- **38-44**: Queue for next  
- **30-37**: Viable but wait
- **20-29**: Probably skip
- **<20**: Archive

---

## 🎯 WHAT TO SAY

### When You Have a New Idea:
> *"Idea: A platform that connects CNC machinists with 3D printing jobs"*

**I do:** Create `ideas/queue/20260216-cnc-3d-platform.md`

---

### When You Want It Researched:
> *"Research the CNC 3D platform idea"*

**I do:** Spawn sub-agent → Deep analysis → Move to `ideas/research/` → Report scores

---

### When You're Ready to Build:
> *"Show me my best ideas"*

**I do:** Rank all Tier 1-2 ideas → You pick → Move to active

---

### When You Forgot What You Thought Of:
> *"Find ideas about manufacturing"* or *"What was that genome idea?"*

**I do:** Semantic search across all idea files → Surface matches

---

## 🚫 WHAT NOT TO DO

❌ **"Let's build this right now"** (before research)
❌ **"Research all my ideas today"** ( overwhelm, decision fatigue)
❌ **"Keep this in your context window"** (bloat, forget)
❌ **"I'll remember this idea"** (you won't)

✅ **DO**: Capture fast, research async, decide once, build focused

---

## 📁 WHERE IDEAS LIVE

- `ideas/queue/` — Raw captures waiting for research
- `ideas/research/` — Full analysis with scores
- `ideas/archived/` — Rejected or parked
- `ideas/active/` — Currently building

---

## 🔄 WEEKLY RITUAL (Optional)

Every Monday, I can:
1. Review queue — surface urgent captures
2. Check research — pending decisions
3. Suggest one idea to research this week

Say: **"Run my weekly idea review"**

---

## 💡 EXAMPLE WORKFLOW

**You:** *"Idea: AI-powered genome analysis platform for methylation data"*

**→ Same day:** Capture file created

**You:** *"Research that genome platform idea"*

**→ 45 min later:** Full report with scores (Viability: 8, Market: 7, Money: 9, Speed: 6, Efficiency: 7 = 37/50 Tier 2)

**You:** *"Show me my ranked ideas"*

**→ I display:**
1. Genome Platform (37/50) — Tier 2
2. CNC Job Board (42/50) — Tier 2  
3. Door Factory SaaS (45/50) — TIER 1 ← Build this

**You:** *"Go on the door factory SaaS"*

**→ I do:** Move to active, start app factory scaffold

---

## 🔗 RELATED FILES

- Pipeline system: `ideas/IDEA_PIPELINE.md`
- Capture template: `ideas/TEMPLATE_CAPTURE.md`
- Research template: `ideas/TEMPLATE_RESEARCH.md`
- This cheat sheet: `IDEA_CHEAT_SHEET.md`

---

*Your ideas deserve evaluation. Most deserve archiving. A few deserve everything.*
