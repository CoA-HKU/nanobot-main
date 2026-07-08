# 小安 (Xiao An) — MCI Chatbot Project

| **Project Information** | |
|------------------------|---|
| **Project Name** | 小安 (Xiao An) |
| **Version** | 0.3.0 |
| **Last Updated** | 2026-07-08 |
| **Status** | Active Development |
| **Target Users** | Chinese older adults with MCI/early dementia, caregivers |
| **Primary Platform** | Telegram |
| **Secondary Platforms** | WeChat, WebUI |
| **Framework** | Nanobot (HKUDS) |
| **LLM Provider** | DeepSeek V4 Flash |
| **RAG Backend** | Custom Hybrid RAG (Semantic + Keyword) |

---

## Executive Summary

小安 (Xiao An) is a **source-grounded, caregiver-aware engagement companion** designed for Chinese older adults with Mild Cognitive Impairment (MCI) or early dementia. Unlike generic chatbots, 小安:

- ✅ **Provides trustworthy dementia information** from curated sources (HA, JCCPA, WHO, etc.)
- ✅ **Offers gentle engagement** through check-ins, memory exercises, and reminiscence prompts
- ✅ **Respects safety boundaries** by refusing diagnosis, medication advice, and treatment decisions
- ✅ **Supports caregivers** with authorable personalization (routines, reminders, preferences)
- ✅ **Speaks Traditional Chinese** (with future support for Cantonese)

### Key Achievements

| Milestone | Date | Status |
|-----------|------|--------|
| Nanobot + Telegram connected | 6/26/2026 | ✅ Done |
| RAG integration via MCP | 6/26/2026 | ✅ Done |
| Intent recognizer implemented | 7/2/2026 | ✅ Done |
| Safety/medical boundaries | 7/2/2026 | ✅ Done |
| Caregiver dashboard | 7/3/2026 | ✅ Done |
| Reminder system | 7/3/2026 | ✅ Done |
| Active engagement features | 7/4/2026 | ✅ Done |
| Hybrid RAG | 7/6/2026 | ✅ Done |
| Caregiver Memory | 7/7/2026 | ✅ Done |
| RAG Server (Standalone) | 7/7/2026 | ✅ Done |
| Nanobot Bridge (Auto-Discovery) | 7/7/2026 | ✅ Done |

---

## Overall Progress

| Phase | Status | % Complete |
|-------|--------|------------|
| Phase 1: Setup & Integration | ✅ Done | 100% |
| Phase 2: Intent Recognizer | ✅ Done | 100% |
| Phase 3: Safety Boundaries | ✅ Done | 100% |
| Phase 4: Hybrid RAG | ✅ Done | 100% |
| Phase 5: Evidence Checking | ✅ Done | 100% |
| Phase 6: Active Engagement | ✅ Done | 100% |
| Phase 7: Caregiver Memory | ✅ Done | 100% |
| Phase 8: Evaluation Benchmark | ⏳ In Progress | 0% |
| Phase 9: User Testing | ⏳ Not Started | 0% |
| Cloud Deployment | ⏳ Not Started | 0% |

---

## Features Implemented

| Feature | Description | Status |
|---------|-------------|--------|
| **Telegram Channel** | Full Telegram bot with rich messages | ✅ |
| **WeChat Channel** | WeChat integration | ✅ |
| **WebUI** | Browser interface via WebSocket | ✅ |
| **Intent Recognizer** | 8 intents: knowledge, medication, safety, reminder, activity, emotional, personal, unknown | ✅ |
| **Safety Handler** | Refusal of medication/diagnosis questions | ✅ |
| **Medical Boundary** | Escalation to caregivers/emergency | ✅ |
| **Debug Logging** | JSON + text logs with all interaction data | ✅ |
| **Caregiver Dashboard** | Streamlit dashboard with conversation history, metrics | ✅ |
| **Medication Reminders** | Scheduled reminders (8am, 9am, 11am, 3pm, 9pm) | ✅ |
| **Cognitive Activities** | Memory exercises, word association | ✅ |
| **Emotional Support** | Empathetic responses | ✅ |
| **Sleep/Wellness Nudges** | Morning/evening check-ins | ✅ |
| **Source Display** | Shows where answers come from | ✅ |
| **Caregiver Memory** | Personalization via `/setname`, `/addpref`, `/addroutine`, `/calm`, `/profile` | ✅ |
| **Hybrid RAG** | Semantic + keyword retrieval with confidence scores | ✅ |
| **Semantic Search** | Meaning-based retrieval using sentence-transformers | ✅ |
| **RAG Server** | Standalone Flask API server on port 5001 | ✅ |
| **CLI Tool** | `rag_cli.py` for testing without Telegram | ✅ |
| **Automated Web Scraping** | `web_ingest.py` with configurable crawling | ✅ |
| **Evidence Sufficiency** | Check if chunks support the answer | ✅ |


---

## Data Flow

