# 小安 (Xiao An) — MCI Chatbot Project

**A Source-Grounded, Caregiver-Aware Engagement Companion for Chinese Older Adults with MCI or Early Dementia**

| **Project Information** | |
|------------------------|---|
| **Project Name** | 小安 (Xiao An) |
| **Version** | 0.2.0 |
| **Last Updated** | 2026-07-06 |
| **Status** | Active Development |
| **Target Users** | Chinese older adults with MCI/early dementia, caregivers |
| **Primary Platform** | Telegram |
| **Secondary Platforms** | WeChat, WebUI |
| **Framework** | Nanobot (HKUDS) |
| **LLM Provider** | DeepSeek V4 Flash |
| **RAG Backend** | Custom Hybrid RAG (Semantic + Keyword) |

---

## What This Project Does

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
| Hybrid RAG (team integration) | ⏳ In Progress | 30% |

---

## Project Overview


### Core Principles

| Principle | Description |
|-----------|-------------|
| **Source-Grounded** | Every answer comes from curated knowledge sources, not LLM hallucination |
| **Caregiver-Aware** | Supports caregivers with tools for monitoring and personalization |
| **Gentle Engagement** | Provides activities and check-ins without being patronizing |
| **Safety-First** | Explicitly refuses diagnosis, medication advice, and treatment decisions |
| **Privacy-First** | Private data stays local; never sent to corporate LLM training |

### What This Bot Is NOT

| ❌ Not This | ✅ Instead |
|------------|------------|
| Medical diagnostic tool | Information resource |
| Treatment recommendation system | Safe boundary with escalation |
| Crisis intervention service | Caregiver/emergency escalation |
| Mental health therapy | Emotional support companion |
| Replacement for professional care | Complement to professional care |

---

## Project Structure

### Key Files Description

| File | Purpose | Owner |
|------|---------|-------|
| `knowledge_tool.py` | Main entry: intent → safety → RAG → response | You |
| `intent_recognizer.py` | Classifies messages into 8 intents | You |
| `safety_handler.py` | Handles medication/diagnosis/safety | You |
| `debug_logger.py` | Logs all interactions for debugging | You |
| `telegram_reminder.py` | Scheduled reminders (5x daily) | You |
| `dashboard.py` | Streamlit caregiver monitoring | You |
| `orchestrator.py` | Hybrid RAG orchestrator | Teammate |
| `medicine_normalizer.py` | Medicine alias mapping | Teammate |

---

## Current Status

### Overall Progress

| Phase | Status | % Complete |
|-------|--------|------------|
| Phase 1: Setup & Integration | ✅ Done | 100% |
| Phase 2: Intent Recognizer | ✅ Done | 100% |
| Phase 3: Safety Boundaries | ✅ Done | 100% |
| Phase 4: Hybrid RAG | ⏳ In Progress | 30% |
| Phase 5: Evidence Checking | ✅ Done | 100% |
| Phase 6: Active Engagement | ✅ Done | 100% |
| Phase 7: Caregiver Memory | ❌ Not Started | 0% |
| Phase 8: Evaluation Benchmark | ❌ Not Started | 0% |
| Phase 9: User Testing | ❌ Not Started | 0% |
| Cloud Deployment | ❌ Not Started | 0% |


---

## 6. Features Implemented

### ✅ Your Features (Complete)

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



| Feature | Description | Status |
|---------|-------------|--------|
| **Hybrid RAG** | Semantic + keyword retrieval | ⏳ In Progress |
| **Chroma DB** | Vector database for embeddings | ⏳ In Progress |
| **Semantic Search** | Meaning-based retrieval | ⏳ In Progress |

---
## 7. Data flow
1. User Message (Telegram/WeChat/WebUI)
    ↓
2. Intent Recognition
    - Classifies into 8 intents
    - Priority: Safety > Medication > Knowledge > Others
    ↓
3. Safety & Medical Boundary
    - Medication questions → Refusal with doctor/caregiver guidance
    - Diagnosis questions → Refusal with guidance
    - Health complaints → Escalation with caregiver/emergency guidance
    - Emergency → Escalate to caregiver or emergency services
    ↓
4. Module Routing 
    - Knowledge QA → Hybrid RAG (TEAMMATE'S WORK)
    - Reminder → Scheduler (YOUR WORK)
    - Activity → Activity Generator (YOUR WORK)
    - Emotional → Support Response (YOUR WORK)
    - Personal Memory → Memory Store (FUTURE)
    - Unknown → Graceful Fallback (YOUR WORK)
    ↓
5. RAG Pipeline 
    - Hybrid Search: Semantic + Keyword (BM25)
    - Chroma DB vector retrieval
    - Evidence sufficiency check (YOUR WORK)
    - Response generation
    ↓
6. Debug Logging 
    - Log: intent, chunks, sources, safety level, response
    - JSON + text logs
    ↓
7. Response to User 
    - Traditional Chinese
    - 3-6 sentences
    - Source display


    
