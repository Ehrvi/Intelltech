#!/usr/bin/env python3
"""
Design System Generator Module for MOTHER
Generates complete design systems using OpenAI and design knowledge
"""

import os
import json
from openai import OpenAI

class DesignSystemGenerator:
    """Generates complete design systems automatically"""
    
    def __init__(self):
        api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        if not api_base.startswith("http"):
            api_base = f"https://{api_base}"
        
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=api_base,
            timeout=120.0,
            max_retries=3
        )
        
        # Load design system prompt
        prompt_path = "/home/ubuntu/autonomous_design_system_prompt_v2.md"
        with open(prompt_path, 'r') as f:
            self.design_system_prompt = f.read()
    
    def generate(self, project_context: str, output_dir: str = None) -> dict:
        """
        Generate complete design system for a project
        
        Args:
            project_context: Description of the project/company
            output_dir: Directory to save design system files
            
        Returns:
            dict with design system specifications and file paths
        """
        print("\n" + "="*80)
        print("🎨 DESIGN SYSTEM GENERATOR - STARTING")
        print("="*80)
        print(f"\nProject Context: {project_context[:100]}...")
        
        # Create output directory
        if output_dir is None:
            output_dir = "/home/ubuntu/design_systems/latest"
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate design system using OpenAI
        print("\n📊 Analyzing project and generating design system...")
        
        full_prompt = f"""{self.design_system_prompt}

---

## PROJECT CONTEXT

{project_context}

---

## YOUR TASK

Based on the project context above and all the knowledge in this prompt, generate a COMPLETE design system.

Deliver:
1. **Strategy & Analysis** - Business analysis, audience, objectives, cultural considerations
2. **Visual Strategy** - Mood, style, justification (psychology + culture + strategy)
3. **Color System** - Complete palette with accessibility validation
4. **Typography System** - Font selection, scale, hierarchy
5. **Grid System** - Breakpoints, specifications, 8-point grid
6. **Component Specifications** - Buttons, inputs, cards, navigation
7. **Layout Patterns** - Hero, content sections, footer
8. **Iconography** - Style, sizes, library recommendation
9. **Image Guidelines** - Photography style, treatment
10. **Animation Principles** - Timing, easing, examples
11. **Design Tokens** - JSON format with all variables

Format as a comprehensive markdown document ready for implementation.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert design system architect with deep knowledge of psychology, culture, strategy, and visual design. You create comprehensive, production-ready design systems."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=16000
            )
            
            design_system_content = response.choices[0].message.content
            
            # Save design system document
            design_system_path = os.path.join(output_dir, "design_system.md")
            with open(design_system_path, 'w', encoding='utf-8') as f:
                f.write(f"# Design System\n\n")
                f.write(f"**Generated for:** {project_context[:200]}\n\n")
                f.write(f"---\n\n")
                f.write(design_system_content)
            
            # Calculate cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = (input_tokens * 0.0025 + output_tokens * 0.01) / 1000
            
            print(f"\n✅ Design system generated successfully!")
            print(f"   Tokens: {input_tokens + output_tokens:,}")
            print(f"   Cost: ${cost:.4f}")
            print(f"   Saved to: {design_system_path}")
            
            # Extract design tokens (if present in response)
            design_tokens = self._extract_design_tokens(design_system_content)
            if design_tokens:
                tokens_path = os.path.join(output_dir, "design_tokens.json")
                with open(tokens_path, 'w', encoding='utf-8') as f:
                    json.dump(design_tokens, f, indent=2)
                print(f"   Design tokens: {tokens_path}")
            
            print("\n" + "="*80)
            print("🎨 DESIGN SYSTEM GENERATOR - COMPLETED")
            print("="*80)
            
            return {
                'success': True,
                'design_system_path': design_system_path,
                'design_tokens_path': tokens_path if design_tokens else None,
                'output_dir': output_dir,
                'cost': cost,
                'tokens': input_tokens + output_tokens
            }
            
        except Exception as e:
            print(f"\n❌ Error generating design system: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_design_tokens(self, content: str) -> dict:
        """Extract design tokens from generated content if present"""
        # Try to find JSON code block with design tokens
        import re
        
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        matches = re.findall(json_pattern, content)
        
        for match in matches:
            try:
                tokens = json.loads(match)
                if 'colors' in tokens or 'typography' in tokens or 'spacing' in tokens:
                    return tokens
            except:
                continue
        
        return None


def generate_design_system(project_context: str, output_dir: str = None) -> dict:
    """
    Main function to generate design system
    
    Args:
        project_context: Description of the project/company
        output_dir: Directory to save design system files
        
    Returns:
        dict with generation results
    """
    generator = DesignSystemGenerator()
    return generator.generate(project_context, output_dir)


# CLI for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python design_system_generator.py <project_context> [output_dir]")
        print("Example: python design_system_generator.py 'IntellTech - SHMS for mining in APAC'")
        sys.exit(1)
    
    project_context = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = generate_design_system(project_context, output_dir)
    
    if result['success']:
        print(f"\n✅ Design system ready at: {result['output_dir']}")
    else:
        print(f"\n❌ Failed: {result['error']}")
