# Claude Pro vs Anthropic API: Complete Research Report

## Executive Summary

**Bottom Line**: Claude Pro ($20/month consumer subscription) does **NOT** include Anthropic API access. They are completely separate products with separate billing systems. However, Claude Pro **does** include Claude Code access (Anthropic's terminal-based coding tool), which has led to some confusion. There are unofficial workarounds to bridge Claude Pro with external systems, but they come with significant risks.

---

## 1. Does Claude Pro Include API Credits or Access?

**NO.** Claude Pro is strictly a consumer web UI subscription. From Anthropic's official pricing:

| Plan | Price | Includes API? |
|------|-------|---------------|
| Free | $0 | No |
| Pro | $20/month ($17/month annual) | **No** |
| Max | From $100/month | **No** |
| Team | $20-25/seat/month | No |
| Enterprise | Custom | No |
| **API (Console)** | Pay-as-you-go | **Yes - this is the only way** |

**Key Finding**: The [Anthropic Pricing Page](https://claude.com/pricing) clearly separates "Chat on web, iOS, Android and Desktop" (consumer plans) from API pricing, which is listed separately with per-token rates ($3-15 per million tokens input, $15-75 per million output).

---

## 2. Relationship Between Claude Pro and API

### Two Completely Separate Systems:

**Claude Pro (Consumer)**:
- Web interface at claude.ai
- Monthly subscription fee
- Usage limits based on "messages" (not tokens)
- Includes features: Projects, Research, Memory, Artifacts, Claude Code
- Billed by Anthropic's consumer billing system

**Anthropic API (Developer)**:
- Programmatic access via platform.claude.com
- Pay-as-you-go pricing
- Billed per token (input/output)
- Requires separate signup and payment method
- Billed through developer console

### What Claude Pro DOES Include (The Source of Confusion):

According to [Claude Code documentation](https://code.claude.com/docs/en/setup):

> **"Claude Pro or Max plan (recommended): Subscribe to Claude's Pro or Max plan for a unified subscription that includes both Claude Code and Claude on the web"**

**Important**: Claude Code authenticates using your claude.ai account (Pro/Max), NOT API keys. This has led people to think Pro includes API access, but Claude Code is a separate tool that uses a different authentication method than the official API.

---

## 3. Workarounds, Integrations, and Third-Party Tools

### A. Unofficial Cookie-Based APIs (⚠️ Unofficial)

Several open-source projects reverse-engineer Claude's web interface to provide API-like functionality using Claude Pro accounts:

#### 1. **unofficial-claude-api** by st1vms
- **Repo**: https://github.com/st1vms/unofficial-claude-api
- **Method**: Uses Firefox + geckodriver to extract session cookies from logged-in Claude account
- **Install**: `pip install unofficial-claude-api`
- **How it works**:
  - Automatically logs into claude.ai via Selenium
  - Extracts session cookie, user agent, organization ID
  - Makes HTTP requests to internal Claude endpoints
- **Features**:
  - Create/delete chats
  - Send messages with attachments (up to 5 files, 10MB each)
  - Get chat history
  - Proxy support (HTTP/S, SOCKS)

**Setup Steps**:
```python
from claude_api.session import get_session_data
from claude_api.client import ClaudeAPIClient

# Auto-extract session from Firefox
session = get_session_data()
client = ClaudeAPIClient(session)

# Use like an API
chat_id = client.create_chat()
response = client.send_message(chat_id, "Hello!")
```

**Requirements**:
- Firefox installed with profile logged into claude.ai
- geckodriver in PATH
- Python >= 3.10

#### 2. **Claude-API** by KoushikNavuluri
- **Repo**: https://github.com/KoushikNavuluri/Claude-API
- **Install**: `pip install claude-api`
- **Method**: Manual cookie extraction from browser dev tools
- **Features**: Send messages, upload attachments, manage conversations

**Setup**:
```python
from claude_api import Client
cookie = "your_claude_cookie_from_browser"
claude_api = Client(cookie)
```

### B. Claude Code API Gateway (Unofficial)

#### **claude-code-api** by codingworkflow
- **Repo**: https://github.com/codingworkflow/claude-code-api
- **What it does**: Wraps Claude Code CLI in an OpenAI-compatible API
- **Install**: `git clone https://github.com/codingworkflow/claude-code-api && cd claude-code-api && make install`
- **Features**:
  - OpenAI-style endpoints (`/v1/chat/completions`)
  - Streaming and non-streaming responses
  - Model aliases
  - Requires Claude Code installed and authenticated

**Setup Steps**:
1. Install Claude Code: `curl -fsSL https://claude.ai/install.sh | bash`
2. Authenticate with Claude Pro account: `claude` (opens browser auth)
3. Start API gateway: `make start`
4. Use OpenAI-compatible endpoint at `http://localhost:8000`

### C. Multi-Account Load Balancer

#### **ccflare** by snipeship
- **Repo**: https://github.com/snipeship/ccflare
- **Purpose**: Proxy that load-balances across multiple Claude accounts (Free, Pro, or Team)
- **Features**:
  - Distributes requests to avoid rate limits
  - Real-time analytics dashboard
  - Request/response logging
  - Session management (5-hour sessions)

**Setup**:
```bash
git clone https://github.com/snipeship/ccflare
cd ccflare
bun install
bun run ccflare
export ANTHROPIC_BASE_URL=http://localhost:8080
```

### D. Browser Automation Approaches

All unofficial methods rely on one of these approaches:

1. **Cookie Extraction**: Extract session cookies from authenticated browser session
2. **Selenium/Playwright**: Automate browser to interact with claude.ai
3. **MITM Proxy**: Intercept requests from official Claude desktop app

---

## 4. Claude for Work/Teams - Does It Change Anything?

**NO** - Claude for Teams and Enterprise also do NOT include API access.

### Team/Enterprise Plans Include:
- Centralized billing for web interface usage
- SSO and domain capture
- Admin controls
- Claude Code access for team members
- Audit logs, compliance API
- **Still NO API credits or access**

### Team API Access Still Requires:
- Separate API console signup at platform.claude.com
- Separate billing/payment method
- Per-token usage charges

---

## 5. Official API Access Setup (The Right Way)

If you need API access for OpenClaw or any external system, here's the official path:

### Step-by-Step API Setup:

1. **Go to Anthropic Console**
   - URL: https://console.anthropic.com (redirects to platform.claude.com)

2. **Create Account/Sign In**
   - Use separate credentials from your Claude Pro account (or same email, different system)

3. **Add Payment Method**
   - Go to Settings → Billing
   - Add credit card
   - API is pay-as-you-go, no monthly fee

4. **Generate API Key**
   - Go to API Keys section
   - Click "Create Key"
   - Copy key (starts with `sk-ant-`)

5. **Set Usage Limits (Recommended)**
   - Set monthly spending cap to avoid surprises
   - Default limits are low for new accounts

6. **Start Using**
   ```python
   from anthropic import Anthropic
   client = Anthropic(api_key="sk-ant-...")
   ```

### API Pricing (as of 2025):
| Model | Input (≤200K) | Output (≤200K) |
|-------|--------------|----------------|
| Opus 4.6 | $5/MTok | $25/MTok |
| Sonnet 4.5 | $3/MTok | $15/MTok |
| Haiku 4.5 | $1/MTok | $5/MTok |

**Note**: 1 million tokens ≈ 750,000 words

---

## 6. Browser Automation / Unofficial Methods (Detailed)

### Method 1: Cookie-Based Access (Most Common)

**How it works**:
1. Log into claude.ai in your browser (with Pro subscription)
2. Open browser dev tools → Network tab
3. Find any request to `claude.ai/api/...`
4. Copy the `Cookie` header value
5. Use this cookie in unofficial API libraries

**Example**:
```python
import requests

cookie = "sessionKey=xxxxx; intercom-id=xxxxx; ..."
headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0..."
}

response = requests.post(
    "https://claude.ai/api/organizations/{org_id}/chat_conversations",
    headers=headers,
    json={"name": "", "uuid": "..."}
)
```

**Risks**:
- ❌ Violates Anthropic's Terms of Service
- ❌ Session cookies expire (requires re-authentication)
- ❌ Rate limits are stricter than official API
- ❌ Can break without warning when Anthropic updates their web app
- ❌ Account suspension risk

### Method 2: Claude Code + Wrapper

**How it works**:
1. Install Claude Code CLI (includes with Pro)
2. Authenticate: `claude` (OAuth with claude.ai)
3. Use unofficial wrapper to expose as HTTP API
4. Redirect API calls to local Claude Code instance

**Trade-offs**:
- ✅ More stable than cookie scraping
- ✅ Uses official authentication flow
- ❌ Adds latency (spawns subprocess)
- ❌ Still unofficial/unsupported
- ❌ Claude Code has its own usage limits

### Method 3: Browser Automation (Puppeteer/Playwright)

**Approach**:
```javascript
const puppeteer = require('puppeteer');
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://claude.ai');
// ... automate login if needed
await page.type('[contenteditable]', 'Hello Claude');
await page.keyboard.press('Enter');
// ... scrape response
```

**Issues**:
- Very fragile (UI changes break automation)
- Slow (full browser overhead)
- Detectable by bot protection

---

## Summary Table: Official vs Unofficial Methods

| Method | Cost | Stability | Risk | Best For |
|--------|------|-----------|------|----------|
| Official API | Pay-per-use | ⭐⭐⭐⭐⭐ | None | Production systems |
| Claude Pro + Cookie API | $20/month | ⭐⭐⭐ | High | Personal experiments |
| Claude Code + Wrapper | $20/month | ⭐⭐⭐⭐ | Medium | Development tools |
| Browser Automation | $20/month | ⭐⭐ | Very High | Not recommended |

---

## Recommendation for OpenClaw

For OpenClaw specifically, you have three options:

### Option 1: Official Anthropic API (Recommended)
- Sign up at platform.claude.com
- Add payment method
- Set usage limits
- Use official Python/JS SDK
- **Pros**: Reliable, supported, predictable
- **Cons**: Additional cost on top of Pro

### Option 2: Use Claude Code (Included with Pro)
- Install Claude Code: `curl -fsSL https://claude.ai/install.sh | bash`
- Use `claude-code-api` wrapper to expose as HTTP API
- Configure OpenClaw to use local endpoint
- **Pros**: Uses existing Pro subscription
- **Cons**: Unofficial, adds complexity

### Option 3: Use Alternative Providers
- OpenRouter (aggregates multiple models including Claude)
- AWS Bedrock (Claude via AWS)
- Google Vertex AI
- **Pros**: May have existing credits/subscriptions
- **Cons**: Different pricing, may not have latest models

---

## Important Disclaimer

**Unofficial methods violate Anthropic's Terms of Service**. Using them risks:
- Account termination
- Loss of Pro subscription
- IP-based restrictions
- Legal action (though rare for individual use)

For any production or important use case, the official API is strongly recommended.

---

## Resources

- Anthropic Pricing: https://claude.com/pricing
- Anthropic Console: https://console.anthropic.com
- Claude Code Docs: https://code.claude.com/docs
- Official Python SDK: https://github.com/anthropics/anthropic-sdk-python
- Unofficial API (st1vms): https://github.com/st1vms/unofficial-claude-api
- Claude Code API Gateway: https://github.com/codingworkflow/claude-code-api
- CCFlare Proxy: https://github.com/snipeship/ccflare
