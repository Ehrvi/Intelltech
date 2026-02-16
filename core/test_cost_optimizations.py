#!/usr/bin/env python3
"""
Test Suite for Cost Optimization Modules
Tests PromptOptimizer and ResponseController
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_optimizer import PromptOptimizer
from response_controller import ResponseController


def test_prompt_optimizer():
    """Test PromptOptimizer functionality"""
    print("="*70)
    print("TEST SUITE: PROMPT OPTIMIZER")
    print("="*70)
    print()
    
    optimizer = PromptOptimizer()
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Basic compression
    print("TEST 1: Basic Prompt Compression")
    print("-"*70)
    tests_total += 1
    
    test_prompt = "Please kindly help me analyze this data. I think it would be very helpful."
    compressed = optimizer.compress_prompt(test_prompt)
    
    original_len = len(test_prompt)
    compressed_len = len(compressed)
    savings = ((original_len - compressed_len) / original_len) * 100
    
    print(f"Original: {test_prompt}")
    print(f"Compressed: {compressed}")
    print(f"Savings: {savings:.1f}%")
    
    if compressed_len < original_len:
        print("✅ PASS: Compression reduced length")
        tests_passed += 1
    else:
        print("❌ FAIL: No compression achieved")
    print()
    
    # Test 2: Chat history summarization
    print("TEST 2: Chat History Summarization")
    print("-"*70)
    tests_total += 1
    
    chat_history = [
        {'role': 'user', 'content': 'What is Python?'},
        {'role': 'assistant', 'content': 'Python is a programming language.'},
        {'role': 'user', 'content': 'How do I install it?'},
        {'role': 'assistant', 'content': 'You can download it from python.org.'},
        {'role': 'user', 'content': 'What are the best practices?'},
        {'role': 'assistant', 'content': 'Follow PEP 8 style guide.'}
    ]
    
    summary = optimizer.summarize_history(chat_history, max_tokens=100)
    
    full_text = '\n'.join([f"{m['role']}: {m['content']}" for m in chat_history])
    
    print(f"Full history length: {len(full_text)} chars")
    print(f"Summary length: {len(summary)} chars")
    print(f"Summary:\n{summary}")
    
    if len(summary) < len(full_text):
        print("✅ PASS: History summarized")
        tests_passed += 1
    else:
        print("❌ FAIL: No summarization achieved")
    print()
    
    # Test 3: Dict optimization
    print("TEST 3: Dict/API Format Optimization")
    print("-"*70)
    tests_total += 1
    
    prompt_data = {
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant. Please be very thorough.'},
            {'role': 'user', 'content': 'Please kindly explain this concept in detail.'}
        ]
    }
    
    optimized_data = optimizer.optimize_prompt_data(prompt_data)
    
    original_str = str(prompt_data)
    optimized_str = str(optimized_data)
    
    print(f"Original: {original_str}")
    print(f"Optimized: {optimized_str}")
    
    if len(optimized_str) < len(original_str):
        print("✅ PASS: Dict optimized")
        tests_passed += 1
    else:
        print("❌ FAIL: No optimization achieved")
    print()
    
    # Summary
    print("="*70)
    print(f"PROMPT OPTIMIZER SUMMARY: {tests_passed}/{tests_total} tests passed")
    print("="*70)
    print()
    
    return tests_passed, tests_total


def test_response_controller():
    """Test ResponseController functionality"""
    print("="*70)
    print("TEST SUITE: RESPONSE CONTROLLER")
    print("="*70)
    print()
    
    controller = ResponseController()
    tests_passed = 0
    tests_total = 0
    
    # Test 1: max_tokens enforcement
    print("TEST 1: max_tokens Enforcement")
    print("-"*70)
    tests_total += 1
    
    api_params = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    }
    
    enforced_params = controller.enforce_max_tokens(api_params, request_type='summary')
    
    print(f"Original params: {api_params}")
    print(f"Enforced params: {enforced_params}")
    
    if 'max_tokens' in enforced_params and enforced_params['max_tokens'] == 150:
        print("✅ PASS: max_tokens enforced correctly")
        tests_passed += 1
    else:
        print("❌ FAIL: max_tokens not enforced")
    print()
    
    # Test 2: Response truncation
    print("TEST 2: Response Truncation")
    print("-"*70)
    tests_total += 1
    
    long_response = "This is a test response. " * 100  # Very long
    
    truncated = controller.truncate_response(long_response, max_length=200)
    
    print(f"Original length: {len(long_response)} chars")
    print(f"Truncated length: {len(truncated)} chars")
    print(f"Truncated: {truncated[:100]}...")
    
    if len(truncated) < len(long_response):
        print("✅ PASS: Response truncated")
        tests_passed += 1
    else:
        print("❌ FAIL: No truncation achieved")
    print()
    
    # Test 3: API response processing
    print("TEST 3: API Response Processing")
    print("-"*70)
    tests_total += 1
    
    api_response = {
        'choices': [
            {
                'message': {
                    'role': 'assistant',
                    'content': 'This is a very long response. ' * 50
                }
            }
        ]
    }
    
    processed = controller.process_api_response(api_response, request_type='summary')
    
    original_content = api_response['choices'][0]['message']['content']
    processed_content = processed['choices'][0]['message']['content']
    
    print(f"Original content length: {len(original_content)} chars")
    print(f"Processed content length: {len(processed_content)} chars")
    
    if len(processed_content) < len(original_content):
        print("✅ PASS: API response processed")
        tests_passed += 1
    else:
        print("❌ FAIL: No processing achieved")
    print()
    
    # Summary
    print("="*70)
    print(f"RESPONSE CONTROLLER SUMMARY: {tests_passed}/{tests_total} tests passed")
    print("="*70)
    print()
    
    return tests_passed, tests_total


def test_integration():
    """Test integration of both modules"""
    print("="*70)
    print("TEST SUITE: INTEGRATION")
    print("="*70)
    print()
    
    optimizer = PromptOptimizer()
    controller = ResponseController()
    tests_passed = 0
    tests_total = 0
    
    # Test: Full pipeline
    print("TEST 1: Full Optimization Pipeline")
    print("-"*70)
    tests_total += 1
    
    # Original request
    original_prompt = {
        'messages': [
            {'role': 'user', 'content': 'Please kindly provide a very detailed analysis of this topic.'}
        ]
    }
    
    # Step 1: Optimize prompt
    optimized_prompt = optimizer.optimize_prompt_data(original_prompt)
    
    # Step 2: Enforce max_tokens
    api_params = controller.enforce_max_tokens(optimized_prompt, request_type='analysis')
    
    # Step 3: Simulate response
    simulated_response = {
        'choices': [
            {
                'message': {
                    'role': 'assistant',
                    'content': 'Here is a detailed analysis. ' * 100
                }
            }
        ]
    }
    
    # Step 4: Control response
    final_response = controller.process_api_response(simulated_response, request_type='analysis')
    
    # Calculate total savings
    original_prompt_len = len(str(original_prompt))
    optimized_prompt_len = len(str(api_params))
    original_response_len = len(simulated_response['choices'][0]['message']['content'])
    final_response_len = len(final_response['choices'][0]['message']['content'])
    
    prompt_savings = ((original_prompt_len - optimized_prompt_len) / original_prompt_len) * 100
    response_savings = ((original_response_len - final_response_len) / original_response_len) * 100
    
    print(f"Prompt optimization: {prompt_savings:.1f}% reduction")
    print(f"Response control: {response_savings:.1f}% reduction")
    print(f"max_tokens enforced: {api_params.get('max_tokens', 'N/A')}")
    
    if prompt_savings > 0 and response_savings > 0 and 'max_tokens' in api_params:
        print("✅ PASS: Full pipeline working")
        tests_passed += 1
    else:
        print("❌ FAIL: Pipeline incomplete")
    print()
    
    # Summary
    print("="*70)
    print(f"INTEGRATION SUMMARY: {tests_passed}/{tests_total} tests passed")
    print("="*70)
    print()
    
    return tests_passed, tests_total


def main():
    """Run all tests"""
    print("\n")
    print("="*70)
    print("COST OPTIMIZATION MODULES - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\n")
    
    # Run all test suites
    prompt_passed, prompt_total = test_prompt_optimizer()
    response_passed, response_total = test_response_controller()
    integration_passed, integration_total = test_integration()
    
    # Overall summary
    total_passed = prompt_passed + response_passed + integration_passed
    total_tests = prompt_total + response_total + integration_total
    
    print("="*70)
    print("OVERALL SUMMARY")
    print("="*70)
    print(f"Total tests passed: {total_passed}/{total_tests}")
    print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
    print()
    
    if total_passed == total_tests:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"❌ {total_tests - total_passed} TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
