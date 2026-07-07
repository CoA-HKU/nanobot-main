"""
metrics.py - Data Collection for MCI Chatbot
Stores interaction metrics in JSON for dashboard insights
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

class MetricsCollector:
    def __init__(self, metrics_file=None):
        if metrics_file is None:
            metrics_file = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "metrics.json"
        
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self):
        """Load metrics from JSON file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"interactions": [], "users": {}}
        return {"interactions": [], "users": {}}
    
    def _save(self):
        """Save metrics to JSON file"""
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def record_interaction(self, user_id, intent, response, metadata=None):
        """
        Record a single interaction
        """
        user_id = str(user_id)
        timestamp = datetime.now().isoformat()
        
        interaction = {
            "timestamp": timestamp,
            "user_id": user_id,
            "intent": intent,
            "response_length": len(response) if response else 0,
            "metadata": metadata or {}
        }
        
        self.data["interactions"].append(interaction)
        self._save()
        return True
    
    def record_mood(self, user_id, mood_score):
        """Record mood score (1-5)"""
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {}
        if "mood_history" not in self.data["users"][user_id]:
            self.data["users"][user_id]["mood_history"] = []
        
        self.data["users"][user_id]["mood_history"].append({
            "timestamp": datetime.now().isoformat(),
            "score": mood_score
        })
        self._save()
    
    def record_cognitive_score(self, user_id, score, exercise_type="memory"):
        """Record cognitive exercise score"""
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {}
        if "cognitive_history" not in self.data["users"][user_id]:
            self.data["users"][user_id]["cognitive_history"] = []
        
        self.data["users"][user_id]["cognitive_history"].append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "exercise_type": exercise_type
        })
        self._save()
    
    def record_medication(self, user_id, taken):
        """Record medication adherence"""
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {}
        if "medication_history" not in self.data["users"][user_id]:
            self.data["users"][user_id]["medication_history"] = []
        
        self.data["users"][user_id]["medication_history"].append({
            "timestamp": datetime.now().isoformat(),
            "taken": taken
        })
        self._save()
    
    def record_activity_participation(self, user_id, activity_type, participated):
        """Record activity participation"""
        user_id = str(user_id)
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = {}
        if "activity_history" not in self.data["users"][user_id]:
            self.data["users"][user_id]["activity_history"] = []
        
        self.data["users"][user_id]["activity_history"].append({
            "timestamp": datetime.now().isoformat(),
            "activity_type": activity_type,
            "participated": participated
        })
        self._save()
    
    def get_user_metrics(self, user_id, days=7):
        """Get aggregated metrics for a user"""
        user_id = str(user_id)
        cutoff = datetime.now() - timedelta(days=days)
        
        # Filter interactions
        interactions = [
            i for i in self.data["interactions"]
            if i["user_id"] == user_id and datetime.fromisoformat(i["timestamp"]) > cutoff
        ]
        
        # Get user-specific data
        user_data = self.data["users"].get(user_id, {})
        
        # Calculate metrics
        metrics = {
            "total_interactions": len(interactions),
            "mood_history": user_data.get("mood_history", [])[-30:],
            "cognitive_history": user_data.get("cognitive_history", [])[-30:],
            "medication_history": user_data.get("medication_history", [])[-30:],
            "activity_history": user_data.get("activity_history", [])[-30:],
            "intent_counts": {},
            "avg_mood": None,
            "avg_cognitive": None,
            "medication_adherence": None
        }
        
        # Intent counts
        for i in interactions:
            intent = i.get("intent", "unknown")
            metrics["intent_counts"][intent] = metrics["intent_counts"].get(intent, 0) + 1
        
        # Average mood
        moods = [m["score"] for m in metrics["mood_history"]]
        if moods:
            metrics["avg_mood"] = sum(moods) / len(moods)
        
        # Average cognitive
        cognitive_scores = [c["score"] for c in metrics["cognitive_history"]]
        if cognitive_scores:
            metrics["avg_cognitive"] = sum(cognitive_scores) / len(cognitive_scores)
        
        # Medication adherence
        meds = metrics["medication_history"]
        if meds:
            taken = sum(1 for m in meds if m["taken"])
            metrics["medication_adherence"] = taken / len(meds)
        
        return metrics
    
    def get_all_users(self):
        """Get list of all users"""
        users = set()
        for i in self.data["interactions"]:
            users.add(i.get("user_id"))
        for u in self.data["users"].keys():
            users.add(u)
        return sorted(list(users))


# Quick test
def test_metrics():
    print("\n" + "=" * 60)
    print("🧪 Testing Metrics Collector")
    print("=" * 60)
    
    collector = MetricsCollector()
    user_id = "test_user"
    
    # Record some test data
    collector.record_interaction(user_id, "knowledge_qa", "Test response")
    collector.record_mood(user_id, 4)
    collector.record_mood(user_id, 5)
    collector.record_cognitive_score(user_id, 3, "memory")
    collector.record_cognitive_score(user_id, 2, "memory")
    collector.record_medication(user_id, True)
    collector.record_medication(user_id, False)
    collector.record_activity_participation(user_id, "memory_exercise", True)
    
    # Get metrics
    metrics = collector.get_user_metrics(user_id, days=7)
    print(f"\n📊 Metrics for {user_id}:")
    print(f"  Total interactions: {metrics['total_interactions']}")
    print(f"  Average mood: {metrics['avg_mood']}")
    print(f"  Average cognitive score: {metrics['avg_cognitive']}")
    print(f"  Medication adherence: {metrics['medication_adherence']}")
    print(f"  Intent counts: {metrics['intent_counts']}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test_metrics()