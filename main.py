import random
import time
import json
from typing import Dict, Tuple, List
import re
import hashlib
from datetime import datetime, timedelta

# Simulated database for storing challenges and responses
challenge_db = {}

def generate_challenge() -> Dict:
    """Generate a new challenge for the user."""
    challenge_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
    operations = ['+', '-', '*']
    operation = random.choice(operations)
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    challenge_text = f"Please solve this math problem: {num1} {operation} {num2}"
    
    if operation == '+':
        solution = num1 + num2
    elif operation == '-':
        solution = num1 - num2
    else:
        solution = num1 * num2
    
    challenge_db[challenge_id] = {
        "challenge_text": challenge_text,
        "solution": solution,
        "creation_time": datetime.now(),
        "attempts": 0
    }
    return {"challenge_id": challenge_id, "challenge_text": challenge_text}

def validate_response(challenge_id: str, user_response: int) -> Tuple[bool, str]:
    """Validate the user's response to a challenge."""
    challenge = challenge_db.get(challenge_id)
    if not challenge:
        return False, "Challenge not found"

    # Check if the challenge has expired
    if datetime.now() - challenge['creation_time'] > timedelta(minutes=5):
        return False, "Challenge expired"

    challenge['attempts'] += 1
    if challenge['attempts'] > 3:
        return False, "Too many attempts"

    if user_response == challenge['solution']:
        return True, "Correct answer"
    else:
        return False, "Incorrect answer"

def detect_bot(user_agent: str, ip_address: str, request_history: List[Dict]) -> bool:
    """Advanced heuristic to detect bot-like behavior."""
    suspicious_user_agents = ["bot", "crawler", "spider", "scraper"]
    suspicious_ips = ["192.168.1.1", "10.0.0.1"]

    # Check user agent
    if any(bot in user_agent.lower() for bot in suspicious_user_agents):
        return True

    # Check IP address
    if ip_address in suspicious_ips:
        return True

    # Check request frequency
    if len(request_history) > 10:
        time_diff = request_history[-1]['timestamp'] - request_history[0]['timestamp']
        if time_diff.total_seconds() < 5:  # More than 10 requests in 5 seconds
            return True

    # Check for consistent request patterns
    if len(request_history) > 5:
        intervals = [
            (request_history[i+1]['timestamp'] - request_history[i]['timestamp']).total_seconds()
            for i in range(len(request_history) - 1)
        ]
        if len(set(intervals)) == 1:  # All intervals are the same
            return True

    return False

def rate_limit(ip_address: str, request_history: List[Dict]) -> bool:
    """Implement rate limiting."""
    if len(request_history) < 100:
        return False
    
    time_diff = request_history[-1]['timestamp'] - request_history[-100]['timestamp']
    if time_diff.total_seconds() < 60:  # More than 100 requests per minute
        return True
    
    return False

def main():
    request_history = []

    while True:
        print("\n1. Generate Challenge")
        print("2. Solve Challenge")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Simulate a user request for a challenge
            print("Generating challenge...")
            challenge = generate_challenge()
            print(f"Challenge: {challenge['challenge_text']}")
            print(f"Challenge ID: {challenge['challenge_id']}")
        
        elif choice == '2':
            challenge_id = input("Enter the challenge ID: ")
            user_response = int(input("Your answer: "))

            # Validate user response
            is_valid, message = validate_response(challenge_id, user_response)
            print(message)

            # Simulate bot detection and rate limiting
            user_agent = "Mozilla/5.0"
            ip_address = "127.0.0.1"
            
            request_history.append({
                'timestamp': datetime.now(),
                'ip_address': ip_address,
                'user_agent': user_agent
            })

            if detect_bot(user_agent, ip_address, request_history):
                print("Suspicious activity detected. Possible bot.")
            elif rate_limit(ip_address, request_history):
                print("Rate limit exceeded. Please try again later.")
            else:
                print("Request processed successfully.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
