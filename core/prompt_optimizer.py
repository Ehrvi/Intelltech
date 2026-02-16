#!/usr/bin/env python3
"""
Prompt Optimizer for Cost Reduction
Reduces token usage through prompt compression and optimization

Target: 30-50% token reduction
Quality: Maintain semantic meaning
"""

import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime


class PromptOptimizer:
    """Optimizes prompts to reduce token usage while maintaining quality"""
    
    def __init__(self, rules: Optional[Dict] = None):
        """
        Initialize PromptOptimizer
        
        Args:
            rules: Optional dict with optimization rules
        """
        self.rules = rules or {
            'max_history_tokens': 500,
            'max_prompt_tokens': 1000,
            'compression_level': 'medium',  # 'low', 'medium', 'high'
            'preserve_examples': True,
            'use_templates': True
        }
        
        # Template directory
        self.templates_dir = Path("/home/ubuntu/manus_global_knowledge/templates")
        self.templates_dir.mkdir(exist_ok=True)
        
        # Tracking
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.log_file = self.base_path / "logs" / "prompt_optimization.jsonl"
        self.log_file.parent.mkdir(exist_ok=True)
    
    def compress_prompt(self, prompt_text: str) -> str:
        """
        Compress prompt by removing unnecessary words
        
        Args:
            prompt_text: Original prompt
            
        Returns:
            Compressed prompt
        """
        if not prompt_text:
            return prompt_text
        
        compressed = prompt_text
        
        # Remove extra whitespace
        compressed = re.sub(r'\s+', ' ', compressed)
        compressed = compressed.strip()
        
        # Remove filler words (if compression level is medium or high)
        if self.rules['compression_level'] in ['medium', 'high']:
            fillers = [
                r'\b(please|kindly|just|simply|actually|basically|literally)\b',
                r'\b(I think|I believe|in my opinion|it seems)\b',
                r'\b(very|really|quite|somewhat|rather)\b'
            ]
            for filler_pattern in fillers:
                compressed = re.sub(filler_pattern, '', compressed, flags=re.IGNORECASE)
        
        # Remove redundant phrases (if compression level is high)
        if self.rules['compression_level'] == 'high':
            redundant = [
                (r'in order to', 'to'),
                (r'due to the fact that', 'because'),
                (r'at this point in time', 'now'),
                (r'for the purpose of', 'for'),
                (r'in the event that', 'if')
            ]
            for old, new in redundant:
                compressed = re.sub(old, new, compressed, flags=re.IGNORECASE)
        
        # Clean up extra spaces again
        compressed = re.sub(r'\s+', ' ', compressed).strip()
        
        return compressed
    
    def summarize_history(self, chat_history: List[Dict[str, str]], max_tokens: Optional[int] = None) -> str:
        """
        Summarize chat history to reduce tokens
        
        Args:
            chat_history: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens for summary (approximate)
            
        Returns:
            Summarized history as string
        """
        if not chat_history:
            return ""
        
        max_tokens = max_tokens or self.rules['max_history_tokens']
        
        # Simple heuristic: 1 token ≈ 4 characters
        max_chars = max_tokens * 4
        
        # Keep only recent messages that fit in budget
        summary_parts = []
        current_chars = 0
        
        for message in reversed(chat_history):
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            message_text = f"{role}: {content}"
            message_chars = len(message_text)
            
            if current_chars + message_chars > max_chars:
                # Truncate this message
                remaining_chars = max_chars - current_chars
                if remaining_chars > 50:  # Only include if meaningful
                    truncated = content[:remaining_chars] + "..."
                    summary_parts.insert(0, f"{role}: {truncated}")
                break
            
            summary_parts.insert(0, message_text)
            current_chars += message_chars
        
        return "\n".join(summary_parts)
    
    def apply_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Apply a predefined template
        
        Args:
            template_name: Name of template file (without .md)
            context: Variables to fill in template
            
        Returns:
            Filled template
        """
        template_file = self.templates_dir / f"{template_name}.md"
        
        if not template_file.exists():
            return None
        
        template_text = template_file.read_text()
        
        # Simple variable substitution: {{variable_name}}
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            template_text = template_text.replace(placeholder, str(value))
        
        return template_text
    
    def save_template(self, template_name: str, content: str):
        """
        Save a template for reuse
        
        Args:
            template_name: Name of template (without .md)
            content: Template content
        """
        template_file = self.templates_dir / f"{template_name}.md"
        template_file.write_text(content)
    
    def optimize_prompt_data(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize prompt data structure (for API calls)
        
        Args:
            prompt_data: Dict with 'messages' or 'prompt' key
            
        Returns:
            Optimized prompt data
        """
        import copy
        optimized = copy.deepcopy(prompt_data)
        
        # Handle messages format (chat)
        if 'messages' in optimized:
            messages = optimized['messages']
            
            # Compress each message
            for message in messages:
                if 'content' in message:
                    original = message['content']
                    compressed = self.compress_prompt(original)
                    message['content'] = compressed
            
            # Summarize history if too long (more than 10 messages)
            if len(messages) > 10:
                # Keep system message and last few user/assistant messages
                system_msgs = [m for m in messages if m.get('role') == 'system']
                other_msgs = [m for m in messages if m.get('role') != 'system']
                
                # Keep last 4 exchanges (8 messages)
                recent_msgs = other_msgs[-8:]
                
                optimized['messages'] = system_msgs + recent_msgs
        
        # Handle single prompt format
        elif 'prompt' in optimized:
            original = optimized['prompt']
            compressed = self.compress_prompt(original)
            optimized['prompt'] = compressed
        
        return optimized
    
    def run(self, prompt_input: Any) -> Any:
        """
        Main optimization method
        
        Args:
            prompt_input: String or dict with prompt data
            
        Returns:
            Optimized prompt (same type as input)
        """
        original_input = prompt_input
        
        # Handle string input
        if isinstance(prompt_input, str):
            optimized = self.compress_prompt(prompt_input)
            
            # Log optimization
            self._log_optimization(
                original_length=len(original_input),
                optimized_length=len(optimized),
                input_type='string'
            )
            
            return optimized
        
        # Handle dict input (API format)
        elif isinstance(prompt_input, dict):
            optimized = self.optimize_prompt_data(prompt_input)
            
            # Calculate token savings (approximate)
            original_tokens = self._estimate_tokens(original_input)
            optimized_tokens = self._estimate_tokens(optimized)
            
            # Log optimization
            self._log_optimization(
                original_length=original_tokens,
                optimized_length=optimized_tokens,
                input_type='dict'
            )
            
            return optimized
        
        # Unknown type, return as-is
        return prompt_input
    
    def _estimate_tokens(self, data: Any) -> int:
        """
        Estimate token count (rough approximation)
        
        Args:
            data: String or dict
            
        Returns:
            Estimated token count
        """
        if isinstance(data, str):
            # Rough estimate: 1 token ≈ 4 characters
            return len(data) // 4
        
        elif isinstance(data, dict):
            # Convert to string and estimate
            text = json.dumps(data)
            return len(text) // 4
        
        return 0
    
    def _log_optimization(self, original_length: int, optimized_length: int, input_type: str):
        """
        Log optimization results
        
        Args:
            original_length: Original token/char count
            optimized_length: Optimized token/char count
            input_type: Type of input ('string' or 'dict')
        """
        tokens_saved = original_length - optimized_length
        savings_percent = (tokens_saved / original_length * 100) if original_length > 0 else 0
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'optimization': 'prompt_compression',
            'original_length': original_length,
            'optimized_length': optimized_length,
            'tokens_saved': tokens_saved,
            'savings_percent': round(savings_percent, 2),
            'input_type': input_type
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# Convenience function
def optimize_prompt(prompt: Any, rules: Optional[Dict] = None) -> Any:
    """
    Convenience function to optimize a prompt
    
    Args:
        prompt: String or dict with prompt data
        rules: Optional optimization rules
        
    Returns:
        Optimized prompt
    """
    optimizer = PromptOptimizer(rules)
    return optimizer.run(prompt)


if __name__ == "__main__":
    # Test the optimizer
    optimizer = PromptOptimizer()
    
    # Test string compression
    test_prompt = """
    Please kindly help me to analyze the following data. I think it would be very helpful
    if you could just simply provide a summary. In order to do this effectively, please
    consider the following factors that I believe are quite important for this analysis.
    """
    
    print("Original prompt:")
    print(test_prompt)
    print(f"Length: {len(test_prompt)} chars, ~{len(test_prompt)//4} tokens")
    print()
    
    compressed = optimizer.compress_prompt(test_prompt)
    print("Compressed prompt:")
    print(compressed)
    print(f"Length: {len(compressed)} chars, ~{len(compressed)//4} tokens")
    print(f"Savings: {len(test_prompt) - len(compressed)} chars ({(len(test_prompt) - len(compressed))/len(test_prompt)*100:.1f}%)")
