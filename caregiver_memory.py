"""
caregiver_memory.py - Caregiver-Authorable Personal Memory
Allows caregivers to store patient information, routines, preferences
"""

import json
import os
from pathlib import Path
from datetime import datetime

class CaregiverMemory:
    def __init__(self, memory_file=None):
        """Initialize caregiver memory store"""
        if memory_file is None:
            memory_file = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "caregiver_memory.json"
        
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
        print(f"📝 Caregiver Memory loaded: {self.memory_file}")
    
    def _load(self):
        """Load memory from JSON file"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        """Save memory to JSON file"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user_profile(self, user_id):
        """Get full profile for a user"""
        user_id = str(user_id)
        return self.data.get(user_id, {})
    
    def get_memory(self, user_id, key, default=None):
        """Get a specific memory value"""
        user_id = str(user_id)
        return self.data.get(user_id, {}).get(key, default)
    
    def set_memory(self, user_id, key, value):
        """Set a specific memory value"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id][key] = value
        self.data[user_id]["last_updated"] = datetime.now().isoformat()
        self._save()
        return True
    
    def add_preference(self, user_id, preference):
        """Add a preference (e.g., '喜歡聽粵曲')"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        if "preferences" not in self.data[user_id]:
            self.data[user_id]["preferences"] = []
        if preference not in self.data[user_id]["preferences"]:
            self.data[user_id]["preferences"].append(preference)
            self._save()
        return True
    
    def add_routine(self, user_id, routine):
        """Add a daily routine (e.g., '9:00 吃多奈哌齊')"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        if "routines" not in self.data[user_id]:
            self.data[user_id]["routines"] = []
        self.data[user_id]["routines"].append(routine)
        self._save()
        return True
    
    def set_emergency_contact(self, user_id, name, phone):
        """Set emergency contact"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id]["emergency_contact"] = {
            "name": name,
            "phone": phone
        }
        self._save()
        return True
    
    def set_calming_phrase(self, user_id, phrase):
        """Set a calming phrase for this user"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {}
        if "calming_phrases" not in self.data[user_id]:
            self.data[user_id]["calming_phrases"] = []
        self.data[user_id]["calming_phrases"].append(phrase)
        self._save()
        return True
    
    def get_name(self, user_id):
        """Get user's preferred name"""
        return self.get_memory(user_id, "name", "朋友")
    
    def get_calming_phrase(self, user_id):
        """Get a random calming phrase for the user"""
        phrases = self.get_memory(user_id, "calming_phrases", [])
        if phrases:
            import random
            return random.choice(phrases)
        return None


# ============================================================
# Quick Test
# ============================================================

def test_caregiver_memory():
    """Test caregiver memory functionality"""
    print("\n" + "=" * 60)
    print("🧪 Testing Caregiver Memory")
    print("=" * 60)
    
    memory = CaregiverMemory()
    
    # Test user
    user_id = "test_user_123"
    
    # Set profile
    memory.set_memory(user_id, "name", "陳婆婆")
    memory.set_memory(user_id, "age", "72")
    memory.set_memory(user_id, "diagnosis", "輕度認知障礙")
    
    # Add preferences
    memory.add_preference(user_id, "喜歡聽粵曲")
    memory.add_preference(user_id, "不喜歡苦瓜")
    
    # Add routines
    memory.add_routine(user_id, "7:00 起床")
    memory.add_routine(user_id, "8:00 早餐")
    memory.add_routine(user_id, "9:00 吃藥 (多奈哌齊)")
    
    # Set emergency contact
    memory.set_emergency_contact(user_id, "陳先生", "9876-5432")
    
    # Add calming phrases
    memory.set_calming_phrase(user_id, "一切安好，慢慢來")
    memory.set_calming_phrase(user_id, "你做得很好，不用擔心")
    
    # Get profile
    profile = memory.get_user_profile(user_id)
    
    print("\n📋 User Profile:")
    print("-" * 40)
    for key, value in profile.items():
        if key != "last_updated":
            print(f"  {key}: {value}")
    print(f"  last_updated: {profile.get('last_updated', 'N/A')}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test_caregiver_memory()