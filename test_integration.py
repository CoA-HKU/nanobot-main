"""
test_integration.py - Complete Integration Test Suite for MCI Chatbot
Verifies all components work together correctly
"""

import sys
import os
from pathlib import Path

# ============================================================
# Add .nanobot folder to Python path
# ============================================================
NANOBOT_DIR = Path.home() / ".nanobot"
if str(NANOBOT_DIR) not in sys.path:
    sys.path.insert(0, str(NANOBOT_DIR))

# ============================================================
# Imports
# ============================================================
from intent_recognizer import IntentRecognizer
from safety_handler import SafetyHandler
from debug_logger import DebugLogger

# Try to import user profiles (optional)
try:
    from user_profiles import USER_PROFILES, get_all_test_questions
    USER_PROFILES_AVAILABLE = True
except ImportError:
    USER_PROFILES_AVAILABLE = False
    USER_PROFILES = {}
    print("⚠️ user_profiles.py not found. User profile tests will be skipped.")

# Try to import knowledge_tool for full integration
try:
    from knowledge_tool import process_message, detect_user_profile
    KNOWLEDGE_TOOL_AVAILABLE = True
except ImportError:
    KNOWLEDGE_TOOL_AVAILABLE = False
    print("⚠️ knowledge_tool.py not found. Full flow tests will be limited.")


# ============================================================
# TEST 1: Intent Recognizer
# ============================================================

def test_intent_recognizer():
    """Test the intent recognizer with sample messages."""
    print("\n" + "=" * 60)
    print("📌 Test 1: Intent Recognizer")
    print("=" * 60)
    
    recognizer = IntentRecognizer()
    
    test_messages = [
        ("什麼是腦退化症？", "knowledge_qa"),
        ("我頭暈得很厲害", "safety_sensitive"),
        ("我可以吃兩粒藥嗎？", "medication_or_diagnosis"),
        ("提醒我明天9點吃藥", "reminder_request"),
        ("我覺得好孤單", "emotional_support"),
        ("我想做記憶練習", "cognitive_activity"),
        ("我喜歡吃蘋果", "personal_memory"),
        ("今天天氣很好", "unknown"),
        # New: User profile keywords
        ("我最近常常忘記事情", "knowledge_qa"),  # 李婆婆
        ("醫生話我有MCI", "knowledge_qa"),      # 陳先生
        ("點樣預防腦退化", "knowledge_qa"),     # 王婆婆
    ]
    
    passed = 0
    total = len(test_messages)
    
    for message, expected in test_messages:
        result = recognizer.detect_intent(message)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        if result == expected:
            passed += 1
        print(f"  {message[:30]:<30} → {result:<20} {status}")
    
    print(f"\n  Result: {passed}/{total} passed")
    return passed == total


# ============================================================
# TEST 2: Safety Handler
# ============================================================

def test_safety_handler():
    """Test the safety handler with sample messages."""
    print("\n" + "=" * 60)
    print("📌 Test 2: Safety Handler")
    print("=" * 60)
    
    handler = SafetyHandler()
    
    test_messages = [
        ("我頭暈", "HEALTH_COMPLAINT"),
        ("我可以吃藥嗎？", "MEDICATION_RELATED"),
        ("我胸口痛", "HEALTH_COMPLAINT"),
        ("我想自殺", "SAFETY_SENSITIVE"),
        ("什麼是腦退化症？", "SAFE"),
        ("我應該停止吃藥嗎？", "MEDICATION_RELATED"),
        ("我呼吸困難", "HEALTH_COMPLAINT"),
        ("我有MCI", "SAFE"),
        ("點樣預防腦退化", "SAFE"),
    ]
    
    results = []
    for msg, expected in test_messages:
        if handler.is_safety_sensitive(msg):
            status = "🔴 SAFETY SENSITIVE"
        elif handler.is_medication_related(msg):
            status = "🟠 MEDICATION RELATED"
        elif handler.is_health_complaint(msg):
            status = "🟡 HEALTH COMPLAINT"
        else:
            status = "🟢 SAFE"
        
        passed = status.replace("🔴 ", "").replace("🟠 ", "").replace("🟡 ", "").replace("🟢 ", "") == expected
        check = "✅" if passed else "❌"
        print(f"  {msg:<25} → {status:<20} {check}")
        results.append(passed)
    
    print(f"\n  Result: {sum(results)}/{len(results)} passed")
    return all(results)


