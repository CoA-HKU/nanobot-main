# knowledge_tool.py - Complete MCI Chatbot with All Features
# Location: C:\Users\user\.nanobot\knowledge_tool.py

import sys
import os
import re
from pathlib import Path
import numpy as np

# ============================================================
# Add .nanobot folder to Python path
# ============================================================
NANOBOT_DIR = Path.home() / ".nanobot"
if str(NANOBOT_DIR) not in sys.path:
    sys.path.insert(0, str(NANOBOT_DIR))

# ============================================================
# COMPONENT IMPORTS
# ============================================================

# 1. Core components
try:
    from intent_recognizer import IntentRecognizer
    from safety_handler import SafetyHandler
    from debug_logger import DebugLogger
    print("✅ Core components imported successfully!")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    COMPONENTS_AVAILABLE = False
    
    class IntentRecognizer:
        def detect_intent(self, msg): 
            return "knowledge_qa" if "什麼" in msg or "是" in msg else "unknown"
        def get_intent_description(self, intent): 
            return "未知" if intent == "unknown" else "知識問答"
    
    class SafetyHandler:
        def is_health_complaint(self, msg): 
            return any(k in msg for k in ["頭暈", "頭痛", "痛"])
        def handle_dizziness(self, msg): 
            return "⚠️ 如果你感到不適，請告訴照顧者或看醫生。"
        def handle_safety_sensitive(self, msg): 
            return "⚠️ 如有危險，請立即告訴照顧者或打999。"
        def handle_medication_or_diagnosis(self, msg): 
            return "⚠️ 小安不能提供用藥建議。請諮詢醫生。"
    
    class DebugLogger:
        def log_interaction(self, **kwargs): 
            print(f"[LOG] {kwargs.get('user_message', '')[:50]}")
        def get_recent_logs(self, n): 
            return []

# 2. Caregiver Memory
try:
    from caregiver_memory import CaregiverMemory
    CAREGIVER_MEMORY_AVAILABLE = True
    print("✅ Caregiver Memory loaded!")
except ImportError:
    CAREGIVER_MEMORY_AVAILABLE = False
    print("⚠️ Caregiver Memory not available.")

# 3. User Profiles
try:
    from user_profiles import USER_PROFILES, get_all_test_questions
    USER_PROFILES_AVAILABLE = True
    print("✅ User Profiles loaded!")
except ImportError:
    USER_PROFILES_AVAILABLE = False
    USER_PROFILES = {}
    print("⚠️ User Profiles not available.")

# 4. Metrics & Insights
try:
    from metrics import MetricsCollector
    from insights import InsightGenerator
    METRICS_AVAILABLE = True
    print("✅ Metrics & Insights loaded!")
except ImportError:
    METRICS_AVAILABLE = False
    print("⚠️ Metrics not available.")

# ============================================================
# SEMANTIC SEARCH (Hybrid RAG)
# ============================================================

try:
    from sentence_transformers import SentenceTransformer
    SEMANTIC_AVAILABLE = True
    print("✅ Semantic search loaded!")
except ImportError:
    SEMANTIC_AVAILABLE = False
    print("⚠️ Semantic search not available. Install: pip install sentence-transformers")

_semantic_model = None

def get_semantic_model():
    global _semantic_model
    if not SEMANTIC_AVAILABLE:
        return None
    if _semantic_model is None:
        try:
            _semantic_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("✅ Semantic model loaded!")
        except Exception as e:
            print(f"⚠️ Failed to load model: {e}")
            return None
    return _semantic_model

