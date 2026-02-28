#!/usr/bin/env python3
"""
Grok-powered Twitter Automation
- Learn your tweet style from past tweets
- Auto-generate tweets in your voice
- Auto-reply to mentions/DMs
"""
import os
import json
from datetime import datetime
from typing import List, Dict
import requests

class GrokTwitterBot:
    """
    Twitter bot powered by Grok API
    Learns your style and automates tweets/replies
    """
    
    def __init__(self):
        self.grok_api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        self.style_profile = self._load_style_profile()
        
    def _load_style_profile(self) -> Dict:
        """Load learned style profile"""
        profile_file = "/root/openclaw_data/lin/twitter_style_profile.json"
        if os.path.exists(profile_file):
            with open(profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "sample_tweets": [],
            "characteristics": {},
            "learned": False
        }
    
    def _save_style_profile(self):
        """Save style profile"""
        profile_file = "/root/openclaw_data/lin/twitter_style_profile.json"
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.style_profile, f, indent=2, ensure_ascii=False)
    
    def learn_from_tweets(self, tweets: List[str]):
        """
        Learn your writing style from past tweets
        
        Args:
            tweets: List of your past tweets
        """
        print(f"🧠 Learning style from {len(tweets)} tweets...")
        
        self.style_profile["sample_tweets"] = tweets
        
        # Analyze with Grok
        analysis_prompt = f"""以下のツイートから、この人の文体・特徴を分析してください：

{chr(10).join([f"- {tweet}" for tweet in tweets[:20]])}

分析項目：
1. 文章の長さ（短い/中/長い）
2. 口調（カジュアル/丁寧/専門的）
3. 絵文字の使用頻度
4. よく使う言い回し・フレーズ
5. トピックの傾向
6. ハッシュタグの使い方

JSON形式で回答してください。
"""
        
        # Call Grok API
        characteristics = self._call_grok_api(analysis_prompt, response_format="json")
        
        if characteristics:
            self.style_profile["characteristics"] = characteristics
            self.style_profile["learned"] = True
            self._save_style_profile()
            
            print("✅ Style learning complete!")
            print(f"Characteristics: {json.dumps(characteristics, indent=2, ensure_ascii=False)}")
        else:
            print("❌ Learning failed")
    
    def generate_tweet(self, topic: str = None, context: str = "") -> str:
        """
        Generate tweet in your style
        
        Args:
            topic: Optional topic to tweet about
            context: Additional context
        """
        if not self.style_profile["learned"]:
            return "[Error: Style not learned yet. Run learn_from_tweets() first]"
        
        prompt = f"""あなたは以下の文体・特徴を持つ人物です：

{json.dumps(self.style_profile['characteristics'], indent=2, ensure_ascii=False)}

過去のツイート例：
{chr(10).join([f"- {tweet}" for tweet in self.style_profile['sample_tweets'][:5]])}

"""
        
        if topic:
            prompt += f"\nトピック：{topic}\n"
        if context:
            prompt += f"\nコンテキスト：{context}\n"
        
        prompt += """
上記の文体・特徴を完全に模倣して、新しいツイートを1つ生成してください。
ツイート本文のみを出力してください（説明不要）。
280文字以内。
"""
        
        tweet = self._call_grok_api(prompt)
        return tweet.strip() if tweet else "[Generation failed]"
    
    def generate_reply(self, original_tweet: str, context: str = "") -> str:
        """
        Generate reply to a tweet in your style
        
        Args:
            original_tweet: Tweet to reply to
            context: Additional context about the conversation
        """
        if not self.style_profile["learned"]:
            return "[Error: Style not learned yet]"
        
        prompt = f"""あなたは以下の文体・特徴を持つ人物です：

{json.dumps(self.style_profile['characteristics'], indent=2, ensure_ascii=False)}

過去のツイート例：
{chr(10).join([f"- {tweet}" for tweet in self.style_profile['sample_tweets'][:5]])}

返信先のツイート：
「{original_tweet}」

{f"コンテキスト：{context}" if context else ""}

上記のツイートに対して、あなたの文体で自然な返信を生成してください。
返信文のみを出力してください（説明不要）。
280文字以内。
"""
        
        reply = self._call_grok_api(prompt)
        return reply.strip() if reply else "[Generation failed]"
    
    def _call_grok_api(self, prompt: str, response_format: str = "text") -> str:
        """
        Call Grok API (xAI)
        
        Args:
            prompt: Prompt text
            response_format: "text" or "json"
        """
        if not self.grok_api_key:
            return "[Grok API key not set]"
        
        try:
            # xAI API endpoint
            url = "https://api.x.ai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.grok_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "grok-beta",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            if response_format == "json":
                data["response_format"] = {"type": "json_object"}
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Grok API error: {e}")
            return None
    
    def fetch_your_tweets(self, username: str, count: int = 100) -> List[str]:
        """
        Fetch your past tweets (requires Twitter API)
        
        Args:
            username: Your Twitter username
            count: Number of tweets to fetch
        """
        if not self.twitter_api_key:
            print("❌ Twitter API credentials not set")
            print("Manual alternative: Export tweets from Twitter archive")
            return []
        
        # TODO: Implement Twitter API v2 fetching
        # For now, placeholder
        print(f"🔄 Fetching @{username}'s tweets...")
        print("⚠️  Twitter API integration pending")
        print("\n📋 Manual workaround:")
        print("1. Go to https://twitter.com/settings/download_your_data")
        print("2. Request archive")
        print("3. Extract tweets.js")
        print("4. Use import_from_archive() method")
        
        return []
    
    def import_from_archive(self, archive_file: str):
        """
        Import tweets from Twitter archive
        
        Args:
            archive_file: Path to tweets.js or tweets.json
        """
        print(f"📥 Importing from {archive_file}...")
        
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Twitter archive format: window.YTD.tweets.part0 = [...]
                if content.startswith("window.YTD"):
                    content = content.split("= ", 1)[1]
                
                data = json.loads(content)
            
            tweets = []
            for item in data:
                tweet_data = item.get("tweet", item)
                text = tweet_data.get("full_text") or tweet_data.get("text", "")
                if text and not text.startswith("RT @"):  # Skip retweets
                    tweets.append(text)
            
            print(f"✅ Imported {len(tweets)} tweets")
            
            # Learn from imported tweets
            if tweets:
                self.learn_from_tweets(tweets[:200])  # Use up to 200 tweets
            
            return tweets
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return []
    
    def manual_tweet_input(self, tweets: List[str]):
        """
        Manually input your tweets for learning
        
        Args:
            tweets: List of your past tweets
        """
        print(f"📝 Manually inputting {len(tweets)} tweets...")
        self.learn_from_tweets(tweets)
    
    def interactive_mode(self):
        """
        Interactive mode for testing
        """
        print("\n" + "="*70)
        print("🤖 Grok Twitter Bot - Interactive Mode")
        print("="*70)
        
        if not self.style_profile["learned"]:
            print("\n⚠️  Style not learned yet!")
            print("\nOptions:")
            print("1. Import from Twitter archive")
            print("2. Manually input sample tweets")
            print("3. Exit")
            
            choice = input("\nYour choice: ").strip()
            
            if choice == "1":
                file_path = input("Archive file path: ").strip()
                self.import_from_archive(file_path)
            elif choice == "2":
                print("\nEnter your past tweets (one per line, empty line to finish):")
                tweets = []
                while True:
                    tweet = input("> ").strip()
                    if not tweet:
                        break
                    tweets.append(tweet)
                
                if tweets:
                    self.learn_from_tweets(tweets)
            else:
                return
        
        # Main loop
        while True:
            print("\n" + "-"*70)
            print("What do you want to do?")
            print("1. Generate tweet")
            print("2. Generate reply")
            print("3. View style profile")
            print("4. Exit")
            
            choice = input("\nYour choice: ").strip()
            
            if choice == "1":
                topic = input("Topic (optional): ").strip()
                context = input("Context (optional): ").strip()
                
                print("\n🤖 Generating...")
                tweet = self.generate_tweet(topic or None, context)
                print(f"\n📝 Generated tweet:\n\n{tweet}\n")
                
            elif choice == "2":
                original = input("Tweet to reply to: ").strip()
                context = input("Context (optional): ").strip()
                
                print("\n🤖 Generating reply...")
                reply = self.generate_reply(original, context)
                print(f"\n💬 Generated reply:\n\n{reply}\n")
                
            elif choice == "3":
                print(f"\n📊 Style Profile:\n")
                print(json.dumps(self.style_profile["characteristics"], indent=2, ensure_ascii=False))
                
            elif choice == "4":
                break


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Grok Twitter Automation')
    subparsers = parser.add_subparsers(dest='command')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Interactive mode')
    
    # Learn from archive
    learn_parser = subparsers.add_parser('learn', help='Learn from Twitter archive')
    learn_parser.add_argument('archive_file', help='Path to tweets.js/json')
    
    # Generate tweet
    gen_parser = subparsers.add_parser('generate', help='Generate tweet')
    gen_parser.add_argument('--topic', help='Tweet topic')
    gen_parser.add_argument('--context', default='', help='Additional context')
    
    # Generate reply
    reply_parser = subparsers.add_parser('reply', help='Generate reply')
    reply_parser.add_argument('tweet', help='Original tweet to reply to')
    reply_parser.add_argument('--context', default='', help='Additional context')
    
    args = parser.parse_args()
    
    bot = GrokTwitterBot()
    
    if args.command == 'interactive' or not args.command:
        bot.interactive_mode()
        
    elif args.command == 'learn':
        bot.import_from_archive(args.archive_file)
        
    elif args.command == 'generate':
        tweet = bot.generate_tweet(args.topic, args.context)
        print(f"\n{tweet}\n")
        
    elif args.command == 'reply':
        reply = bot.generate_reply(args.tweet, args.context)
        print(f"\n{reply}\n")


if __name__ == "__main__":
    main()