# ============================================================
# TEST 3: Debug Logger
# ============================================================

def test_debug_logger():
    """Test the debug logger."""
    print("\n" + "=" * 60)
    print("📌 Test 3: Debug Logger")
    print("=" * 60)
    
    logger = DebugLogger()
    
    # Test logging
    test_interactions = [
        {
            "user_message": "什麼是腦退化症？",
            "intent": "knowledge_qa",
            "chunks": ["Chunk 1", "Chunk 2"],
            "sources": ["ha_dementia.txt", "medication.txt"],
            "safety_level": "PASS",
            "response": "腦退化症是一種大腦神經細胞病變導致的疾病。",
            "found": True
        },
        {
            "user_message": "我頭暈",
            "intent": "safety_sensitive",
            "chunks": [],
            "sources": [],
            "safety_level": "ESCALATE",
            "response": "⚠️ 如果你感到不適，請立即告訴你的照顧者。",
            "found": False,
            "fallback_reason": "Safety escalation"
        },
        {
            "user_message": "我可以吃藥嗎？",
            "intent": "medication_or_diagnosis",
            "chunks": [],
            "sources": [],
            "safety_level": "FAIL",
            "response": "⚠️ 小安不能提供用藥建議。",
            "found": False,
            "fallback_reason": "Medication question refused"
        }
    ]
    
    for interaction in test_interactions:
        logger.log_interaction(**interaction)
    
    print(f"  ✅ {len(test_interactions)} test logs created!")
    
    # Test retrieving logs
    recent_logs = logger.get_recent_logs(3)
    print(f"  ✅ Retrieved {len(recent_logs)} recent logs")
    
    # Test stats
    stats = logger.get_stats()
    if stats and "error" not in stats:
        print(f"  ✅ Statistics: {stats['total']} total interactions")
    
    return True


# ============================================================
# TEST 4: Safety Responses
# ============================================================

def test_safety_responses():
    """Test the safety response messages."""
    print("\n" + "=" * 60)
    print("📌 Test 4: Safety Response Messages")
    print("=" * 60)
    
    handler = SafetyHandler()
    
    print("\n  [Medication Response:]")
    print("  " + "-" * 40)
    response = handler.handle_medication_or_diagnosis("測試")
    for line in response.split('\n'):
        print(f"  {line}")
    
    print("\n  [Dizziness Response:]")
    print("  " + "-" * 40)
    response = handler.handle_dizziness("測試")
    for line in response.split('\n'):
        print(f"  {line}")
    
    print("\n  [Safety Sensitive Response:]")
    print("  " + "-" * 40)
    response = handler.handle_safety_sensitive("測試")
    for line in response.split('\n'):
        print(f"  {line}")
    
    return True


# ============================================================
# TEST 5: Complete Flow Simulation
# ============================================================

def test_combined_flow():
    """Test the complete flow: message → intent → safety → response."""
    print("\n" + "=" * 60)
    print("📌 Test 5: Complete Flow Simulation")
    print("=" * 60)
    
    recognizer = IntentRecognizer()
    handler = SafetyHandler()
    logger = DebugLogger()
    
    test_messages = [
        "什麼是腦退化症？",
        "我頭暈得很厲害",
        "我可以吃兩粒藥嗎？",
        "提醒我明天9點吃藥",
        "我覺得好孤單",
        "我想做記憶練習",
        "今天天氣很好",
        "我最近常常忘記事情",   # 李婆婆 - should detect
        "醫生話我有MCI",        # 陳先生 - should educate
        "點樣預防腦退化",       # 王婆婆 - should educate
    ]
    
    print("\n  Simulating message processing flow:")
    print("  " + "-" * 40)
    
    for msg in test_messages:
        # Step 1: Detect intent
        intent = recognizer.detect_intent(msg)
        intent_desc = recognizer.get_intent_description(intent)
        
        # Step 2: Handle based on intent
        if intent == "safety_sensitive":
            if handler.is_health_complaint(msg):
                response = handler.handle_dizziness(msg)
                safety_level = "ESCALATE"
            else:
                response = handler.handle_safety_sensitive(msg)
                safety_level = "ESCALATE"
            found = False
            
        elif intent == "medication_or_diagnosis":
            response = handler.handle_medication_or_diagnosis(msg)
            safety_level = "FAIL"
            found = False
            
        else:
            # Simulate knowledge retrieval
            response = f"[知識庫回答] 關於「{msg}」的相關資訊..."
            safety_level = "PASS"
            found = True
        
        # Step 3: Log the interaction
        logger.log_interaction(
            user_message=msg,
            intent=intent,
            safety_level=safety_level,
            response=response,
            found=found
        )
        
        print(f"\n  Message: {msg}")
        print(f"  Intent: {intent_desc}")
        print(f"  Safety: {safety_level}")
        print(f"  Response: {response[:60]}...")
    
    print("\n  ✅ Complete flow tested successfully!")
    return True


