"""
user_profiles.py - User Profiles for Testing and Routing
Each profile represents a real user type with specific needs
"""

# ============================================================
# USER PROFILE DEFINITIONS
# ============================================================

USER_PROFILES = {
    "concerned_lee": {
        "name": "李婆婆",
        "age": 68,
        "type": "concerned_user",
        "description": "Worried about memory, wants reassurance",
        "keywords": ["忘記", "記性", "忘事", "記唔到"],
        "intent": "screening_intent",
        "test_questions": [
            "我最近常常忘記事情",
            "我記性差咗好多",
            "我成日都唔記得鎖門"
        ],
        "expected_response_type": "detect_then_screen"
    },
    
    "mci_chan": {
        "name": "陳先生",
        "age": 72,
        "type": "mci_patient",
        "description": "Diagnosed with MCI, wants education",
        "keywords": ["MCI", "輕度認知", "認知障礙", "醫生話"],
        "intent": "knowledge_intent",
        "test_questions": [
            "醫生話我有MCI",
            "輕度認知障礙係咩",
            "我點樣管理MCI"
        ],
        "expected_response_type": "educate"
    },
    
    "healthy_wong": {
        "name": "王婆婆",
        "age": 62,
        "type": "healthy_user",
        "description": "Healthy, wants prevention tips",
        "keywords": ["預防", "保健", "健腦", "點樣預防"],
        "intent": "knowledge_intent",
        "test_questions": [
            "點樣預防腦退化",
            "有咩方法可以健腦",
            "點樣保持腦健康"
        ],
        "expected_response_type": "educate_prevention"
    },
    
    "caregiver_cheung": {
        "name": "張女士",
        "age": 45,
        "type": "caregiver",
        "description": "Caring for mother with dementia, needs resources",
        "keywords": ["照顧", "媽媽", "屋企人", "點樣照顧"],
        "intent": "emotional_intent",
        "test_questions": [
            "我媽媽有認知障礙",
            "點樣照顧認知障礙長者",
            "有咩社區資源"
        ],
        "expected_response_type": "support_and_resources"
    },
    
    "dementia_lam": {
        "name": "林先生",
        "age": 78,
        "type": "dementia_patient",
        "description": "Early dementia, needs gentle engagement",
        "keywords": ["唔想麻煩人", "孤單", "鬱悶", "唔開心"],
        "intent": "emotional_intent",
        "test_questions": [
            "我唔想麻煩人",
            "我覺得好孤單",
            "我成日唔開心"
        ],
        "expected_response_type": "gentle_support"
    },
    
    "doctor_chiu": {
        "name": "趙醫生",
        "age": 50,
        "type": "healthcare_professional",
        "description": "Geriatrician, wants screening reports",
        "keywords": ["報告", "篩查結果", "評估"],
        "intent": "report_intent",
        "test_questions": [
            "給我篩查報告",
            "顯示評估結果",
            "這個用戶的篩查結果"
        ],
        "expected_response_type": "generate_report"
    }
}


# ============================================================
# PROFILE MAPPING FUNCTIONS
# ============================================================

def get_profile_by_keyword(keyword):
    """Find which profile matches a keyword"""
    keyword_lower = keyword.lower()
    for profile_id, profile in USER_PROFILES.items():
        for kw in profile["keywords"]:
            if kw in keyword_lower:
                return profile_id, profile
    return None, None


def get_profile_by_intent(intent):
    """Find which profile matches an intent"""
    for profile_id, profile in USER_PROFILES.items():
        if profile["intent"] == intent:
            return profile_id, profile
    return None, None


def get_all_test_questions():
    """Get all test questions from all profiles"""
    questions = []
    for profile in USER_PROFILES.values():
        for q in profile["test_questions"]:
            questions.append({
                "question": q,
                "profile": profile["name"],
                "expected": profile["expected_response_type"]
            })
    return questions


# ============================================================
# TEST FUNCTION
# ============================================================

def test_user_profiles():
    """Test that all profiles are loaded correctly"""
    print("\n" + "=" * 60)
    print("🧪 Testing User Profiles")
    print("=" * 60)
    
    print(f"\n📋 Loaded {len(USER_PROFILES)} profiles:")
    for profile_id, profile in USER_PROFILES.items():
        print(f"  - {profile['name']} ({profile['type']})")
        print(f"    Keywords: {', '.join(profile['keywords'][:3])}...")
    
    print(f"\n📋 Total test questions: {len(get_all_test_questions())}")
    
    print("\n" + "=" * 60)
    print("✅ User profiles loaded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    test_user_profiles()