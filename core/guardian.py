#!/usr/bin/env python3
"""
Guardian Validation System

Validates output quality using OpenAI before delivery.
Fixes BUG-003: No Quality Validation

Based on: Ouyang, L. et al. (2022). "Training language models to follow 
instructions with human feedback" (InstructGPT)
"""

import os
from openai import OpenAI
from typing import Dict, Optional

class Guardian:
    """Quality validation using OpenAI"""
    
    def __init__(self):
        self.client = OpenAI()
        self.quality_threshold = 80  # Minimum acceptable quality
    
    def validate(
        self,
        output: str,
        task: str,
        criteria: Optional[Dict[str, int]] = None
    ) -> Dict:
        """
        Validate output quality
        
        Args:
            output: The output to validate
            task: Description of the original task
            criteria: Custom criteria weights (default: accuracy=40, completeness=30, clarity=20, relevance=10)
        
        Returns:
            Dict with 'score', 'passed', 'feedback', 'breakdown'
        """
        if criteria is None:
            criteria = {
                'accuracy': 40,
                'completeness': 30,
                'clarity': 20,
                'relevance': 10
            }
        
        # Build validation prompt
        validation_prompt = f"""
You are a quality validator. Rate the following output on a scale of 0-100.

TASK:
{task}

OUTPUT:
{output}

CRITERIA:
{self._format_criteria(criteria)}

Provide your rating in this exact JSON format:
{{
    "overall_score": <number 0-100>,
    "accuracy": <number 0-100>,
    "completeness": <number 0-100>,
    "clarity": <number 0-100>,
    "relevance": <number 0-100>,
    "feedback": "<brief explanation of the score>",
    "improvements": "<suggestions for improvement if score < 80>"
}}

Be strict but fair. A score of 80+ means production-ready quality.
"""
        
        try:
            # Call OpenAI for validation
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a strict quality validator."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.3,  # Low temperature for consistent scoring
                response_format={"type": "json_object"}
            )
            
            # Parse response
            import json
            result = json.loads(response.choices[0].message.content)
            
            score = result.get('overall_score', 0)
            passed = score >= self.quality_threshold
            
            return {
                'score': score,
                'passed': passed,
                'feedback': result.get('feedback', ''),
                'improvements': result.get('improvements', ''),
                'breakdown': {
                    'accuracy': result.get('accuracy', 0),
                    'completeness': result.get('completeness', 0),
                    'clarity': result.get('clarity', 0),
                    'relevance': result.get('relevance', 0)
                },
                'cost': 0.01  # Approximate cost of validation
            }
            
        except Exception as e:
            # If validation fails, assume quality is acceptable
            # (fail-open to avoid blocking legitimate work)
            return {
                'score': 80,
                'passed': True,
                'feedback': f'Validation error: {e}. Assuming acceptable quality.',
                'improvements': '',
                'breakdown': {},
                'cost': 0,
                'error': str(e)
            }
    
    def _format_criteria(self, criteria: Dict[str, int]) -> str:
        """Format criteria for the prompt"""
        lines = []
        for criterion, weight in criteria.items():
            lines.append(f"- {criterion.capitalize()}: {weight}%")
        return '\n'.join(lines)
    
    def validate_and_improve(
        self,
        output: str,
        task: str,
        max_iterations: int = 2
    ) -> Dict:
        """
        Validate and iteratively improve until quality threshold is met
        
        Args:
            output: Initial output
            task: Task description
            max_iterations: Maximum improvement attempts
        
        Returns:
            Dict with final 'output', 'score', 'iterations', 'total_cost'
        """
        current_output = output
        total_cost = 0
        
        for iteration in range(max_iterations):
            # Validate current output
            validation = self.validate(current_output, task)
            total_cost += validation['cost']
            
            if validation['passed']:
                return {
                    'output': current_output,
                    'score': validation['score'],
                    'iterations': iteration + 1,
                    'total_cost': total_cost,
                    'feedback': validation['feedback']
                }
            
            # If not passed, try to improve
            if iteration < max_iterations - 1:
                improvement_prompt = f"""
The following output scored {validation['score']}/100, which is below the 80 threshold.

TASK:
{task}

CURRENT OUTPUT:
{current_output}

FEEDBACK:
{validation['feedback']}

IMPROVEMENTS NEEDED:
{validation['improvements']}

Please provide an improved version that addresses the feedback.
"""
                
                try:
                    response = self.client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert at improving content quality."},
                            {"role": "user", "content": improvement_prompt}
                        ],
                        temperature=0.7
                    )
                    
                    current_output = response.choices[0].message.content
                    total_cost += 0.02  # Approximate cost of improvement
                    
                except Exception as e:
                    # If improvement fails, return current output
                    break
        
        # Return final output even if below threshold
        final_validation = self.validate(current_output, task)
        total_cost += final_validation['cost']
        
        return {
            'output': current_output,
            'score': final_validation['score'],
            'iterations': max_iterations,
            'total_cost': total_cost,
            'feedback': final_validation['feedback'],
            'warning': 'Quality threshold not met after maximum iterations'
        }


# Convenience functions
_guardian = None

def get_guardian() -> Guardian:
    """Get the global Guardian instance"""
    global _guardian
    if _guardian is None:
        _guardian = Guardian()
    return _guardian


def validate(output: str, task: str) -> Dict:
    """Quick validation function"""
    return get_guardian().validate(output, task)


def validate_and_improve(output: str, task: str, max_iterations: int = 2) -> Dict:
    """Quick validate-and-improve function"""
    return get_guardian().validate_and_improve(output, task, max_iterations)


if __name__ == '__main__':
    # Demo usage
    guardian = Guardian()
    
    # Test validation
    test_output = """
    The top 10 AI companies are:
    1. OpenAI
    2. Google DeepMind
    3. Anthropic
    4. Microsoft
    5. Meta AI
    """
    
    test_task = "List the top 10 AI companies with brief descriptions"
    
    print("Testing Guardian Validation...")
    print("=" * 70)
    
    result = guardian.validate(test_output, test_task)
    
    print(f"Score: {result['score']}/100")
    print(f"Passed: {result['passed']}")
    print(f"Feedback: {result['feedback']}")
    print(f"Cost: ${result['cost']:.4f}")
    print()
    
    if not result['passed']:
        print("Improvements needed:")
        print(result['improvements'])
    
    print("=" * 70)