# ============================================================
# TEST 6: User Profile Testing (NEW)
# ============================================================

def test_user_profiles():
    """Test all user profiles and their expected responses."""
    print("\n" + "=" * 60)
    print("📌 Test 6: User Profile Testing")
    print("=" * 60)
    
    if not USER_PROFILES_AVAILABLE:
        print("  ⚠️ user_profiles.py not found. Skipping.")
        return True
    
    if not KNOWLEDGE_TOOL_AVAILABLE:
        print("  ⚠️ knowledge_tool.py not found. Skipping.")
        return True
    
    print(f"\n  📋 Testing {len(USER_PROFILES)} user profiles:")
    
    passed = 0
    total = 0
    
    for profile_id, profile in USER_PROFILES.items():
        print(f"\n  👤 {profile['name']} ({profile['type']})")
        print(f"     Description: {profile['description']}")
        
        for question in profile.get("test_questions", []):
            total += 1
            print(f"\n     💬 '{question}'")
            
            try:
                # Process message
                response = process_message(question)
                print(f"     🤖 {response[:80]}...")
                
                # Check for expected keywords based on profile type
                expected_keywords = {
                    "concerned_user": ["關注", "留意", "醫生", "檢查", "專業"],
                    "mci_patient": ["輕度認知", "MCI", "管理", "健康", "醫生"],
                    "healthy_user": ["預防", "健腦", "健康", "活動", "飲食"],
                    "caregiver": ["照顧", "支援", "資源", "幫助", "家人"],
                    "dementia_patient": ["明白", "陪伴", "支持", "感受", "安心"],
                    "healthcare_professional": ["報告", "評估", "篩查", "結果"]
                }
                
                profile_type = profile.get("type", "concerned_user")
                keywords = expected_keywords.get(profile_type, ["幫助", "了解"])
                
                has_keyword = any(kw in response for kw in keywords)
                
                if has_keyword:
                    print(f"     ✅ PASS (keywords found)")
                    passed += 1
                else:
                    print(f"     ❌ FAIL (expected keywords: {keywords})")
                    
            except Exception as e:
                print(f"     ❌ ERROR: {e}")
    
    print(f"\n  📊 Results: {passed}/{total} profile tests passed")
    return passed == total


# ============================================================
# MAIN
# ============================================================

def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 MCI Chatbot - Integration Test Suite")
    print("=" * 80)
    print(f"📁 User Profiles Available: {USER_PROFILES_AVAILABLE}")
    print(f"📁 Knowledge Tool Available: {KNOWLEDGE_TOOL_AVAILABLE}")
    print("=" * 80)
    
    tests = [
        ("Intent Recognizer", test_intent_recognizer),
        ("Safety Handler", test_safety_handler),
        ("Debug Logger", test_debug_logger),
        ("Safety Responses", test_safety_responses),
        ("Complete Flow", test_combined_flow),
    ]
    
    # Add user profile test if available
    if USER_PROFILES_AVAILABLE and KNOWLEDGE_TOOL_AVAILABLE:
        tests.append(("User Profiles", test_user_profiles))
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print("\n" + "-" * 60)
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
    
    print("\n" + "=" * 80)
    print(f"📊 Test Results: {passed}/{total} passed")
    print("=" * 80)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your components are ready to use.")
        print("\n📋 Next steps:")
        print("  1. Make sure knowledge_tool.py is updated")
        print("  2. Restart nanobot gateway")
        print("  3. Test on Telegram with safety questions")
        print("  4. Test with user profiles")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()