#!/usr/bin/env python3
"""
Response Controller for Cost Reduction
Controls API response length and format to reduce token usage

Target: 10-30% token reduction
Quality: Maintain essential information
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class ResponseController:
    """Controls API responses to reduce token usage"""
    
    def __init__(self, rules: Optional[Dict] = None):
        """
        Initialize ResponseController
        
        Args:
            rules: Optional dict with control rules
        """
        self.rules = rules or {
            'default_max_tokens': 500,
            'max_tokens_by_type': {
                'summary': 150,
                'analysis': 300,
                'code': 500,
                'creative': 800,
                'default': 500
            },
            'enable_truncation': True,
            'truncation_threshold': 1.05,  # Truncate if response is 5% over limit (more aggressive)
            'enable_streaming': False
        }
        
        # Tracking
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.log_file = self.base_path / "logs" / "response_control.jsonl"
        self.log_file.parent.mkdir(exist_ok=True)
    
    def get_max_tokens(self, request_type: str = 'default') -> int:
        """
        Get max_tokens for a request type
        
        Args:
            request_type: Type of request ('summary', 'analysis', etc.)
            
        Returns:
            Max tokens limit
        """
        return self.rules['max_tokens_by_type'].get(
            request_type,
            self.rules['default_max_tokens']
        )
    
    def enforce_max_tokens(self, api_params: Dict[str, Any], request_type: str = 'default') -> Dict[str, Any]:
        """
        Add or modify max_tokens parameter in API request
        
        Args:
            api_params: API request parameters
            request_type: Type of request
            
        Returns:
            Modified API parameters
        """
        params = api_params.copy()
        
        # Get appropriate max_tokens
        max_tokens = self.get_max_tokens(request_type)
        
        # Set max_tokens if not already set or if it's too high
        if 'max_tokens' not in params or params['max_tokens'] > max_tokens:
            params['max_tokens'] = max_tokens
        
        return params
    
    def truncate_response(self, response_text: str, max_length: Optional[int] = None) -> str:
        """
        Truncate response if too long
        
        Args:
            response_text: Original response
            max_length: Maximum length in characters (None = use default)
            
        Returns:
            Truncated response
        """
        if not self.rules['enable_truncation']:
            return response_text
        
        if max_length is None:
            # Estimate from default max_tokens
            max_length = self.rules['default_max_tokens'] * 4  # 1 token ≈ 4 chars
        
        threshold_length = int(max_length * self.rules['truncation_threshold'])
        
        if len(response_text) <= threshold_length:
            return response_text
        
        # Truncate at sentence boundary if possible
        truncated = response_text[:max_length]
        
        # Find last sentence boundary
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        boundary = max(last_period, last_newline)
        
        if boundary > max_length * 0.8:  # Only truncate at boundary if it's not too far back
            truncated = truncated[:boundary + 1]
        
        # Add ellipsis if truncated
        if len(truncated) < len(response_text):
            truncated += "\n\n[Response truncated for brevity]"
        
        return truncated
    
    def summarize_response(self, response_text: str, max_length: int = 200) -> str:
        """
        Create a summary of a long response
        
        Args:
            response_text: Original response
            max_length: Maximum summary length
            
        Returns:
            Summary
        """
        if len(response_text) <= max_length:
            return response_text
        
        # Simple extractive summary: first paragraph + last paragraph
        paragraphs = response_text.split('\n\n')
        
        if len(paragraphs) <= 2:
            return self.truncate_response(response_text, max_length)
        
        first_para = paragraphs[0]
        last_para = paragraphs[-1]
        
        summary = f"{first_para}\n\n[...]\n\n{last_para}"
        
        if len(summary) > max_length:
            summary = self.truncate_response(summary, max_length)
        
        return summary
    
    def process_api_response(self, response_data: Dict[str, Any], request_type: str = 'default') -> Dict[str, Any]:
        """
        Process API response to control length
        
        Args:
            response_data: API response data
            request_type: Type of request
            
        Returns:
            Processed response data
        """
        processed = response_data.copy()
        
        # Get max length for this request type
        max_tokens = self.get_max_tokens(request_type)
        max_length = max_tokens * 4  # Approximate chars
        
        # Handle OpenAI chat completion format
        if 'choices' in processed:
            for choice in processed['choices']:
                if 'message' in choice and 'content' in choice['message']:
                    original = choice['message']['content']
                    truncated = self.truncate_response(original, max_length)
                    choice['message']['content'] = truncated
        
        # Handle simple text response
        elif 'text' in processed:
            original = processed['text']
            truncated = self.truncate_response(original, max_length)
            processed['text'] = truncated
        
        return processed
    
    def run(self, response_input: Any, request_type: str = 'default') -> Any:
        """
        Main control method
        
        Args:
            response_input: String or dict with response data
            request_type: Type of request
            
        Returns:
            Controlled response (same type as input)
        """
        original_input = response_input
        
        # Handle string input
        if isinstance(response_input, str):
            max_tokens = self.get_max_tokens(request_type)
            max_length = max_tokens * 4
            
            controlled = self.truncate_response(response_input, max_length)
            
            # Log control
            self._log_control(
                original_length=len(original_input),
                controlled_length=len(controlled),
                input_type='string',
                request_type=request_type
            )
            
            return controlled
        
        # Handle dict input (API format)
        elif isinstance(response_input, dict):
            controlled = self.process_api_response(response_input, request_type)
            
            # Calculate token savings (approximate)
            original_tokens = self._estimate_tokens(original_input)
            controlled_tokens = self._estimate_tokens(controlled)
            
            # Log control
            self._log_control(
                original_length=original_tokens,
                controlled_length=controlled_tokens,
                input_type='dict',
                request_type=request_type
            )
            
            return controlled
        
        # Unknown type, return as-is
        return response_input
    
    def _estimate_tokens(self, data: Any) -> int:
        """
        Estimate token count (rough approximation)
        
        Args:
            data: String or dict
            
        Returns:
            Estimated token count
        """
        if isinstance(data, str):
            return len(data) // 4
        
        elif isinstance(data, dict):
            text = json.dumps(data)
            return len(text) // 4
        
        return 0
    
    def _log_control(self, original_length: int, controlled_length: int, 
                    input_type: str, request_type: str):
        """
        Log control results
        
        Args:
            original_length: Original token/char count
            controlled_length: Controlled token/char count
            input_type: Type of input ('string' or 'dict')
            request_type: Type of request
        """
        tokens_saved = original_length - controlled_length
        savings_percent = (tokens_saved / original_length * 100) if original_length > 0 else 0
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'optimization': 'response_control',
            'original_length': original_length,
            'controlled_length': controlled_length,
            'tokens_saved': tokens_saved,
            'savings_percent': round(savings_percent, 2),
            'input_type': input_type,
            'request_type': request_type
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# Convenience functions
def control_response(response: Any, request_type: str = 'default', rules: Optional[Dict] = None) -> Any:
    """
    Convenience function to control a response
    
    Args:
        response: String or dict with response data
        request_type: Type of request
        rules: Optional control rules
        
    Returns:
        Controlled response
    """
    controller = ResponseController(rules)
    return controller.run(response, request_type)


def enforce_max_tokens(api_params: Dict[str, Any], request_type: str = 'default') -> Dict[str, Any]:
    """
    Convenience function to enforce max_tokens
    
    Args:
        api_params: API request parameters
        request_type: Type of request
        
    Returns:
        Modified API parameters
    """
    controller = ResponseController()
    return controller.enforce_max_tokens(api_params, request_type)


if __name__ == "__main__":
    # Test the controller
    controller = ResponseController()
    
    # Test response truncation
    test_response = """
    This is a very long response that goes on and on. It contains multiple sentences
    and paragraphs. The response is quite verbose and could be truncated to save tokens.
    
    This is the second paragraph. It continues with more information that may or may not
    be essential. The goal is to demonstrate how the response controller can truncate
    long responses while maintaining readability.
    
    This is the third paragraph. It adds even more content to make the response longer.
    By now, the response is definitely over the token limit and should be truncated.
    """ * 5  # Repeat to make it very long
    
    print("Original response:")
    print(f"Length: {len(test_response)} chars, ~{len(test_response)//4} tokens")
    print()
    
    controlled = controller.truncate_response(test_response, max_length=500)
    print("Controlled response:")
    print(controlled)
    print()
    print(f"Length: {len(controlled)} chars, ~{len(controlled)//4} tokens")
    print(f"Savings: {len(test_response) - len(controlled)} chars ({(len(test_response) - len(controlled))/len(test_response)*100:.1f}%)")