def semantic_search(query: str, top_k: int = 3) -> list:
    model = get_semantic_model()
    if model is None:
        return []
    
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    chunks = []
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if len(para.strip()) > 20:
                    chunks.append({
                        'text': para.strip(),
                        'source': file.name
                    })
        except:
            continue
    
    if not chunks:
        return []
    
    try:
        query_embedding = model.encode(query)
        chunk_texts = [c['text'] for c in chunks]
        chunk_embeddings = model.encode(chunk_texts)
        
        scores = np.dot(chunk_embeddings, query_embedding)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0.3:
                results.append({
                    'text': chunks[idx]['text'],
                    'source': chunks[idx]['source'],
                    'score': float(scores[idx])
                })
        return results
    except Exception as e:
        print(f"⚠️ Semantic search error: {e}")
        return []

def hybrid_search(query: str) -> str:
    combined_results = []
    
    semantic_results = semantic_search(query, top_k=3)
    keyword_results = search_keyword_fallback(query)
    
    if semantic_results:
        for r in semantic_results[:2]:
            combined_results.append(f"📄 {r['source']} (信心: {r['score']:.2f}): {r['text'][:200]}...")
    
    if keyword_results and keyword_results not in combined_results:
        combined_results.append(keyword_results)
    
    return '\n\n'.join(combined_results[:3]) if combined_results else ""

# ============================================================
# INITIALIZE COMPONENTS
# ============================================================
intent_recognizer = IntentRecognizer()
safety_handler = SafetyHandler()
debug_logger = DebugLogger()

if CAREGIVER_MEMORY_AVAILABLE:
    caregiver_memory = CaregiverMemory()
else:
    caregiver_memory = None

if METRICS_AVAILABLE:
    metrics_collector = MetricsCollector()
    insight_generator = InsightGenerator()
else:
    metrics_collector = None
    insight_generator = None

# ============================================================
# SEARCH FUNCTIONS
# ============================================================

def search_keyword_fallback(query: str) -> str:
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:2]) if results else ""

def search_resources(query: str) -> str:
    result = hybrid_search(query)
    return result if result else "小安暫時沒有這個資源資訊。請聯絡中心查詢。"

def search_medication(query: str) -> str:
    result = hybrid_search(query)
    return result if result else "小安暫時沒有這個藥物資訊。請諮詢醫生或藥劑師。"

def search_cognitive(query: str) -> str:
    result = hybrid_search(query)
    return result if result else "小安暫時沒有這個認知訓練資訊。請諮詢職業治療師。"

def search_psychological(query: str) -> str:
    result = hybrid_search(query)
    return result if result else "小安暫時沒有這個心理支援資訊。請聯絡專業人士。"

TOOLS = [
    {"name": "search_resources", "description": "Search for center locations, contact info, transport, and opening hours", "function": search_resources},
    {"name": "search_medication", "description": "Search for medication information, side effects, dosage, and interactions", "function": search_medication},
    {"name": "search_cognitive", "description": "Search for cognitive training exercises and activity plans", "function": search_cognitive},
    {"name": "search_psychological", "description": "Search for psychological support, coping strategies, and anxiety management", "function": search_psychological},
]

# ============================================================
# USER PROFILE DETECTION
# ============================================================

def detect_user_profile(message):
    """Detect which user profile matches the message"""
    if not USER_PROFILES_AVAILABLE:
        return None, None
    for profile_id, profile in USER_PROFILES.items():
        for keyword in profile.get("keywords", []):
            if keyword in message:
                return profile_id, profile
    return None, None

# ============================================================
# DETECT FUNCTION (Pattern Detection)
# ============================================================

DETECT_KEYWORDS = {
    "memory": ["忘記", "記性", "忘事", "記唔到", "memory", "忘", "記"],
    "language": ["講唔到", "搵唔到字", "speech", "語言", "表達", "詞語"],
    "orientation": ["迷路", "唔知時間", "lost", "confused", "混淆", "時間"],
    "mood": ["擔心", "焦慮", "depressed", "憂鬱", "緊張", "不安", "驚"],
}

