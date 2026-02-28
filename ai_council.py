#!/usr/bin/env python3
"""
AI Council - Multi-AI Debate System
Orchestrates Claude, GPT-4, and Gemini to provide diverse perspectives
"""
import os
import sys
from typing import List, Dict
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

class AICouncil:
    """
    Orchestrates multiple AI models for collaborative problem-solving
    """
    
    def __init__(self):
        # Initialize API clients
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
        
        if self.anthropic_key:
            self.claude = Anthropic(api_key=self.anthropic_key)
        else:
            self.claude = None
            
        if self.openai_key:
            self.gpt = OpenAI(api_key=self.openai_key)
        else:
            self.gpt = None
            
        if self.google_key:
            genai.configure(api_key=self.google_key)
            self.gemini = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini = None
    
    def _call_claude(self, prompt: str, context: List[Dict] = None) -> str:
        """Call Claude API"""
        if not self.claude:
            return "[Claude unavailable - API key not set]"
        
        try:
            messages = []
            if context:
                for msg in context:
                    messages.append({
                        "role": "user" if msg["role"] == "user" else "assistant",
                        "content": msg["content"]
                    })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=messages,
                system="You are Claude, known for logical, careful, and detailed analysis. Provide your perspective on this topic."
            )
            
            return response.content[0].text
        except Exception as e:
            return f"[Claude error: {str(e)}]"
    
    def _call_gpt4(self, prompt: str, context: List[Dict] = None) -> str:
        """Call GPT-4 API"""
        if not self.gpt:
            return "[GPT-4 unavailable - API key not set]"
        
        try:
            messages = [
                {"role": "system", "content": "You are GPT-4, known for creative, bold, and innovative thinking. Provide your perspective on this topic."}
            ]
            
            if context:
                messages.extend(context)
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.gpt.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"[GPT-4 error: {str(e)}]"
    
    def _call_gemini(self, prompt: str, context: List[Dict] = None) -> str:
        """Call Gemini API"""
        if not self.gemini:
            return "[Gemini unavailable - API key not set]"
        
        try:
            # Build context string
            full_prompt = "You are Gemini, known for balanced, practical, and data-driven analysis. Provide your perspective on this topic.\n\n"
            
            if context:
                full_prompt += "Previous discussion:\n"
                for msg in context:
                    role = msg["role"]
                    content = msg["content"]
                    full_prompt += f"{role}: {content}\n\n"
            
            full_prompt += f"Question: {prompt}"
            
            response = self.gemini.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"[Gemini error: {str(e)}]"
    
    def debate(self, topic: str, rounds: int = 2) -> Dict:
        """
        Conduct multi-round debate between AIs
        
        Args:
            topic: Question or topic to debate
            rounds: Number of discussion rounds (default: 2)
        
        Returns:
            Dict with all responses and final synthesis
        """
        print(f"\n{'='*70}")
        print(f"🎭 AI Council Convened")
        print(f"{'='*70}")
        print(f"\n📋 Topic: {topic}\n")
        
        context = []
        all_responses = {"claude": [], "gpt4": [], "gemini": []}
        
        for round_num in range(rounds):
            print(f"\n{'─'*70}")
            print(f"🔄 Round {round_num + 1}/{rounds}")
            print(f"{'─'*70}\n")
            
            # Claude's turn
            print("💭 Claude thinking...")
            claude_prompt = topic if round_num == 0 else f"Given the previous discussion, what's your updated perspective on: {topic}"
            claude_response = self._call_claude(claude_prompt, context)
            all_responses["claude"].append(claude_response)
            context.append({"role": "Claude", "content": claude_response})
            print(f"\n🧠 Claude says:\n{claude_response}\n")
            
            # GPT-4's turn
            print("💭 GPT-4 thinking...")
            gpt_prompt = topic if round_num == 0 else f"Given Claude's perspective and the discussion so far, what do you think about: {topic}"
            gpt_response = self._call_gpt4(gpt_prompt, [{"role": "user", "content": f"Claude said: {claude_response}"}] if round_num == 0 else context)
            all_responses["gpt4"].append(gpt_response)
            context.append({"role": "GPT-4", "content": gpt_response})
            print(f"\n🚀 GPT-4 says:\n{gpt_response}\n")
            
            # Gemini's turn
            print("💭 Gemini thinking...")
            gemini_prompt = topic if round_num == 0 else f"Given both Claude's and GPT-4's perspectives, what's your view on: {topic}"
            gemini_response = self._call_gemini(gemini_prompt, context)
            all_responses["gemini"].append(gemini_response)
            context.append({"role": "Gemini", "content": gemini_response})
            print(f"\n🌐 Gemini says:\n{gemini_response}\n")
        
        # Lin synthesizes
        print(f"\n{'='*70}")
        print(f"📊 Lin's Synthesis")
        print(f"{'='*70}\n")
        
        synthesis = self._synthesize(topic, all_responses)
        print(synthesis)
        
        print(f"\n{'='*70}")
        print(f"✅ Council Adjourned")
        print(f"{'='*70}\n")
        
        return {
            "topic": topic,
            "rounds": rounds,
            "responses": all_responses,
            "synthesis": synthesis
        }
    
    def _synthesize(self, topic: str, responses: Dict) -> str:
        """
        Synthesize multiple AI responses into coherent summary
        """
        synthesis = f"## Summary of AI Council Discussion on:\n### {topic}\n\n"
        
        synthesis += "### Key Perspectives:\n\n"
        synthesis += "**Claude** (Logical & Careful):\n"
        synthesis += f"- {responses['claude'][-1][:200]}...\n\n"
        
        synthesis += "**GPT-4** (Creative & Bold):\n"
        synthesis += f"- {responses['gpt4'][-1][:200]}...\n\n"
        
        synthesis += "**Gemini** (Balanced & Practical):\n"
        synthesis += f"- {responses['gemini'][-1][:200]}...\n\n"
        
        synthesis += "### Consensus Points:\n"
        synthesis += "- [Analysis of agreement between models]\n\n"
        
        synthesis += "### Divergent Views:\n"
        synthesis += "- [Analysis of disagreements and different perspectives]\n\n"
        
        synthesis += "### Lin's Recommendation:\n"
        synthesis += "Based on the council's input, consider:\n"
        synthesis += "1. [Action item]\n"
        synthesis += "2. [Action item]\n"
        synthesis += "3. [Action item]\n"
        
        return synthesis


def main():
    """Command-line interface for AI Council"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Council - Multi-AI Debate System')
    parser.add_argument('topic', nargs='?', help='Topic or question to discuss')
    parser.add_argument('--rounds', type=int, default=2, help='Number of debate rounds (default: 2)')
    parser.add_argument('--example', action='store_true', help='Run example debate')
    
    args = parser.parse_args()
    
    council = AICouncil()
    
    if args.example or not args.topic:
        print("\n💡 Running example debate...\n")
        topic = "Should I start a new business venture now, or wait until market conditions improve?"
    else:
        topic = args.topic
    
    result = council.debate(topic, rounds=args.rounds)
    
    # Save to file
    output_file = f"/root/openclaw_data/lin/council_debates/debate_{len(os.listdir('/root/openclaw_data/lin/council_debates') if os.path.exists('/root/openclaw_data/lin/council_debates') else 0) + 1}.md"
    os.makedirs("/root/openclaw_data/lin/council_debates", exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(f"# AI Council Debate\n\n")
        f.write(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Topic**: {topic}\n")
        f.write(f"**Rounds**: {args.rounds}\n\n")
        f.write(result['synthesis'])
    
    print(f"\n💾 Debate saved to: {output_file}\n")


if __name__ == "__main__":
    main()
