"""
insights.py - Smart Insights & Alerts for MCI Chatbot
Generates alerts and summaries from metrics data
"""

from datetime import datetime, timedelta
from metrics import MetricsCollector

class InsightGenerator:
    def __init__(self):
        self.collector = MetricsCollector()
    
    def get_alerts(self, user_id, days=3):
        """Generate alerts for a user"""
        user_id = str(user_id)
        alerts = []
        metrics = self.collector.get_user_metrics(user_id, days=30)
        
        # Alert 1: Mood drop
        mood_history = metrics.get("mood_history", [])
        if len(mood_history) >= 3:
            recent_moods = [m["score"] for m in mood_history[-3:]]
            if recent_moods and all(m < 3 for m in recent_moods):
                alerts.append({
                    "level": "warning",
                    "icon": "⚠️",
                    "message": f"情緒連續3天偏低 (平均 {sum(recent_moods)/len(recent_moods):.1f})。建議多陪伴溝通。"
                })
        
        # Alert 2: Cognitive decline
        cognitive_history = metrics.get("cognitive_history", [])
        if len(cognitive_history) >= 4:
            recent = [c["score"] for c in cognitive_history[-4:]]
            older = [c["score"] for c in cognitive_history[-8:-4]]
            if older and recent:
                recent_avg = sum(recent) / len(recent)
                older_avg = sum(older) / len(older)
                if older_avg - recent_avg > 1.0:
                    alerts.append({
                        "level": "warning",
                        "icon": "🧠",
                        "message": f"認知訓練表現下降 (從 {older_avg:.1f} 降至 {recent_avg:.1f})。建議增加訓練頻率。"
                    })
        
        # Alert 3: Low engagement
        interactions = [
            i for i in self.collector.data["interactions"]
            if i["user_id"] == user_id and 
            datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(days=2)
        ]
        if len(interactions) == 0:
            alerts.append({
                "level": "info",
                "icon": "💬",
                "message": "過去2天沒有互動。試試主動關心患者。"
            })
        
        # Alert 4: Medication adherence
        adherence = metrics.get("medication_adherence")
        if adherence is not None and adherence < 0.7:
            alerts.append({
                "level": "warning",
                "icon": "💊",
                "message": f"用藥依從率偏低 ({int(adherence*100)}%)。請確認患者是否按時服藥。"
            })
        
        # Alert 5: Positive reinforcement
        activity_history = metrics.get("activity_history", [])
        recent_activities = [
            a for a in activity_history
            if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(days=3)
        ]
        participated = sum(1 for a in recent_activities if a.get("participated", False))
        if participated >= 2:
            alerts.append({
                "level": "success",
                "icon": "🌟",
                "message": f"過去3天參與了 {participated} 次活動。積極參與對認知健康有益！"
            })
        
        return alerts
    
    def get_summary(self, user_id):
        """Generate a summary report for a user"""
        user_id = str(user_id)
        metrics = self.collector.get_user_metrics(user_id, days=30)
        
        summary = {
            "user_id": user_id,
            "period": "過去30天",
            "total_interactions": metrics["total_interactions"],
            "avg_mood": metrics.get("avg_mood"),
            "avg_cognitive": metrics.get("avg_cognitive"),
            "medication_adherence": metrics.get("medication_adherence"),
            "alerts": self.get_alerts(user_id)
        }
        
        # Add trend descriptions
        if summary["avg_mood"]:
            if summary["avg_mood"] >= 4:
                summary["mood_status"] = "良好 😊"
            elif summary["avg_mood"] >= 3:
                summary["mood_status"] = "穩定 😐"
            else:
                summary["mood_status"] = "需要關注 😟"
        
        if summary["avg_cognitive"]:
            if summary["avg_cognitive"] >= 3:
                summary["cognitive_status"] = "良好 🎯"
            elif summary["avg_cognitive"] >= 2:
                summary["cognitive_status"] = "穩定 📊"
            else:
                summary["cognitive_status"] = "需要關注 📉"
        
        if summary["medication_adherence"] is not None:
            if summary["medication_adherence"] >= 0.8:
                summary["medication_status"] = "良好 ✅"
            elif summary["medication_adherence"] >= 0.6:
                summary["medication_status"] = "注意 ⚠️"
            else:
                summary["medication_status"] = "需要跟進 ❌"
        
        return summary


# Quick test
def test_insights():
    print("\n" + "=" * 60)
    print("🧪 Testing Insights Generator")
    print("=" * 60)
    
    insights = InsightGenerator()
    user_id = "test_user"
    
    # Test alerts
    alerts = insights.get_alerts(user_id)
    print(f"\n📋 Alerts for {user_id}:")
    if alerts:
        for alert in alerts:
            print(f"  {alert['icon']} [{alert['level']}] {alert['message']}")
    else:
        print("  ✅ No alerts — everything looks good!")
    
    # Test summary
    summary = insights.get_summary(user_id)
    print(f"\n📊 Summary for {user_id}:")
    for key, value in summary.items():
        if key != "alerts":
            print(f"  {key}: {value}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test_insights()