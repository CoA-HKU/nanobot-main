mci_chatbot/
├── README.md                         ← overview + roadmap + nanobot mapping (繁中)
├── docs/
│   ├── setup-guide.md                ← install nanobot, init, run
│   ├── preparation-checklist.md      ← hardware / API keys / WhatsApp number / consent
│   ├── onboarding-a-patient.md       ← per-patient process incl. routing test
│   └── safety-and-privacy.md         ← not-a-medical-device, escalation, data, ethics
├── config/config.example.json        ← nanobot config (GLM/Zhipu provider, WhatsApp allowFrom)
├── workspace/
│   ├── SOUL.md                       ← bot personality "小安" + 繁中 + safety floor
│   ├── HEARTBEAT.md                  ← periodic tasks (NOT per-patient reminders)
│   ├── profiles/
│   │   ├── README.md                 ← filename = WhatsApp number w/ country code
│   │   └── _template.md              ← patient profile template
│   └── skills/
│       ├── patient-profile/SKILL.md  ← always-on; identifies patient, loads profile
│       ├── medication-reminders/SKILL.md  ← uses nanobot `cron`
│       ├── health-info/SKILL.md      ← web search/fetch + safety disclaimers
│       └── cognitive-training/
│           ├── SKILL.md              ← 5–10 min conversational exercises
│           └── references/exercises.md  ← CST-style exercise library
├── research/
│   ├── README.md                     ← contribution, RQs, dual-track timeline
│   ├── study-materials.md            ← procedure, interview guides, measures, logging spec
│   ├── consent-template.md           ← informed consent (繁中) — needs IRB sign-off
│   └── paper-outline.md              ← CHI paper skeleton
└── deploy/docker-compose.yml         ← always-on deployment
```