```
1. User Message (Telegram/WeChat/WebUI)
    ↓
2. Intent Recognition (YOUR WORK)
    - Classifies into 8 intents
    - Priority: Safety > Medication > Knowledge > Others
    ↓
3. Safety & Medical Boundary (YOUR WORK)
    - Medication questions → Refusal with doctor/caregiver guidance
    - Diagnosis questions → Refusal with guidance
    - Health complaints → Escalation with caregiver/emergency guidance
    - Emergency → Escalate to caregiver or emergency services
    ↓
4. Module Routing (YOUR WORK)
    - Knowledge QA → Hybrid RAG (TEAMMATE'S WORK)
    - Reminder → Scheduler (YOUR WORK)
    - Activity → Activity Generator (YOUR WORK)
    - Emotional → Support Response (YOUR WORK)
    - Personal Memory → Memory Store (YOUR WORK)
    - Unknown → Graceful Fallback (YOUR WORK)
    ↓
5. RAG Pipeline (TEAMMATE'S WORK)
    - Hybrid Search: Semantic + Keyword (BM25)
    - Chroma DB vector retrieval
    - Evidence sufficiency check (YOUR WORK)
    - Response generation
    ↓
6. Debug Logging (YOUR WORK)
    - Log: intent, chunks, sources, safety level, response
    - JSON + text logs
    ↓
7. Response to User (YOUR WORK)
    - Traditional Chinese
    - 3-6 sentences
    - Source display
```

---

## Intent Categories

| Intent | Description | Example |
|--------|-------------|---------|
| `knowledge_qa` | Dementia/MCI knowledge | "什麼是腦退化症？" |
| `personal_memory` | Caregiver-personal info | "我喜歡吃什麼？" |
| `reminder_request` | Setting/checking reminders | "提醒我9點吃藥" |
| `cognitive_activity` | Memory exercises | "我想做記憶練習" |
| `emotional_support` | Emotional needs | "我覺得好孤單" |
| `safety_sensitive` | Emergency/danger | "我頭暈得好犀利" |
| `medication_or_diagnosis` | Medical advice | "我應該吃多少藥？" |
| `unknown` | Everything else | "今天天氣好嗎？" |

---


## Development Phases

### Phase 1: Stabilize Current System (✅ Done)
- CLI and Telegram use same answer function
- Debug logs for intent, chunks, sources, safety
- Every answer returns: answer, sources, found, intent, safety, debug info

### Phase 2: Validate Intent Recognizer (✅ Done)
- 8 intent categories
- Unit tests for each intent
- Priority rules: safety and medication override QA
- Test with Traditional Chinese, Cantonese, mixed Chinese/English

### Phase 3: Safety and Medical Boundaries (✅ Done)
- Separate handlers for safety_sensitive and medication_or_diagnosis
- Medication questions do NOT go through RAG
- Emergency situations trigger caregiver or emergency escalation

### Phase 4: Improve Retrieval with Hybrid RAG (✅ Done)
- Add semantic search (sentence-transformers)
- Add BM25 keyword search
- Merge and deduplicate results
- Reranking for relevance

### Phase 5: Evidence Sufficiency Checking (✅ Done)
- Check if retrieved chunks support the answer
- Return sufficient/insufficient, reason, risk type
- Fallback: "I can't find enough information"

### Phase 6: Active Engagement (✅ Done)
- Simple check-ins
- Reminiscence prompts
- Gentle conversation
- Orientation support
- Simple activity suggestions (category naming, word association)
- Daily reflection
- Caregiver-authored routines

### Phase 7: Caregiver Memory (✅ Done)
- Separate knowledge stores:
  - Dementia knowledge base (public, curated)
  - Personal memory base (caregiver-authored)
- Caregiver-authored: routines, preferences, names, reminders, calming phrases
- Commands: `/setname`, `/addroutine`, `/addpref`, `/calm`, `/profile`

### Phase 8: Evaluation Benchmark (⏳ In Progress)
- 30-50 question benchmark across categories
- Metrics: intent accuracy, retrieval accuracy, safety compliance, hallucination rate

### Phase 9: User & Expert Studies (❌ Planned)
- Pre-design interviews with PwD/caregivers
- Post-use interviews
- Expert review (clinicians, dementia researchers, care workers)
- CHI-style publication

---


## RAG Research Papers
- A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces (arXiv:2605.03534)
- Awesome RAG: https://github.com/Danielskry/Awesome-RAG

## Non-Research Resources
- Should You Be Using RAG in 2026? (dev.to/riddhesh)
- RAG Types (turingpost.com/p/ragtypes)
- RAG Is Dead — And Why That's the Best News (medium.com)

## Knowledge Sources
- JCCPA (耆智園): https://www.jccpa.org.hk/
- HA Smart Patient (智友站): https://www.smartpatient.ha.org.hk/
- HA CPH (精神健康): https://www3.ha.org.hk/cph/imh/
- Elderly.gov.hk: https://www.elderly.gov.hk/
- Alzheimer's International: https://www.alzint.org/
- World Alzheimer Reports (2023-2025)
- WHO Risk Dementia Report


---

## Commands

```powershell
# Start bot
cd C:\Users\user\Desktop\nanobot-main-main5\nanobot-main
.\start_bot.cmd

# Start RAG server (standalone)
cd C:\Users\user\.nanobot
py -3.14 rag_server.py

# Test RAG via CLI
py -3.14 rag_cli.py "什麼是腦退化症？"

# Test knowledge_tool
py -3.14 knowledge_tool.py

# Launch dashboard
py -3.14 -m streamlit run dashboard.py

# View logs
type C:\Users\user\.nanobot\logs\bot_debug.log
```

### Caregiver Commands on Telegram

| Command | Description |
|---------|-------------|
| `/setname 陳婆婆` | Sets patient name |
| `/addroutine 9:00 吃藥` | Adds daily routine |
| `/addpref 喜歡聽粵曲` | Adds preference |
| `/calm 一切安好` | Adds calming phrase |
| `/profile` | Shows all stored info |


*Last Updated: 2026-07-08*

    
