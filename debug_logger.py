"""
Debug Logger for MCI Chatbot
Logs all interactions for debugging and improvement
"""

import logging
import json
from datetime import datetime
from pathlib import Path

class DebugLogger:
    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = Path.home() / ".nanobot" / "logs"
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup main log file
        log_file = self.log_dir / "bot_debug.log"
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
        # Also create a JSON log for easier analysis
        self.json_log_file = self.log_dir / "interactions.jsonl"
        
        print(f"📝 Debug logs will be saved to: {self.log_dir}")
    
    def log_interaction(self, user_message, intent, chunks=None, sources=None, 
                        safety_level="PASS", response="", found=False, 
                        fallback_reason=None, retrieval_scores=None):
        """
        Log a complete interaction.
        
        Parameters:
        - user_message: What the user said
        - intent: Detected intent
        - chunks: Retrieved text chunks (list)
        - sources: Source filenames (list)
        - safety_level: PASS / FAIL / ESCALATE
        - response: Bot's response
        - found: Whether answer was found
        - fallback_reason: Why the bot couldn't answer
        - retrieval_scores: Relevance scores
        """
        
        # Log to text file (human readable)
        log_entry = f"""
        ========================================
        TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        USER: {user_message[:100]}{'...' if len(user_message) > 100 else ''}
        INTENT: {intent}
        CHUNKS: {len(chunks) if chunks else 0}
        SOURCES: {sources if sources else 'None'}
        SAFETY: {safety_level}
        FOUND: {found}
        FALLBACK: {fallback_reason if fallback_reason else 'N/A'}
        RESPONSE: {response[:200]}{'...' if len(response) > 200 else ''}
        ========================================
        """
        self.logger.info(log_entry)
        
        # Log to JSON file (for analysis)
        json_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "intent": intent,
            "chunks_count": len(chunks) if chunks else 0,
            "sources": sources if sources else [],
            "safety_level": safety_level,
            "found": found,
            "fallback_reason": fallback_reason,
            "response": response,
            "retrieval_scores": retrieval_scores if retrieval_scores else []
        }
        
        with open(self.json_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(json_entry, ensure_ascii=False) + '\n')
        
        # Also print to console for real-time debugging
        print(f"\n[DEBUG] Intent: {intent}")
        print(f"[DEBUG] Safety: {safety_level}")
        print(f"[DEBUG] Sources: {sources if sources else 'None'}")
        print(f"[DEBUG] Response: {response[:100]}...")
    
    def get_recent_logs(self, n=10):
        """Get the most recent n log entries."""
        try:
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_n = lines[-n:] if len(lines) > n else lines
                return [json.loads(line) for line in last_n if line.strip()]
        except:
            return []
    
    def get_stats(self):
        """Get statistics from the logs."""
        logs = self.get_recent_logs(1000)  # Get last 1000 entries
        
        if not logs:
            return {"error": "No logs found"}
        
        stats = {
            "total": len(logs),
            "intent_counts": {},
            "safety_failures": 0,
            "fallback_count": 0,
            "found_count": 0
        }
        
        for log in logs:
            intent = log.get("intent", "unknown")
            stats["intent_counts"][intent] = stats["intent_counts"].get(intent, 0) + 1
            
            if log.get("safety_level") == "FAIL":
                stats["safety_failures"] += 1
            
            if log.get("fallback_reason"):
                stats["fallback_count"] += 1
            
            if log.get("found"):
                stats["found_count"] += 1
        
        return stats


# Quick test
if __name__ == "__main__":
    logger = DebugLogger()
    
    # Test logging
    logger.log_interaction(
        user_message="什麼是腦退化症？",
        intent="knowledge_qa",
        chunks=["Chunk 1", "Chunk 2"],
        sources=["ha_dementia.txt", "medication.txt"],
        safety_level="PASS",
        response="腦退化症是一種大腦神經細胞病變導致的疾病。",
        found=True
    )
    
    print("✅ Test log created!")
    print(f"Recent logs: {logger.get_recent_logs(2)}")