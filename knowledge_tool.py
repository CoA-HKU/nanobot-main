# knowledge_tool.py - Multi-RAG Knowledge Search with Safety & Intent Integration
# Location: C:\Users\user\.nanobot\knowledge_tool.py

import sys
import os
from pathlib import Path
import numpy as np

# ============================================================
# FIX 1: Add .nanobot folder to Python path
# ============================================================
NANOBOT_DIR = Path.home() / ".nanobot"
if str(NANOBOT_DIR) not in sys.path:
    sys.path.insert(0, str(NANOBOT_DIR))

# ============================================================
# FIX 2: Import with error handling for Pylance
# ============================================================
try:
    from intent_recognizer import IntentRecognizer
    from safety_handler import SafetyHandler
    from debug_logger import DebugLogger
    print("✅ Safety components imported successfully!")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("Creating fallback components...")
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

# ============================================================
# IMPORT CAREGIVER MEMORY
# ============================================================
try:
    from caregiver_memory import CaregiverMemory
    CAREGIVER_MEMORY_AVAILABLE = True
    print("✅ Caregiver Memory loaded!")
except ImportError:
    CAREGIVER_MEMORY_AVAILABLE = False
    print("⚠️ Caregiver Memory not available.")

# ============================================================
# IMPORT METRICS & INSIGHTS (NEW!)
# ============================================================
try:
    from metrics import MetricsCollector  # type: ignore
    from insights import InsightGenerator  # type: ignore
    METRICS_AVAILABLE = True
    print("✅ Metrics & Insights loaded!")
except ImportError as e:
    METRICS_AVAILABLE = False
    print(f"⚠️ Metrics not available: {e}")

# ============================================================
# SEMANTIC SEARCH
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
# Initialize components
# ============================================================
intent_recognizer = IntentRecognizer()
safety_handler = SafetyHandler()
debug_logger = DebugLogger()

# Initialize caregiver memory
if CAREGIVER_MEMORY_AVAILABLE:
    caregiver_memory = CaregiverMemory()
else:
    caregiver_memory = None

# Initialize metrics collector
if METRICS_AVAILABLE:
    metrics_collector = MetricsCollector()
    insight_generator = InsightGenerator()
else:
    metrics_collector = None
    insight_generator = None

# ============================================================
# EXISTING: Search functions
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

# ============================================================
# TOOLS list
# ============================================================

TOOLS = [
    {
        "name": "search_resources",
        "description": "Search for center locations, contact info, transport, and opening hours",
        "function": search_resources,
    },
    {
        "name": "search_medication",
        "description": "Search for medication information, side effects, dosage, and interactions",
        "function": search_medication,
    },
    {
        "name": "search_cognitive",
        "description": "Search for cognitive training exercises and activity plans",
        "function": search_cognitive,
    },
    {
        "name": "search_psychological",
        "description": "Search for psychological support, coping strategies, and anxiety management",
        "function": search_psychological,
    },
]

# ============================================================
# Main process_message function
# ============================================================

def get_user_id(message=None):
    """Get user ID (for now, use default)"""
    # In production, extract from Telegram user ID
    return "default_user"

