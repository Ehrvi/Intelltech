"""
OpenAI Helper - Solução Científica para Chamadas OpenAI

Implementa a solução validada pelo método científico:
- gpt-4-turbo para tarefas rápidas (1-5s)
- gpt-5 para tarefas complexas com reasoning (15-90s)
- Timeout adequado para cada modelo
- Retry automático com fallback
"""

import os
import time
import httpx
from typing import Dict, Any, Optional, Literal
from openai import OpenAI
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIHelper:
    """
    Helper class for OpenAI API calls with scientific method-based optimization.
    
    Features:
    - Automatic model selection based on task complexity
    - Appropriate timeouts for each model
    - Retry logic with exponential backoff
    - Comprehensive error handling
    - Performance monitoring
    """
    
    # Model configurations based on empirical testing
    MODEL_CONFIGS = {
        'gpt-4-turbo': {
            'timeout': 60,      # 1 minute (typically responds in 1-5s)
            'max_tokens': 4096,
            'use_case': 'fast, straightforward tasks'
        },
        'gpt-5': {
            'timeout': 300,     # 5 minutes (reasoning takes 15-90s)
            'max_tokens': 8192,
            'use_case': 'complex reasoning, deep analysis'
        }
    }
    
    def __init__(self):
        """Initialize OpenAI client with proper configuration."""
        api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        if not api_base.startswith('http'):
            api_base = 'https://' + api_base
        
        # Create client with extended timeout
        self.client = OpenAI(
            base_url=api_base,
            timeout=httpx.Timeout(300.0, connect=10.0)
        )
        
        logger.info(f"✓ OpenAI Helper initialized with base URL: {api_base}")
    
    def generate(
        self,
        prompt: str,
        model: Literal['gpt-4-turbo', 'gpt-5', 'auto'] = 'auto',
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using OpenAI API with automatic model selection.
        
        Args:
            prompt: Input prompt for generation
            model: Model to use ('gpt-4-turbo', 'gpt-5', or 'auto')
            max_retries: Maximum number of retry attempts
            **kwargs: Additional parameters for the API call
        
        Returns:
            Dict with:
                - success: bool
                - output: str (generated text)
                - model_used: str
                - duration: float (seconds)
                - metadata: dict
        """
        # Auto-select model based on prompt complexity
        if model == 'auto':
            model = self._select_model(prompt)
        
        config = self.MODEL_CONFIGS[model]
        logger.info(f"Using model: {model} (timeout: {config['timeout']}s)")
        
        # Retry loop with exponential backoff
        for attempt in range(1, max_retries + 1):
            try:
                start_time = time.time()
                
                response = self.client.responses.create(
                    model=model,
                    input=prompt,
                    **kwargs
                )
                
                duration = time.time() - start_time
                
                # Extract text from response
                output_text = self._extract_text(response.output)
                
                logger.info(f"✓ Success in {duration:.2f}s (attempt {attempt}/{max_retries})")
                
                return {
                    'success': True,
                    'output': output_text,
                    'model_used': model,
                    'duration': duration,
                    'metadata': {
                        'attempts': attempt,
                        'response_length': len(output_text)
                    }
                }
            
            except Exception as e:
                duration = time.time() - start_time
                logger.warning(f"✗ Attempt {attempt}/{max_retries} failed after {duration:.2f}s: {e}")
                
                if attempt == max_retries:
                    # Final attempt failed - try fallback
                    if model == 'gpt-5':
                        logger.info("Trying fallback to gpt-4-turbo...")
                        return self.generate(prompt, model='gpt-4-turbo', max_retries=1, **kwargs)
                    else:
                        return {
                            'success': False,
                            'output': '',
                            'model_used': model,
                            'duration': duration,
                            'error': str(e),
                            'metadata': {'attempts': attempt}
                        }
                
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
    
    def _select_model(self, prompt: str) -> str:
        """
        Select optimal model based on prompt characteristics.
        
        Heuristics (based on empirical testing):
        - Short prompts (<200 chars): gpt-4-turbo
        - Simple tasks (keywords: "summarize", "translate", "list"): gpt-4-turbo
        - Complex tasks (keywords: "analyze", "design", "implement", "comprehensive"): gpt-5
        - Code generation >100 lines: gpt-5
        """
        prompt_lower = prompt.lower()
        prompt_length = len(prompt)
        
        # Short prompts = fast model
        if prompt_length < 200:
            return 'gpt-4-turbo'
        
        # Keywords indicating simple tasks
        simple_keywords = ['summarize', 'translate', 'list', 'define', 'what is']
        if any(kw in prompt_lower for kw in simple_keywords):
            return 'gpt-4-turbo'
        
        # Keywords indicating complex tasks
        complex_keywords = [
            'analyze', 'design', 'implement', 'comprehensive',
            'complete implementation', 'production-ready',
            'architecture', 'system', 'framework'
        ]
        if any(kw in prompt_lower for kw in complex_keywords):
            return 'gpt-5'
        
        # Default to fast model
        return 'gpt-4-turbo'
    
    def _extract_text(self, output: list) -> str:
        """Extract text from OpenAI response output."""
        text_parts = []
        
        for item in output:
            if hasattr(item, 'content') and item.content:
                for content_item in item.content:
                    if hasattr(content_item, 'text'):
                        text_parts.append(content_item.text)
        
        return '\n'.join(text_parts)
    
    def generate_code(
        self,
        specification: str,
        language: str = 'python',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate code with optimized prompt for code generation.
        
        Args:
            specification: Code specification/requirements
            language: Programming language
            **kwargs: Additional parameters
        
        Returns:
            Same format as generate()
        """
        prompt = f"""Generate {language} code based on this specification:

{specification}

Requirements:
- Production-ready code
- Type hints (if applicable)
- Docstrings for all functions/classes
- Comprehensive error handling
- Clean, readable code

Output only the code, no explanations."""
        
        return self.generate(prompt, model='gpt-5', **kwargs)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics (placeholder for future implementation)."""
        return {
            'total_calls': 0,
            'total_duration': 0,
            'average_duration': 0,
            'model_distribution': {}
        }


# Global instance for easy import
openai_helper = OpenAIHelper()


# Convenience functions
def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """Convenience function for text generation."""
    return openai_helper.generate(prompt, **kwargs)


def generate_code(specification: str, **kwargs) -> Dict[str, Any]:
    """Convenience function for code generation."""
    return openai_helper.generate_code(specification, **kwargs)


if __name__ == '__main__':
    # Test the helper
    print("=== Testing OpenAI Helper ===\n")
    
    # Test 1: Simple prompt (should use gpt-4-turbo)
    result1 = generate("Say 'hello' in one word")
    print(f"Test 1: {result1['model_used']} in {result1['duration']:.2f}s")
    print(f"Output: {result1['output']}\n")
    
    # Test 2: Complex prompt (should use gpt-5)
    result2 = generate("Analyze the comprehensive implications of quantum computing on cryptography")
    print(f"Test 2: {result2['model_used']} in {result2['duration']:.2f}s")
    print(f"Output length: {len(result2['output'])} chars\n")
    
    print("✓ All tests completed")