def detect_patterns(user_id, user_message):
    """Detect patterns in user message and track them"""
    detected = []
    for category, keywords in DETECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_message:
                detected.append(category)
                break
    
    if caregiver_memory and detected:
        pattern_counts = caregiver_memory.get_memory(user_id, "detected_patterns", {})
        for category in detected:
            pattern_counts[category] = pattern_counts.get(category, 0) + 1
        caregiver_memory.set_memory(user_id, "detected_patterns", pattern_counts)
        
        total_patterns = sum(pattern_counts.values())
        if total_patterns >= 3:
            return f"""⚠️ 我留意到你多次提到一些值得關注的事情（共{total_patterns}次）。

這不是診斷，但值得留意。

💡 建議：
1. 記錄你的觀察
2. 與家人討論
3. 考慮諮詢醫生

需要我幫你準備見醫生的問題嗎？ (輸入 /doctor)"""
    
    return None

# ============================================================
# SCREENING QUESTIONS
# ============================================================

screening_sessions = {}

def ask_screening_questions(user_id):
    """Ask a series of screening questions"""
    if user_id not in screening_sessions:
        screening_sessions[user_id] = {"step": 0, "answers": []}
    
    session = screening_sessions[user_id]
    step = session["step"]
    
    questions = [
        ("今天星期幾？", "orientation"),
        ("記住這3個詞語：蘋果、巴士、紅色。你記得哪幾個？", "memory"),
        ("100減7等於多少？", "calculation"),
        ("你記得剛才的3個詞語嗎？", "recall"),
    ]
    
    if step >= len(questions):
        score = sum(1 for a in session["answers"] if a)
        result = "正常" if score >= 3 else "需要關注" if score >= 2 else "建議諮詢醫生"
        
        response = f"""📋 篩查結果（非診斷）：

你答對了 {score}/{len(questions)} 題。

📊 初步觀察：{result}

⚠️ 這只是一個簡單的觀察，不是醫療診斷。
💡 建議：{ "繼續觀察，如有持續擔憂可諮詢醫生" if score >= 3 else "建議與醫生討論你的情況" }

🔍 你想要：
/result → 查看詳細結果
/doctor → 準備見醫生的問題
/exit → 回到一般對話"""
        
        screening_sessions[user_id] = None
        return response
    
    question = questions[step][0]
    response = f"""🧠 問題 {step+1}/{len(questions)}：

{question}

請回答，或輸入 /skip 跳過"""
    
    session["current_question"] = questions[step][1]
    return response