def process_message(user_message: str) -> str:
    """Main entry point for processing user messages."""
    
    # Get user ID
    user_id = get_user_id()
    
    # ============================================================
    # CAREGIVER COMMANDS
    # ============================================================
    
    if caregiver_memory:
        if user_message.startswith("/setname"):
            name = user_message.replace("/setname", "").strip()
            if name:
                caregiver_memory.set_memory(user_id, "name", name)
                response = f"✅ 已記住你的名字：{name}"
                
                # Record interaction
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
                    if key != "last_updated":
                        response += f"  {key}: {value}\n"
                if metrics_collector:
                    metrics_collector.record_interaction(user_id, "caregiver_command", response)
                return response
            response = "📋 暫時沒有個人檔案。你可以用以下指令設定：\n/setname 名字\n/addroutine 日常安排\n/addpref 喜好\n/calm 安撫語句"
            if metrics_collector:
                metrics_collector.record_interaction(user_id, "caregiver_command", response)
            return response
    
    # ============================================================
    # Step 1: Detect intent
    # ============================================================
    intent = intent_recognizer.detect_intent(user_message)
    intent_desc = intent_recognizer.get_intent_description(intent) if hasattr(intent_recognizer, 'get_intent_description') else intent
    
    print(f"\n[PROCESS] Message: {user_message[:50]}...")
    print(f"[PROCESS] Intent: {intent_desc}")
    
    # ============================================================
    # Step 2: Handle SAFETY_SENSITIVE
    # ============================================================
    if intent == "safety_sensitive":
        if safety_handler.is_health_complaint(user_message):
            response = safety_handler.handle_dizziness(user_message)
        else:
            response = safety_handler.handle_safety_sensitive(user_message)
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="ESCALATE",
            response=response,
            found=False,
            fallback_reason="Safety escalation triggered"
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 3: Handle MEDICATION_OR_DIAGNOSIS
    # ============================================================
    if intent == "medication_or_diagnosis":
        response = safety_handler.handle_medication_or_diagnosis(user_message)
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="FAIL",
            response=response,
            found=False,
            fallback_reason="Medication/diagnosis question refused"
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 4: Handle REMINDER_REQUEST
    # ============================================================
    if intent == "reminder_request":
        response = "📋 好的！我已經記住了。請告訴我你想設定什麼提醒？"
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="PASS",
            response=response,
            found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 5: Handle COGNITIVE_ACTIVITY
    # ============================================================
    if intent == "cognitive_activity":
        response = """🧠 好的！我們來做一個簡單的記憶練習。

請記住這3個詞語：
🍎 蘋果
🚌 巴士
🔴 紅色

1分鐘後我會問你記不記得。準備好了嗎？"""
        
        # Record activity participation
        if metrics_collector:
            metrics_collector.record_activity_participation(user_id, "memory_exercise", True)
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="PASS",
            response=response,
            found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 6: Handle EMOTIONAL_SUPPORT (WITH CAREGIVER MEMORY!)
    # ============================================================
    if intent == "emotional_support":
        # Get name and calming phrase from caregiver memory
        name = "朋友"
        calming_phrase = None
        
        if caregiver_memory:
            name = caregiver_memory.get_name(user_id) or "朋友"
            calming_phrase = caregiver_memory.get_calming_phrase(user_id)
        
        # Extract mood from message or use default
        mood_score = 3  # Default neutral
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
        
        # Record mood metric
        if metrics_collector:
            metrics_collector.record_mood(user_id, mood_score)
            metrics_collector.record_interaction(user_id, intent, response)
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="PASS",
            response=response,
            found=True
        )
        return response
    
    # ============================================================
    # Step 7: Handle KNOWLEDGE_QA (HYBRID SEARCH)
    # ============================================================
    if intent == "knowledge_qa":
        result = hybrid_search(user_message)
        
        if not result:
            response = "小安暫時沒有這個資訊。請向照顧者或專業人士查詢。"
            found = False
            fallback_reason = "No information found in knowledge base"
        else:
            response = result
            found = True
            fallback_reason = None
        
        debug_logger.log_interaction(
            user_message=user_message,
            intent=intent,
            chunks=["Found relevant content"] if found else [],
            sources=["knowledge files"] if found else [],
            safety_level="PASS",
            response=response,
            found=found,
            fallback_reason=fallback_reason
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 8: Handle PERSONAL_MEMORY (WITH CAREGIVER MEMORY!)
    # ============================================================
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
            user_message=user_message,
            intent=intent,
            chunks=[],
            sources=[],
            safety_level="PASS",
            response=response,
            found=True
        )
        if metrics_collector:
            metrics_collector.record_interaction(user_id, intent, response)
        return response
    
    # ============================================================
    # Step 9: Handle UNKNOWN
    # ============================================================
    response = "😊 小安不太明白你的意思。你可以問我關於腦退化症的問題、藥物資訊、或者告訴我你想做記憶練習。"
    
    debug_logger.log_interaction(
        user_message=user_message,
        intent=intent,
        chunks=[],
        sources=[],
        safety_level="PASS",
        response=response,
        found=False,
        fallback_reason="Unknown intent"
    )
    if metrics_collector:
        metrics_collector.record_interaction(user_id, intent, response)
    return response


# ============================================================
# Test function
# ============================================================

def test_knowledge_tool():
    """Test the integrated knowledge tool."""
    print("\n" + "=" * 70)
    print("🧪 Testing YOUR Hybrid RAG (Semantic + Keyword)")
    print("=" * 70)
    print(f"📁 Components available: {COMPONENTS_AVAILABLE}")
    print(f"📁 Semantic search available: {SEMANTIC_AVAILABLE}")
    print(f"📁 Caregiver memory available: {CAREGIVER_MEMORY_AVAILABLE}")
    print(f"📁 Metrics available: {METRICS_AVAILABLE}")
    print("-" * 70)
    
    test_messages = [
        "什麼是腦退化症？",
        "我頭暈",
        "我可以吃兩粒藥嗎？",
        "提醒我吃藥",
        "我想做記憶練習",
        "我覺得好孤單",
        "我喜歡吃蘋果",
        "今天天氣如何？"
    ]
    
    print("\n📝 Processing test messages:\n")
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n{i}. 👤 用戶: {msg}")
        response = process_message(msg)
        print(f"   🤖 小安: {response[:100]}..." if len(response) > 100 else f"   🤖 小安: {response}")
        print("   " + "-" * 40)
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_knowledge_tool()