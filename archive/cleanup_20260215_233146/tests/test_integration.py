#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.unified_enforcement import UnifiedEnforcementPipeline

class TestOpenAIIntegration(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.base_path = Path(__file__).parent.parent
        self.pipeline = UnifiedEnforcementPipeline(self.base_path)

    def test_openai_execution_flow(self):
        """Test the full execution flow with a real OpenAI call."""
        # This action will be routed to the OpenAI execution path
        action = {
            "type": "test.openai.generate",
            "payload": {
                "args": (),
                "kwargs": {"prompt": "Say hello in English."}
            },
            "metadata": {
                "tool": "test_tool",
                "module": "test_module",
                "cost_estimate": 0.1, # Low cost to pass the cost gate
            },
        }

        # Enforce the action
        result = self.pipeline.enforce(action)

        # Print the full result for debugging
        print(f"Enforcement Result: {result}")

        # Assertions
        self.assertFalse(result.get("blocked"), "The action should not be blocked.")
        self.assertEqual(result.get("status"), "ok", "The status should be 'ok'.")
        
        output_data = result.get("data", {}).get("output", {})

        self.assertIn("result", output_data, "The output data should contain a 'result' key.")
        self.assertIsInstance(output_data["result"], str, "The result should be a string.")
        self.assertGreater(len(output_data["result"]), 0, "The result string should not be empty.")
        self.assertIn("hello", output_data["result"].lower(), "The result should contain 'hello'.")

if __name__ == '__main__':
    unittest.main()
