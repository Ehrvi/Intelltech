#!/usr/bin/env python3
"""
OpenAI API Wrapper for Cost-Optimized Operations
Replaces expensive Manus operations with cheap OpenAI API calls
"""

import os
import json
from openai import OpenAI

class CheapOpenAIWrapper:
    """
    Wrapper for OpenAI API to replace expensive Manus operations
    Cost: ~$0.0001 per call (vs $0.20+ for Manus tools)
    """
    
    def __init__(self):
        self.client = OpenAI()  # Uses OPENAI_API_KEY env var
        self.model = "gpt-4o-mini"  # Cheapest, fastest model
        
    def research(self, query: str, max_tokens: int = 1000) -> dict:
        """
        Research/search replacement
        
        Instead of: Manus search tool (~20 credits)
        Use: OpenAI API (~0.01 credits)
        Savings: 2000x
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a research assistant. Provide accurate, concise information based on your knowledge."},
                    {"role": "user", "content": query}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'tokens': response.usage.total_tokens,
                'cost': response.usage.total_tokens * 0.0000002,  # Approximate
                'method': 'openai_api'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'openai_api'
            }
    
    def analyze_code(self, code: str, question: str, max_tokens: int = 2000) -> dict:
        """
        Code analysis replacement
        
        Instead of: Multiple file reads + shell commands
        Use: Single OpenAI API call
        """
        prompt = f"""Analyze this code and answer the question.

Code:
```
{code}
```

Question: {question}

Provide a detailed analysis."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.2
            )
            
            return {
                'success': True,
                'analysis': response.choices[0].message.content,
                'tokens': response.usage.total_tokens,
                'cost': response.usage.total_tokens * 0.0000002,
                'method': 'openai_api'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'openai_api'
            }
    
    def generate_text(self, prompt: str, max_tokens: int = 1500) -> dict:
        """
        Text generation replacement
        
        Instead of: Manus generate tool (~40 credits)
        Use: OpenAI API (~0.01 credits)
        Savings: 4000x
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return {
                'success': True,
                'text': response.choices[0].message.content,
                'tokens': response.usage.total_tokens,
                'cost': response.usage.total_tokens * 0.0000002,
                'method': 'openai_api'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'openai_api'
            }
    
    def batch_analyze(self, items: list, analysis_prompt: str) -> dict:
        """
        Batch analysis replacement
        
        Instead of: Manus map tool (100 credits per item)
        Use: Single OpenAI API call with all items
        Savings: 10000x+
        """
        prompt = f"""{analysis_prompt}

Items to analyze:
{json.dumps(items, indent=2)}

Provide analysis for each item in JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an analyst. Return results in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.2
            )
            
            return {
                'success': True,
                'results': response.choices[0].message.content,
                'tokens': response.usage.total_tokens,
                'cost': response.usage.total_tokens * 0.0000002,
                'method': 'openai_api',
                'items_processed': len(items)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'openai_api'
            }


# Global instance
openai_wrapper = CheapOpenAIWrapper()


# Convenience functions
def cheap_research(query: str) -> str:
    """Quick research using OpenAI API"""
    result = openai_wrapper.research(query)
    if result['success']:
        print(f"✅ Research complete (Cost: ${result['cost']:.6f}, {result['tokens']} tokens)")
        return result['content']
    else:
        print(f"❌ Research failed: {result['error']}")
        return None


def cheap_analyze(code: str, question: str) -> str:
    """Quick code analysis using OpenAI API"""
    result = openai_wrapper.analyze_code(code, question)
    if result['success']:
        print(f"✅ Analysis complete (Cost: ${result['cost']:.6f}, {result['tokens']} tokens)")
        return result['analysis']
    else:
        print(f"❌ Analysis failed: {result['error']}")
        return None


def cheap_generate(prompt: str) -> str:
    """Quick text generation using OpenAI API"""
    result = openai_wrapper.generate_text(prompt)
    if result['success']:
        print(f"✅ Generation complete (Cost: ${result['cost']:.6f}, {result['tokens']} tokens)")
        return result['text']
    else:
        print(f"❌ Generation failed: {result['error']}")
        return None


if __name__ == "__main__":
    print("Testing OpenAI Wrapper\n")
    
    # Test 1: Research
    print("Test 1: Research")
    result = cheap_research("What are the top 3 AI companies in 2026?")
    if result:
        print(f"Result: {result[:200]}...\n")
    
    # Test 2: Code analysis
    print("Test 2: Code Analysis")
    sample_code = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
    result = cheap_analyze(sample_code, "What is the time complexity?")
    if result:
        print(f"Result: {result[:200]}...\n")
    
    # Test 3: Text generation
    print("Test 3: Text Generation")
    result = cheap_generate("Write a haiku about AI optimization")
    if result:
        print(f"Result: {result}\n")
