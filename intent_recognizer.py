"""
Intent Recognizer for MCI Chatbot
Classifies user messages into 8 categories based on keywords
"""

class IntentRecognizer:
    def __init__(self):
        # Priority 1: Safety (highest priority - always check first)
        self.safety_keywords = [
            "自殺", "傷害", "救命", "危險", "暈倒", "出血", "昏迷", 
            "想死", "不想活", "死", "緊急", "流血", "休克", "昏倒",
            "頭暈", "頭痛", "胸痛", "呼吸困難", "無力", "麻痺"
        ]
        
        # Priority 2: Medication/Diagnosis 
        # Check for medication DECISIONS (taking, stopping, dosage)
        self.medication_keywords = [
            "劑量", "診斷", "停止吃藥", "吃多少", "食幾多",
            "停藥", "換藥", "加藥", "減藥",
        ]
        
        # Priority 3: Knowledge QA
        # Note: This comes AFTER medication decisions, so "副作用" won't override
        self.knowledge_keywords = [
            # Question words
            "什麼是", "什麼叫", "定義", "症狀", "原因", "如何", "怎樣",
            "什麼時候", "為什麼", "怎麼", "有哪些", "是什麼",
            "何謂", "何為", "哪一些", "哪種", "邊種",
            
            # Dementia-related terms
            "腦退化", "認知障礙", "失智", "癡呆", "阿茲海默", "血管性",
            "預防", "治療", "照護", "照顧", "護理",
            "飲食", "運動", "副作用", "風險",
            "成因", "類型", "分期", "診斷", "檢查",
            "行為", "情緒", "語言",  # REMOVED: "記憶", "認知" (moved to activity)
            "生活", "日常", "居家", "社區", "機構",
            "資源", "服務", "支援", "幫助", "協助",
            "患者", "病人", "長者", "老人", "家屬",
            "徵兆", "早期", "晚期", "進程", "惡化",
            "活動", "訓練", "復健", "用藥",
            
            # Medication names
            "多奈哌齊", "卡巴拉汀", "美金剛", "安理申", "艾斯能",
            "donepezil", "rivastigmine", "memantine"
        ]
        
        # Priority 4: Reminders
        self.reminder_keywords = [
            "提醒", "記得", "通知", "幫我記", "記住", "定時", "準時",
            "鬧鐘", "提示", "日程", "行程"
        ]
        
        # Priority 5: Emotional Support
        self.emotional_keywords = [
            "難過", "孤單", "擔心", "害怕", "壓力", "焦慮", "緊張",
            "不安", "失落", "沮喪", "煩惱", "傷心", "憂鬱",
            "抑鬱", "孤獨", "無助", "絕望", "痛苦", "疲累"
        ]
        
        # Priority 6: Cognitive Activities
        # MOVED: "記憶", "認知" here so they take priority over knowledge
        self.activity_keywords = [
            "記憶", "認知",  # <-- MOVED from knowledge
            "練習", "遊戲", "活動", "訓練", "測試", "挑戰",
            "腦力", "回憶", "動腦", "思考", "專注",
            "觀察", "反應", "計算", "命名", "分類"
        ]
        
        # Priority 7: Personal Memory
        self.personal_keywords = [
            "我喜歡", "我討厭", "我的", "我常", "我最", "家人", "朋友",
            "我叫", "我係", "我是", "我住", "我識", "我鍾意"
        ]

    def detect_intent(self, message):
        """
        Detect the intent of the user message.
        Returns: one of 8 intent categories
        """
        if not message or message.strip() == "":
            return "unknown"
        
        msg = message.lower().strip()
        
        # Priority 1: Safety (ALWAYS check first - most critical)
        for keyword in self.safety_keywords:
            if keyword in msg:
                return "safety_sensitive"
        
        # Priority 2: Medication/Diagnosis
        # Detect medication DECISION questions
        # Pattern 1: "吃" + "藥" + "多少/幾多"
        if "藥" in msg:
            # Check if it's a medication decision question
            decision_patterns = ["多少", "幾多", "可以", "應該", "能夠"]
            if any(p in msg for p in decision_patterns):
                return "medication_or_diagnosis"
            
            # Check if it's a dosage/stop question
            if "劑量" in msg or "停止" in msg or "停" in msg or "換" in msg or "加" in msg or "減" in msg:
                return "medication_or_diagnosis"
        
        # Check specific medication keywords
        for keyword in self.medication_keywords:
            if keyword in msg:
                return "medication_or_diagnosis"
        
        # Priority 3: Knowledge QA
        for keyword in self.knowledge_keywords:
            if keyword in msg:
                return "knowledge_qa"
        
        # Priority 4: Reminders
        for keyword in self.reminder_keywords:
            if keyword in msg:
                return "reminder_request"
        
        # Priority 5: Emotional Support
        for keyword in self.emotional_keywords:
            if keyword in msg:
                return "emotional_support"
        
        # Priority 6: Cognitive Activities
        for keyword in self.activity_keywords:
            if keyword in msg:
                return "cognitive_activity"
        
        # Priority 7: Personal Memory
        for keyword in self.personal_keywords:
            if keyword in msg:
                return "personal_memory"
        
        # Default: Unknown
        return "unknown"

    def get_intent_description(self, intent):
        """Get a human-readable description of the intent."""
        descriptions = {
            "knowledge_qa": "知識問答",
            "personal_memory": "個人記憶", 
            "reminder_request": "提醒請求",
            "cognitive_activity": "認知活動",
            "emotional_support": "情緒支援",
            "safety_sensitive": "⚠️ 安全敏感",
            "medication_or_diagnosis": "⚠️ 藥物/診斷",
            "unknown": "未知"
        }
        return descriptions.get(intent, "未知")


# Quick test function
def test_intent_recognizer():
    """Test the intent recognizer with sample messages."""
    recognizer = IntentRecognizer()
    
    test_messages = [
        ("什麼是腦退化症？", "knowledge_qa"),
        ("腦退化症預防", "knowledge_qa"),
        ("腦退化症治療", "knowledge_qa"),
        ("如何照顧腦退化症患者", "knowledge_qa"),
        ("我頭暈得很厲害", "safety_sensitive"),
        ("我可以吃兩粒藥嗎？", "medication_or_diagnosis"),
        ("多奈哌齊的副作用", "knowledge_qa"),
        ("提醒我明天9點吃藥", "reminder_request"),
        ("我覺得好孤單", "emotional_support"),
        ("我想做記憶練習", "cognitive_activity"),
        ("我喜歡吃蘋果", "personal_memory"),
        ("今天天氣很好", "unknown")
    ]
    
    print("=" * 60)
    print("🧪 Intent Recognizer Test Results")
    print("=" * 60)
    
    passed = 0
    for message, expected in test_messages:
        result = recognizer.detect_intent(message)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        if result == expected:
            passed += 1
        print(f"  {message[:35]:<35} → {result:<20} {status}")
    
    print("=" * 60)
    print(f"📊 Result: {passed}/{len(test_messages)} passed")
    print("=" * 60)


if __name__ == "__main__":
    test_intent_recognizer()