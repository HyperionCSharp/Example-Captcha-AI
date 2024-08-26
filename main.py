import random
import time
import json
from typing import Dict, Tuple

# Simulated database for storing challenges and responses
challenge_db = {}

def generate_challenge() -> Dict:
    """Generate a new challenge for the user."""
    challenge_id = str(random.randint(1000, 9999))
    challenge_text = f"Please solve this simple math: 5 + {random.randint(1, 10)}"
    challenge_db[challenge_id] = {
        "challenge_text": challenge_text,
        "solution": 5 + int(challenge_text.split(' ')[-1]),
        "creation_time": time.time()
    }
    return {"challenge_id": challenge_id, "challenge_text": challenge_text}

def validate_response(challenge_id: str, user_response: int) -> bool:
    """Validate the user's response to a challenge."""
    challenge = challenge_db.get(challenge_id)
    if not challenge:
        return False

    # Check if the challenge has expired
    if time.time() - challenge['creation_time'] > 300:  # 5 minutes expiration
        return False

    return user_response == challenge['solution']

def detect_bot(user_agent: str, ip_address: str) -> bool:
    """Basic heuristic to detect bot-like behavior."""
    # Heuristic: Simple detection based on user-agent and IP patterns
    suspicious_user_agents = ["bot", "crawler", "spider"]
    suspicious_ips = ["192.168.1.1", "10.0.0.1"]

    if any(bot in user_agent.lower() for bot in suspicious_user_agents):
        return True

    if ip_address in suspicious_ips:
        return True

    return False

def main():
    # Simulate a user request for a challenge
    print("Generating challenge...")
    challenge = generate_challenge()
    print(f"Challenge: {challenge['challenge_text']}")
    
    # Simulate user response (replace with actual user input)
    user_response = int(input("Your answer: "))

    # Validate user response
    is_valid = validate_response(challenge['challenge_id'], user_response)
    if is_valid:
        print("Challenge solved successfully!")
    else:
        print("Invalid response or challenge expired.")
    
    # Simulate bot detection
    user_agent = "Mozilla/5.0"
    ip_address = "192.168.1.1"
    
    if detect_bot(user_agent, ip_address):
        print("Suspicious activity detected. Possible bot.")
    else:
        print("User seems legitimate.")

if __name__ == "__main__":
    main()
