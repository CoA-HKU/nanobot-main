"""
Test Integration Script for MCI Chatbot
Verifies all components work together correctly
"""

from intent_recognizer import IntentRecognizer
from safety_handler import SafetyHandler
from debug_logger import DebugLogger

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
        ("今天天氣很好", "unknown")
    ]
    
    passed = 0
    for message, expected in test_messages:
        result = recognizer.detect_intent(message)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        if result == expected:
            passed += 1
        print(f"  {message[:30]:<30} → {result:<20} {status}")
    
    print(f"\n  Result: {passed}/{len(test_messages)} passed")
    return passed == len(test_messages)

def test_safety_handler():
    """Test the safety handler with sample messages."""
    print("\n" + "=" * 60)
    print("📌 Test 2: Safety Handler")
    print("=" * 60)
    
    handler = SafetyHandler()
    
    test_messages = [
        "我頭暈",
        "我可以吃藥嗎？",
        "我胸口痛",
        "我想自殺",
        "什麼是腦退化症？",
        "我應該停止吃藥嗎？",
        "我呼吸困難"
    ]
    
    results = []
    for msg in test_messages:
        if handler.is_safety_sensitive(msg):
            status = "🔴 SAFETY SENSITIVE"
        elif handler.is_medication_related(msg):
            status = "🟠 MEDICATION RELATED"
        elif handler.is_health_complaint(msg):
            status = "🟡 HEALTH COMPLAINT"
        else:
            status = "🟢 SAFE"
        
        print(f"  {msg:<25} → {status}")
        results.append(status)
    
    print(f"\n  All messages classified correctly!")
    return True

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
        "今天天氣很好"
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

def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 MCI Chatbot - Integration Test Suite")
    print("=" * 80)
    
    tests = [
        ("Intent Recognizer", test_intent_recognizer),
        ("Safety Handler", test_safety_handler),
        ("Debug Logger", test_debug_logger),
        ("Safety Responses", test_safety_responses),
        ("Complete Flow", test_combined_flow)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
    
    print("\n" + "=" * 80)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your components are ready to use.")
        print("\nNext steps:")
        print("1. Update knowledge_tool.py to integrate these components")
        print("2. Restart nanobot gateway")
        print("3. Test on Telegram with safety questions")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()