def handle_screening_answer(user_id, answer):
    """Handle a screening answer"""
    if user_id not in screening_sessions or screening_sessions[user_id] is None:
        return None
    
    session = screening_sessions[user_id]
    if answer == "/skip":
        session["answers"].append(False)
    else:
        q_type = session.get("current_question", "unknown")
        if q_type == "orientation":
            days = ["一", "二", "三", "四", "五", "六", "日", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            session["answers"].append(any(day in answer for day in days))
        elif q_type == "memory" or q_type == "recall":
            key_words = ["蘋果", "巴士", "紅色", "apple", "bus", "red"]
            session["answers"].append(any(kw in answer for kw in key_words))
        elif q_type == "calculation":
            numbers = re.findall(r'\d+', answer)
            session["answers"].append(bool(numbers) and any(int(n) == 93 for n in numbers))
        else:
            session["answers"].append(True)
    
    session["step"] += 1
    return ask_screening_questions(user_id)

# ============================================================
# INFORMED CONSENT
# ============================================================

def get_consent_status(user_id):
    """Check if user has given consent"""
    if not caregiver_memory:
        return True  # No consent system available
    return caregiver_memory.get_memory(user_id, "consent_given", False)

def get_consent_response(user_message, user_id):
    """Handle consent flow"""
    if user_message.startswith("/consent_yes"):
        if caregiver_memory:
            caregiver_memory.set_memory(user_id, "consent_given", True)
            caregiver_memory.set_memory(user_id, "share_with_caregiver", True)
        return "✅ 感謝你！我會與你的看護者分享重要資訊。"
    
    if user_message.startswith("/consent_no"):
        if caregiver_memory:
            caregiver_memory.set_memory(user_id, "consent_given", True)
            caregiver_memory.set_memory(user_id, "share_with_caregiver", False)
        return "✅ 明白了。你的資料會保持私隱。"
    
    return None  # No consent response yet

# ============================================================
# GET USER ID
# ============================================================

def get_user_id(message=None):
    """Get user ID (for now, use default)"""
    return "default_user"

# ============================================================
# MAIN process_message FUNCTION
# ============================================================

def process_message(user_message: str) -> str:
    """Main entry point for processing user messages."""
    
    user_id = get_user_id()
    
    # ============================================================
    # 1. INFORMED CONSENT (First-time users)
    # ============================================================
    if not get_consent_status(user_id):
        consent_response = get_consent_response(user_message, user_id)
        if consent_response:
            if metrics_collector:
                metrics_collector.record_interaction(user_id, "consent", consent_response)
            return consent_response
        
        return """👋 你好！我是小安，一個認知健康助理。

在開始之前，請告訴我：
/consent_yes → 我同意與看護者分享資料
/consent_no  → 我不希望分享資料

你的選擇會影響我能提供的幫助。"""

    # ============================================================
    # 2. CAREGIVER COMMANDS
    # ============================================================
    if caregiver_memory:
        if user_message.startswith("/setname"):
            name = user_message.replace("/setname", "").strip()
            if name:
                caregiver_memory.set_memory(user_id, "name", name)
                response = f"✅ 已記住你的名字：{name}"
                if metrics_collector:
                    metrics_collector.record_interaction(user_id, "caregiver_command", response)
                return response
            return "請輸入名字，例如：/setname 陳婆婆"
        
        if user_message.startswith("/addroutine"):
            routine = user_message.replace("/addroutine", "").strip()
            if routine:
                caregiver_memory.add_routine(user_id, routine)
                response = f"✅ 已記住日常安排：{routine}"
                if metrics_collector:
                    metrics_collector.record_interaction(user_id, "caregiver_command", response)
                return response
            return "請輸入日常安排，例如：/addroutine 9:00 吃藥"
        
        if user_message.startswith("/addpref"):
            pref = user_message.replace("/addpref", "").strip()
            if pref:
                caregiver_memory.add_preference(user_id, pref)
                response = f"✅ 已記住你的喜好：{pref}"
                if metrics_collector:
                    metrics_collector.record_interaction(user_id, "caregiver_command", response)
                return response
            return "請輸入喜好，例如：/addpref 喜歡聽粵曲"
        
        if user_message.startswith("/calm"):
            phrase = user_message.replace("/calm", "").strip()
            if phrase:
                caregiver_memory.set_calming_phrase(user_id, phrase)
                response = f"✅ 已記住安撫語句：{phrase}"
                if metrics_collector:
                    metrics_collector.record_interaction(user_id, "caregiver_command", response)
                return response
            return "請輸入安撫語句，例如：/calm 一切安好，慢慢來"
        
        if user_message.startswith("/profile"):
            profile = caregiver_memory.get_user_profile(user_id)
            if profile:
                response = "📋 你的個人檔案：\n"
                for key, value in profile.items():
                    if key != "last_updated" and key != "detected_patterns":
                        response += f"  {key}: {value}\n"
                return response
            return "📋 暫時沒有個人檔案。"

    # ============================================================
    # 3. SCREENING FLOW
    # ============================================================
    if user_message.startswith("/screen"):
        response = ask_screening_questions(user_id)
        if metrics_collector:
            metrics_collector.record_interaction(user_id, "screening_start", response)
        return response
    
    # Handle screening answers
    if user_id in screening_sessions and screening_sessions[user_id] is not None:
        if user_message.startswith("/exit"):
            screening_sessions[user_id] = None
            return "📋 篩查已結束。有其他問題隨時可以問我！"
        
        response = handle_screening_answer(user_id, user_message)
        if response:
            if metrics_collector:
                metrics_collector.record_interaction(user_id, "screening_answer", response)
            return response

    # ============================================================
    # 4. DETECT PATTERNS
    # ============================================================
    detect_response = detect_patterns(user_id, user_message)
    if detect_response:
        if metrics_collector:
            metrics_collector.record_interaction(user_id, "detection", detect_response)
        return detect_response

    # ============================================================
    # 5. INTENT RECOGNITION
    # ============================================================
    intent = intent_recognizer.detect_intent(user_message)
    intent_desc = intent_recognizer.get_intent_description(intent) if hasattr(intent_recognizer, 'get_intent_description') else intent
    
    print(f"\n[PROCESS] Message: {user_message[:50]}...")
    print(f"[PROCESS] Intent: {intent_desc}")
    
    # Detect user profile
    if USER_PROFILES_AVAILABLE:
        profile_id, profile = detect_user_profile(user_message)
        if profile_id:
            print(f"[PROFILE] Detected: {profile['name']} ({profile['type']})")

    # ============================================================
    # 6. ROUTE BY INTENT
    # ============================================================
    
    # Safety
    if intent == "safety_sensitive":
        if safety_handler.is_health_complaint(user_message):
            response = safety_handler.handle_dizziness(user_message)
        else:
            response = safety_handler.handle_safety_sensitive(user_message)
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="ESCALATE", response=response, found=False,
            fallback_reason="Safety escalation triggered"
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Medication
    if intent == "medication_or_diagnosis":
        response = safety_handler.handle_medication_or_diagnosis(user_message)
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="FAIL", response=response, found=False,
            fallback_reason="Medication/diagnosis question refused"
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Reminder
    if intent == "reminder_request":
        response = "📋 好的！我已經記住了。請告訴我你想設定什麼提醒？"
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="PASS", response=response, found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Cognitive Activity
    if intent == "cognitive_activity":
        response = """🧠 好的！我們來做一個簡單的記憶練習。

請記住這3個詞語：
🍎 蘋果
🚌 巴士
🔴 紅色

1分鐘後我會問你記不記得。準備好了嗎？"""
        
        if metrics_collector:
            metrics_collector.record_activity_participation(user_id, "memory_exercise", True)
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="PASS", response=response, found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Emotional Support
    if intent == "emotional_support":
        name = "朋友"
        calming_phrase = None
        
        if caregiver_memory:
            name = caregiver_memory.get_name(user_id) or "朋友"
            calming_phrase = caregiver_memory.get_calming_phrase(user_id)
        
        mood_score = 3
        if "開心" in user_message or "好" in user_message:
            mood_score = 4
        elif "唔開心" in user_message or "不好" in user_message or "難過" in user_message:
            mood_score = 2
        elif "很差" in user_message or "好差" in user_message:
            mood_score = 1
        elif "非常好" in user_message or "很好" in user_message:
            mood_score = 5
        
        if calming_phrase:
            response = f"""💙 我明白你的感受，{name}。照顧好自己的情緒很重要。

{calming_phrase}

你可以試試：
1. 跟家人或朋友傾訴
2. 做幾次深呼吸，放鬆一下
3. 如果持續感到難過，可以尋求專業心理輔導

小安會一直在這裡陪伴你。"""
        else:
            response = f"""💙 我明白你的感受，{name}。照顧好自己的情緒很重要。

你可以試試：
1. 跟家人或朋友傾訴
2. 做幾次深呼吸，放鬆一下
3. 如果持續感到難過，可以尋求專業心理輔導

小安會一直在這裡陪伴你。"""
        
        if metrics_collector:
            metrics_collector.record_mood(user_id, mood_score)
            metrics_collector.record_interaction(user_id, intent, response)
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="PASS", response=response, found=True
        )
        return response
    
    # Knowledge QA (Hybrid RAG)
    if intent == "knowledge_qa":
        result = hybrid_search(user_message)
        
        if not result:
            response = "小安暫時沒有這個資訊。請向照顧者或專業人士查詢。"
            found = False
            fallback_reason = "No information found"
        else:
            response = result
            found = True
            fallback_reason = None
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent,
            chunks=["Found relevant content"] if found else [],
            sources=["knowledge files"] if found else [],
            safety_level="PASS", response=response, found=found,
            fallback_reason=fallback_reason
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Personal Memory
    if intent == "personal_memory":
        name = "朋友"
        if caregiver_memory:
            name = caregiver_memory.get_name(user_id) or "朋友"
        
        response = f"""📝 你好 {name}！你想告訴我關於自己的事情嗎？

你可以告訴我：
- 你喜歡什麼？ (例如：「我喜歡聽粵曲」)
- 你不喜歡什麼？ (例如：「我不喜歡苦瓜」)
- 你的日常習慣？ (例如：「我習慣7點起床」)

小安會記住這些，更好地陪伴你。

💡 照顧者可以用以下指令：
/setname 名字
/addroutine 日常安排
/addpref 喜好
/calm 安撫語句
/profile 查看檔案"""
        
        debug_logger.log_interaction(
            user_message=user_message, intent=intent, chunks=[], sources=[],
            safety_level="PASS", response=response, found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # Unknown
    response = "😊 小安不太明白你的意思。你可以問我關於腦退化症的問題、藥物資訊、或者告訴我你想做記憶練習。"
    
    debug_logger.log_interaction(
        user_message=user_message, intent=intent, chunks=[], sources=[],
        safety_level="PASS", response=response, found=False,
        fallback_reason="Unknown intent"
    )
    if metrics_collector:
        metrics_collector.record_interaction(user_id, intent, response)
    return response

# ============================================================
# TEST FUNCTION
# ============================================================

def test_knowledge_tool():
    """Test the integrated knowledge tool."""
    print("\n" + "=" * 70)
    print("🧪 Testing Complete Xiao An Chatbot")
    print("=" * 70)
    
    # ============================================================
    # ✅ ADD THIS: Auto-consent for testing
    # ============================================================
    if CAREGIVER_MEMORY_AVAILABLE:
        caregiver_memory.set_memory("default_user", "consent_given", True)
        caregiver_memory.set_memory("default_user", "share_with_caregiver", True)
        print("📝 Auto-consent enabled for testing")
    
    print(f"📁 Core components: {'✅' if COMPONENTS_AVAILABLE else '❌'}")
    print(f"📁 Caregiver Memory: {'✅' if CAREGIVER_MEMORY_AVAILABLE else '❌'}")
    print(f"📁 User Profiles: {'✅' if USER_PROFILES_AVAILABLE else '❌'}")
    print(f"📁 Semantic Search: {'✅' if SEMANTIC_AVAILABLE else '❌'}")
    print(f"📁 Metrics: {'✅' if METRICS_AVAILABLE else '❌'}")
    print("-" * 70)
    
    test_messages = [
        "什麼是腦退化症？",
        "我頭暈",
        "我可以吃兩粒藥嗎？",
        "提醒我吃藥",
        "我想做記憶練習",
        "我覺得好孤單",
        "我喜歡吃蘋果",
        "今天天氣如何？",
        "我最近常常忘記事情",  # Should detect pattern
        "/screen",              # Should start screening
        "我今天心情不好",       # Should detect mood
    ]
    
    print("\n📝 Processing test messages:\n")
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n{i}. 👤 用戶: {msg}")
        try:
            response = process_message(msg)
            print(f"   🤖 小安: {response[:150]}..." if len(response) > 150 else f"   🤖 小安: {response}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        print("   " + "-" * 40)
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_knowledge_tool()