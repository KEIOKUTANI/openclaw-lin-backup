#!/usr/bin/env python3
"""
Sequential Debate - Progressive refinement through multiple AIs
Claude (draft) → GPT-4 (refine) → Gemini (counter) → Final synthesis
"""
import os
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

class SequentialDebate:
    """
    Progressive debate: each AI builds on/challenges previous responses
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
    
    def debate(self, question: str) -> dict:
        """
        Sequential debate process:
        1. Claude: Initial draft/proposal
        2. GPT-4: Refine and improve Claude's proposal
        3. Gemini: Counter-argue or propose alternative
        4. Synthesis: Final integrated answer
        """
        print(f"\n{'='*70}")
        print(f"🎭 Sequential Debate System")
        print(f"{'='*70}\n")
        print(f"📋 Question: {question}\n")
        
        # Stage 1: Claude's initial draft
        print(f"{'─'*70}")
        print(f"🧠 Stage 1: Claude's Initial Proposal")
        print(f"{'─'*70}\n")
        
        claude_response = self._claude_draft(question)
        print(f"{claude_response}\n")
        
        # Stage 2: GPT-4 refines Claude's proposal
        print(f"{'─'*70}")
        print(f"🚀 Stage 2: GPT-4's Refinement")
        print(f"{'─'*70}\n")
        
        gpt_response = self._gpt_refine(question, claude_response)
        print(f"{gpt_response}\n")
        
        # Stage 3: Gemini counter-argues or proposes alternative
        print(f"{'─'*70}")
        print(f"🌐 Stage 3: Gemini's Counter-Argument")
        print(f"{'─'*70}\n")
        
        gemini_response = self._gemini_counter(question, claude_response, gpt_response)
        print(f"{gemini_response}\n")
        
        # Stage 4: Final synthesis
        print(f"{'='*70}")
        print(f"📊 Final Synthesis")
        print(f"{'='*70}\n")
        
        synthesis = self._synthesize(question, claude_response, gpt_response, gemini_response)
        print(f"{synthesis}\n")
        
        return {
            "question": question,
            "claude_draft": claude_response,
            "gpt_refinement": gpt_response,
            "gemini_counter": gemini_response,
            "synthesis": synthesis
        }
    
    def _claude_draft(self, question: str) -> str:
        """Claude creates initial draft"""
        if not self.claude:
            return "[Claude unavailable]"
        
        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"""You are Claude, tasked with creating the INITIAL DRAFT response to this question.

Question: {question}

Provide a thoughtful, comprehensive initial answer. Be clear about your reasoning and any assumptions you're making.

Your draft will be refined by GPT-4 and challenged by Gemini, so focus on creating a solid foundation."""
                }]
            )
            return response.content[0].text
        except Exception as e:
            return f"[Claude error: {e}]"
    
    def _gpt_refine(self, question: str, claude_draft: str) -> str:
        """GPT-4 refines Claude's draft"""
        if not self.gpt:
            return "[GPT-4 unavailable]"
        
        try:
            response = self.gpt.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are GPT-4, tasked with REFINING and IMPROVING the initial draft."},
                    {"role": "user", "content": f"""Original question: {question}

Claude's initial draft:
{claude_draft}

Your task:
1. Identify strengths in Claude's response
2. Point out any weaknesses, gaps, or unclear points
3. Suggest improvements or additions
4. Provide a REFINED version that builds on Claude's foundation

Be constructive and specific in your refinement."""}
                ],
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[GPT-4 error: {e}]"
    
    def _gemini_counter(self, question: str, claude_draft: str, gpt_refinement: str) -> str:
        """Gemini provides counter-argument or alternative perspective"""
        if not self.gemini:
            return "[Gemini unavailable]"
        
        try:
            prompt = f"""You are Gemini, tasked with providing COUNTER-ARGUMENTS or ALTERNATIVE PERSPECTIVES.

Original question: {question}

Previous responses:

CLAUDE'S DRAFT:
{claude_draft}

GPT-4'S REFINEMENT:
{gpt_refinement}

Your task:
1. What are the potential FLAWS or RISKS in the previous responses?
2. What ALTERNATIVE approaches or perspectives are being missed?
3. Play devil's advocate - what could go wrong with their recommendations?
4. Propose a DIFFERENT or COMPLEMENTARY approach if appropriate

Be critical but constructive. Challenge assumptions and offer fresh perspectives."""
            
            response = self.gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Gemini error: {e}]"
    
    def _synthesize(self, question: str, claude: str, gpt: str, gemini: str) -> str:
        """Synthesize all perspectives into final answer"""
        
        synthesis = f"""## Final Integrated Answer

### Question
{question}

### Process Summary

**Stage 1 (Claude)**: Provided initial comprehensive draft
**Stage 2 (GPT-4)**: Refined and improved the draft  
**Stage 3 (Gemini)**: Offered counter-arguments and alternatives

---

### Integrated Recommendation

After considering all three perspectives:

#### What Claude Got Right
- [Key strengths from initial draft]

#### GPT-4's Key Improvements
- [Main refinements and additions]

#### Gemini's Valid Concerns
- [Important counter-points and risks to consider]

---

### Final Answer

[This would be synthesized by me (Lin/Claude) based on all inputs]

For now, please review the three perspectives above. Each offers valuable insights:
- **Claude**: Comprehensive foundation
- **GPT-4**: Refinements and improvements
- **Gemini**: Critical challenges and alternatives

The best path forward likely incorporates elements from all three viewpoints.

---

### Action Items
1. [Specific actionable step based on synthesis]
2. [Another action]
3. [Consideration of risks raised by Gemini]

"""
        return synthesis


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sequential Debate - Progressive multi-AI refinement')
    parser.add_argument('question', nargs='?', help='Question to debate')
    parser.add_argument('--example', action='store_true', help='Run example debate')
    
    args = parser.parse_args()
    
    debater = SequentialDebate()
    
    if args.example or not args.question:
        question = "Should I invest in AI startups now, or wait for the market to stabilize?"
    else:
        question = args.question
    
    result = debater.debate(question)
    
    # Save result
    import json
    from datetime import datetime
    
    output_dir = "/root/openclaw_data/lin/sequential_debates"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/debate_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Debate saved to: {output_file}\n")


if __name__ == "__main__":
    main()
