#!/usr/bin/env python3
"""
Visual Identity Workflow Integration for MOTHER
Integrates visual identity detection and generation into MOTHER workflow
"""

import sys
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge/core')
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge/modules')

from visual_identity_detector import detect_visual_identity_need
from design_system_generator import generate_design_system

class VisualIdentityWorkflow:
    """Manages visual identity detection and generation workflow"""
    
    def __init__(self, automation_level: int = 2):
        """
        Initialize workflow
        
        Args:
            automation_level: 
                1 = Suggest only (never auto-create)
                2 = Ask for high priority (default)
                3 = Auto-create for high priority
        """
        self.automation_level = automation_level
    
    def process(self, user_request: str) -> dict:
        """
        Process user request and handle visual identity needs
        
        Args:
            user_request: User's request or project description
            
        Returns:
            dict with workflow results
        """
        # Step 1: Detect need
        detection = detect_visual_identity_need(user_request, self.automation_level)
        
        if not detection['needed']:
            return {
                'visual_identity_needed': False,
                'detection': detection,
                'action_taken': 'none'
            }
        
        # Step 2: Determine action based on automation level
        action = detection['action']
        
        if action == 'auto':
            # Auto-create design system
            print(f"\n🎨 Auto-creating design system (confidence: {detection['confidence']*100:.0f}%)")
            result = generate_design_system(user_request)
            
            return {
                'visual_identity_needed': True,
                'detection': detection,
                'action_taken': 'auto_created',
                'generation_result': result
            }
        
        elif action == 'ask':
            # Return with recommendation to ask user
            return {
                'visual_identity_needed': True,
                'detection': detection,
                'action_taken': 'ask_user',
                'message': f"🎨 {detection['suggestion']}\n\nWould you like me to create a complete design system now?"
            }
        
        else:  # suggest
            # Return with suggestion
            return {
                'visual_identity_needed': True,
                'detection': detection,
                'action_taken': 'suggested',
                'message': f"💡 {detection['suggestion']}"
            }
    
    def create_design_system(self, project_context: str, output_dir: str = None) -> dict:
        """
        Create design system (can be called after user confirms)
        
        Args:
            project_context: Project description
            output_dir: Optional output directory
            
        Returns:
            Generation result
        """
        return generate_design_system(project_context, output_dir)


def check_visual_identity_need(user_request: str, automation_level: int = 2) -> dict:
    """
    Main function to check and handle visual identity needs
    
    Args:
        user_request: User's request
        automation_level: 1=suggest, 2=ask, 3=auto
        
    Returns:
        Workflow result
    """
    workflow = VisualIdentityWorkflow(automation_level)
    return workflow.process(user_request)


# CLI for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visual_identity_workflow.py <user_request> [automation_level]")
        print("Example: python visual_identity_workflow.py 'criar website para IntellTech' 2")
        sys.exit(1)
    
    user_request = sys.argv[1]
    automation_level = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    result = check_visual_identity_need(user_request, automation_level)
    
    print("\n" + "="*80)
    print("VISUAL IDENTITY WORKFLOW RESULT")
    print("="*80)
    print(f"\nVisual Identity Needed: {'✅ YES' if result['visual_identity_needed'] else '❌ NO'}")
    print(f"Action Taken: {result['action_taken'].upper()}")
    
    if 'message' in result:
        print(f"\nMessage: {result['message']}")
    
    if 'generation_result' in result:
        gen = result['generation_result']
        if gen['success']:
            print(f"\n✅ Design system created at: {gen['output_dir']}")
            print(f"   Cost: ${gen['cost']:.4f}")
        else:
            print(f"\n❌ Generation failed: {gen['error']}")
    
    print("\n" + "="*80)
