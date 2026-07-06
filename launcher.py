"""
launcher.py - Menu to run all bot services and tests
"""

import subprocess
import os
import sys
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_screen()
    print("\n" + "=" * 60)
    print("🤖 MCI Chatbot - Launcher")
    print("=" * 60)
    print("\n📋 Available Options:")
    print("  1. 🚀 Start Bot (Gateway + Reminder)")
    print("  2. 🧪 Run All Tests (Quick)")
    print("  3. 🔍 Test Intent Recognition")
    print("  4. 📊 Run Full Integration Test")
    print("  5. 🛡️ Test Safety Features")
    print("  6. 📝 View Recent Logs")
    print("  7. 🔄 Restart Bot")
    print("  8. 🛑 Stop Bot")
    print("  9. ❌ Exit")
    print("-" * 60)

def run_command(cmd, description):
    """Run a command and show output."""
    print(f"\n▶️ {description}...")
    print("-" * 40)
    result = subprocess.run(cmd, shell=True, cwd=Path.home() / ".nanobot", capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("⚠️", result.stderr)
    
    return result.returncode == 0

def start_bot():
    """Start the bot using start_bot.cmd."""
    print("\n🚀 Starting bot...")
    bot_cmd = Path.home() / "Desktop" / "nanobot-main-main5" / "nanobot-main" / "start_bot.cmd"
    
    if bot_cmd.exists():
        subprocess.Popen([str(bot_cmd)], shell=True)
        print("✅ Bot started! Check the new windows.")
        print("📱 Now test on Telegram!")
    else:
        print(f"❌ start_bot.cmd not found at: {bot_cmd}")
        print("   Please update the path if needed.")
    
    input("\nPress Enter to continue...")

def run_tests():
    """Run all quick tests."""
    print("\n🧪 Running quick tests...")
    print("-" * 40)
    
    tests = [
        ("intent_recognizer", "from intent_recognizer import IntentRecognizer; print('✅ Intent Recognizer OK')"),
        ("safety_handler", "from safety_handler import SafetyHandler; print('✅ Safety Handler OK')"),
        ("debug_logger", "from debug_logger import DebugLogger; print('✅ Debug Logger OK')"),
    ]
    
    passed = 0
    for name, cmd in tests:
        result = subprocess.run(f'py -3.14 -c "{cmd}"', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {name}: PASSED")
            passed += 1
        else:
            print(f"  ❌ {name}: FAILED")
            if result.stderr:
                print(f"     {result.stderr.strip()}")
    
    print(f"\n📊 {passed}/{len(tests)} tests passed")
    input("\nPress Enter to continue...")

def test_intent():
    """Interactive intent test."""
    print("\n🔍 Testing Intent Recognition...")
    print("-" * 40)
    
    test_messages = [
        "什麼是腦退化症？",
        "我頭暈",
        "我可以吃兩粒藥嗎？",
        "提醒我吃藥",
        "我想做記憶練習",
    ]
    
    try:
        sys.path.insert(0, str(Path.home() / ".nanobot"))
        from intent_recognizer import IntentRecognizer
        from knowledge_tool import process_message
        
        recognizer = IntentRecognizer()
        
        for msg in test_messages:
            intent = recognizer.detect_intent(msg)
            desc = recognizer.get_intent_description(intent)
            print(f"\n👤 {msg}")
            print(f"🤖 Intent: {desc}")
            
            # Quick response preview
            response = process_message(msg)
            print(f"💬 {response[:80]}...")
        
        print("\n✅ Intent test complete!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def run_integration():
    """Run full integration test."""
    print("\n📊 Running Integration Test...")
    run_command("py -3.14 test_integration.py", "Integration Test")
    input("\nPress Enter to continue...")

def test_safety():
    """Test safety features."""
    print("\n🛡️ Testing Safety Features...")
    print("-" * 40)
    
    test_cases = [
        ("我頭暈", "Should refuse with escalation"),
        ("我可以吃藥嗎？", "Should refuse medication"),
        ("什麼是腦退化症？", "Should answer from knowledge"),
    ]
    
    try:
        sys.path.insert(0, str(Path.home() / ".nanobot"))
        from knowledge_tool import process_message
        
        for msg, expected in test_cases:
            response = process_message(msg)
            has_refusal = any(kw in response for kw in ["不能", "不可以", "請諮詢", "⚠️"])
            status = "✅" if has_refusal or "暫時沒有" in response else "❌"
            print(f"  {status} {msg}")
            print(f"     → {response[:60]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to continue...")

def view_logs():
    """View debug logs."""
    print("\n📝 Debug Logs:")
    print("-" * 40)
    
    log_file = Path.home() / ".nanobot" / "logs" / "bot_debug.log"
    
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Show last 30 lines
            lines = content.strip().split('\n')
            if len(lines) > 30:
                print("... (showing last 30 lines) ...\n")
                for line in lines[-30:]:
                    print(line)
            else:
                print(content)
    else:
        print("📭 No logs found yet.")
        print("   Send some messages to your bot first!")
    
    input("\nPress Enter to continue...")

def restart_bot():
    """Restart the bot."""
    print("\n🔄 Restarting bot...")
    # Kill existing processes
    subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Gateway*\" 2>nul", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Reminder*\" 2>nul", shell=True, capture_output=True)
    import time
    time.sleep(1)
    start_bot()

def stop_bot():
    """Stop the bot."""
    print("\n🛑 Stopping bot...")
    subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Gateway*\" 2>nul", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq Reminder*\" 2>nul", shell=True, capture_output=True)
    print("✅ Bot stopped!")
    input("\nPress Enter to continue...")

def main():
    menu_actions = {
        '1': start_bot,
        '2': run_tests,
        '3': test_intent,
        '4': run_integration,
        '5': test_safety,
        '6': view_logs,
        '7': restart_bot,
        '8': stop_bot,
    }
    
    while True:
        print_menu()
        choice = input("\n👉 Select an option (1-9): ").strip()
        
        if choice == '9':
            print("\n👋 Goodbye!")
            break
        
        if choice in menu_actions:
            menu_actions[choice]()
        else:
            print("\n❌ Invalid option! Please try 1-9.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()