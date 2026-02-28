#!/usr/bin/env python3
"""
Personality Learner - Automatically learn user's personality, habits, and preferences
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class PersonalityLearner:
    """
    Learn and adapt to user's personality through conversation
    """
    
    def __init__(self, profile_file="/root/openclaw_data/lin/user_profile_deep.json"):
        self.profile_file = profile_file
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load existing profile or create new one"""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "personality": {
                "communication_style": {},
                "decision_making_patterns": {},
                "emotional_triggers": {},
                "humor_preferences": {}
            },
            "interests": {
                "topics_excited_about": [],
                "topics_bored_by": [],
                "learning_goals": []
            },
            "habits": {
                "daily_routines": {},
                "work_patterns": {},
                "energy_levels": {}
            },
            "preferences": {
                "response_style": "balanced",  # concise, detailed, balanced
                "tone": "professional",  # casual, professional, friendly
                "formality": "medium"  # low, medium, high
            },
            "conversation_history": [],
            "observations": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_profile(self):
        """Save profile to file"""
        self.profile["last_updated"] = datetime.now().isoformat()
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, indent=2, ensure_ascii=False)
    
    def observe(self, observation: str, category: str = "general"):
        """
        Record an observation about the user
        
        Args:
            observation: What you observed
            category: Type of observation (personality, habit, preference, etc.)
        """
        entry = {
            "observation": observation,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "confidence": "medium"  # low, medium, high
        }
        
        self.profile["observations"].append(entry)
        self._save_profile()
        
        print(f"📝 Observation recorded: {observation}")
    
    def track_conversation(self, user_message: str, context: str = ""):
        """
        Track conversation for pattern analysis
        
        Args:
            user_message: User's message
            context: Context or topic of conversation
        """
        entry = {
            "message": user_message,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "length": len(user_message.split()),
            "sentiment": self._analyze_sentiment(user_message)
        }
        
        self.profile["conversation_history"].append(entry)
        
        # Keep only last 1000 conversations
        if len(self.profile["conversation_history"]) > 1000:
            self.profile["conversation_history"] = self.profile["conversation_history"][-1000:]
        
        self._save_profile()
    
    def _analyze_sentiment(self, text: str) -> str:
        """
        Simple sentiment analysis
        (In production, would use proper NLP)
        """
        positive_words = ["good", "great", "awesome", "love", "excellent", "perfect"]
        negative_words = ["bad", "terrible", "hate", "worst", "awful", "horrible"]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def learn_from_interaction(self, user_message: str, user_reaction: str = None):
        """
        Learn from user interaction
        
        Args:
            user_message: What user said
            user_reaction: How user reacted (satisfied, frustrated, etc.)
        """
        # Analyze message characteristics
        length = len(user_message.split())
        
        # Update communication style preferences
        if length < 20:
            self.profile["personality"]["communication_style"]["prefers_concise"] = \
                self.profile["personality"]["communication_style"].get("prefers_concise", 0) + 1
        elif length > 50:
            self.profile["personality"]["communication_style"]["prefers_detailed"] = \
                self.profile["personality"]["communication_style"].get("prefers_detailed", 0) + 1
        
        # Learn from reaction
        if user_reaction:
            if user_reaction in ["satisfied", "happy", "good"]:
                # User liked the response - remember this pattern
                pass
            elif user_reaction in ["frustrated", "confused", "bad"]:
                # User didn't like it - avoid this pattern
                pass
        
        self._save_profile()
    
    def add_interest(self, topic: str, sentiment: str = "excited"):
        """
        Add a topic to user's interests
        
        Args:
            topic: Topic name
            sentiment: excited, bored, neutral
        """
        if sentiment == "excited":
            if topic not in self.profile["interests"]["topics_excited_about"]:
                self.profile["interests"]["topics_excited_about"].append({
                    "topic": topic,
                    "added": datetime.now().isoformat(),
                    "strength": 1
                })
        elif sentiment == "bored":
            if topic not in self.profile["interests"]["topics_bored_by"]:
                self.profile["interests"]["topics_bored_by"].append(topic)
        
        self._save_profile()
        print(f"✅ Interest recorded: {topic} ({sentiment})")
    
    def get_communication_insights(self) -> Dict:
        """
        Analyze conversation patterns
        """
        if not self.profile["conversation_history"]:
            return {"message": "Not enough data yet"}
        
        history = self.profile["conversation_history"]
        recent = history[-100:]  # Last 100 conversations
        
        # Average message length
        avg_length = sum(h["length"] for h in recent) / len(recent)
        
        # Sentiment distribution
        sentiments = [h["sentiment"] for h in recent]
        sentiment_counts = {
            "positive": sentiments.count("positive"),
            "neutral": sentiments.count("neutral"),
            "negative": sentiments.count("negative")
        }
        
        # Time of day patterns
        hour_counts = defaultdict(int)
        for h in recent:
            hour = datetime.fromisoformat(h["timestamp"]).hour
            hour_counts[hour] += 1
        
        most_active_hour = max(hour_counts, key=hour_counts.get) if hour_counts else None
        
        return {
            "average_message_length": round(avg_length, 1),
            "preferred_length": "concise" if avg_length < 20 else "detailed" if avg_length > 50 else "medium",
            "sentiment_distribution": sentiment_counts,
            "most_active_hour": most_active_hour,
            "total_conversations": len(history),
            "recent_activity": len(recent)
        }
    
    def get_adaptive_response_style(self) -> str:
        """
        Determine how Lin should respond based on learned preferences
        """
        insights = self.get_communication_insights()
        
        if insights.get("preferred_length") == "concise":
            return "Keep responses brief and to the point"
        elif insights.get("preferred_length") == "detailed":
            return "Provide detailed, comprehensive responses"
        else:
            return "Balance between detail and brevity"
    
    def generate_summary(self) -> str:
        """
        Generate summary of what Lin knows about user
        """
        insights = self.get_communication_insights()
        
        summary = "## What Lin Knows About You\n\n"
        
        # Communication style
        summary += "### Communication Style\n"
        summary += f"- Preferred message length: {insights.get('preferred_length', 'unknown')}\n"
        summary += f"- Total conversations: {insights.get('total_conversations', 0)}\n\n"
        
        # Interests
        summary += "### Interests\n"
        if self.profile["interests"]["topics_excited_about"]:
            summary += "You're excited about:\n"
            for interest in self.profile["interests"]["topics_excited_about"][:5]:
                topic = interest if isinstance(interest, str) else interest.get("topic", "Unknown")
                summary += f"- {topic}\n"
        else:
            summary += "- No specific interests recorded yet\n"
        summary += "\n"
        
        # Recent observations
        summary += "### Recent Observations\n"
        recent_obs = self.profile["observations"][-5:]
        if recent_obs:
            for obs in recent_obs:
                summary += f"- {obs['observation']} ({obs.get('category', 'general')})\n"
        else:
            summary += "- No observations yet\n"
        
        summary += f"\n**Last updated**: {self.profile['last_updated']}\n"
        
        return summary


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Personality Learner - Track user preferences')
    subparsers = parser.add_subparsers(dest='command')
    
    # Observe
    obs_parser = subparsers.add_parser('observe', help='Record an observation')
    obs_parser.add_argument('observation', help='What you observed')
    obs_parser.add_argument('--category', default='general')
    
    # Add interest
    interest_parser = subparsers.add_parser('interest', help='Add an interest')
    interest_parser.add_argument('topic', help='Topic name')
    interest_parser.add_argument('--sentiment', choices=['excited', 'bored', 'neutral'], default='excited')
    
    # Summary
    subparsers.add_parser('summary', help='Show profile summary')
    
    # Insights
    subparsers.add_parser('insights', help='Show communication insights')
    
    args = parser.parse_args()
    
    learner = PersonalityLearner()
    
    if args.command == 'observe':
        learner.observe(args.observation, args.category)
    elif args.command == 'interest':
        learner.add_interest(args.topic, args.sentiment)
    elif args.command == 'summary':
        print(learner.generate_summary())
    elif args.command == 'insights':
        insights = learner.get_communication_insights()
        print("\n📊 Communication Insights:\n")
        for key, value in insights.items():
            print(f"{key}: {value}")
        print()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
