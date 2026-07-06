"""
Safety Handler for MCI Chatbot
Handles medication/diagnosis questions and safety escalation
"""

from datetime import datetime

class SafetyHandler:
    def __init__(self):
        # Emergency escalation contacts
        self.emergency_contacts = {
            "caregiver": "你的照顧者",
            "doctor": "你的醫生",
            "emergency": "999"
        }
    
    def handle_medication_or_diagnosis(self, message):
        """Handle medication/diagnosis questions with safe refusal."""
        return """⚠️ 小安不能提供用藥建議或診斷。

請注意：
1. 不要自行調整、增加或停止藥物
2. 請諮詢你的醫生、藥劑師或照顧者
3. 如有緊急情況，請立即聯絡照顧者或打 999

小安提提你：這裡只提供一般資訊，不是醫療建議。"""
    
    def handle_safety_sensitive(self, message):
        """Handle safety-sensitive situations with escalation."""
        return """⚠️ 如果你感到不適或有危險，請立即告訴你的照顧者或家人。

緊急情況：
- 如有生命危險，請立即打 999
- 如需要醫療協助，請讓照顧者陪你去看醫生
- 如感到暈眩、胸痛、呼吸困難，請不要延誤就醫

小安提提你：小安不能處理緊急情況，請優先尋求專業協助。"""
    
    def handle_dizziness(self, message):
        """Handle dizziness/headache complaints with escalation."""
        return """頭暈可能有多種原因。請注意：

1. 如果你有胸痛、說話不清、手腳麻痺，請立即去急症室
2. 請馬上告訴你的照顧者或家人
3. 如果沒有緊急症狀，請坐下休息，飲水

⚠️ 小安不能診斷你的情況。請讓照顧者或家人陪同你盡快看醫生。"""
    
    def is_safety_sensitive(self, message):
        """Check if message is safety sensitive."""
        msg = message.lower()
        sensitive_keywords = [
            "自殺", "傷害", "救命", "危險", "暈倒", "出血", "昏迷",
            "想死", "不想活", "死"
        ]
        return any(kw in msg for kw in sensitive_keywords)
    
    def is_medication_related(self, message):
        """Check if message is medication related."""
        msg = message.lower()
        med_keywords = [
            "藥", "劑量", "診斷", "停止吃藥", "治療", "吃多少", "食幾多",
            "停藥", "換藥", "加藥", "減藥"
        ]
        return any(kw in msg for kw in med_keywords)
    
    def is_health_complaint(self, message):
        """Check if message is a health complaint."""
        msg = message.lower()
        health_keywords = [
            "頭暈", "頭痛", "胸痛", "呼吸困難", "無力", "痛", "不適"
        ]
        return any(kw in msg for kw in health_keywords)


# Quick test
if __name__ == "__main__":
    handler = SafetyHandler()
    
    print("=" * 50)
    print("Safety Handler Test")
    print("=" * 50)
    
    test_messages = [
        "我頭暈",
        "我可以吃藥嗎？",
        "我胸口痛",
        "我想自殺",
        "什麼是腦退化症？"
    ]
    
    for msg in test_messages:
        if handler.is_safety_sensitive(msg):
            print(f"  {msg:<25} → SAFETY SENSITIVE")
        elif handler.is_medication_related(msg):
            print(f"  {msg:<25} → MEDICATION RELATED")
        elif handler.is_health_complaint(msg):
            print(f"  {msg:<25} → HEALTH COMPLAINT")
        else:
            print(f"  {msg:<25} → SAFE")
    
    print("=" * 50)
    print("\nSample Responses:")
    print("-" * 30)
    print("\n[Dizziness Response:]")
    print(handler.handle_dizziness("我頭暈"))
    
    print("\n[Medication Response:]")
    print(handler.handle_medication_or_diagnosis("我可以吃藥嗎？"))