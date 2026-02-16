#!/usr/bin/env python3
"""
Visual Identity Need Detector for MOTHER
Automatically detects when a project needs visual identity/design system
"""

import re
from typing import Dict, List, Tuple

class VisualIdentityDetector:
    """Detects need for visual identity based on context analysis"""
    
    def __init__(self):
        # Trigger keywords that indicate need for visual identity
        self.triggers = {
            'high_priority': [
                'criar website',
                'desenvolver app',
                'nova marca',
                'identidade visual',
                'design system',
                'rebranding',
                'criar logo',
                'visual identity',
                'brand identity',
                'create website',
                'develop app',
                'new brand'
            ],
            'medium_priority': [
                'apresentação',
                'proposta comercial',
                'landing page',
                'pitch deck',
                'sales deck',
                'marketing material',
                'presentation',
                'commercial proposal',
                'slide deck'
            ],
            'low_priority': [
                'documento',
                'relatório',
                'report',
                'document',
                'template'
            ]
        }
        
        # Project types that typically need visual identity
        self.project_types = [
            'website',
            'app',
            'aplicativo',
            'application',
            'plataforma',
            'platform',
            'produto',
            'product',
            'serviço',
            'service',
            'startup',
            'empresa',
            'company',
            'negócio',
            'business'
        ]
        
        # Indicators that visual identity already exists
        self.existing_identity_indicators = [
            'design system',
            'style guide',
            'brand guidelines',
            'guia de marca',
            'paleta de cores',
            'color palette',
            'tipografia definida',
            'defined typography'
        ]
    
    def detect(self, context: str) -> Dict:
        """
        Detect if visual identity is needed based on context
        
        Args:
            context: User request or project description
            
        Returns:
            Dict with detection results:
            {
                'needed': bool,
                'confidence': float (0-1),
                'priority': str ('high', 'medium', 'low'),
                'triggers': List[str],
                'reasoning': str,
                'suggestion': str
            }
        """
        context_lower = context.lower()
        
        # Check if visual identity already exists
        has_existing = self._check_existing_identity(context_lower)
        if has_existing:
            return {
                'needed': False,
                'confidence': 0.9,
                'priority': 'none',
                'triggers': [],
                'reasoning': 'Visual identity already exists in project',
                'suggestion': 'Use existing design system'
            }
        
        # Detect triggers
        high_triggers = self._find_triggers(context_lower, self.triggers['high_priority'])
        medium_triggers = self._find_triggers(context_lower, self.triggers['medium_priority'])
        low_triggers = self._find_triggers(context_lower, self.triggers['low_priority'])
        
        # Detect project type
        project_type_detected = any(pt in context_lower for pt in self.project_types)
        
        # Calculate confidence and priority
        if high_triggers:
            confidence = 0.95
            priority = 'high'
            triggers = high_triggers
        elif medium_triggers:
            confidence = 0.75
            priority = 'medium'
            triggers = medium_triggers
        elif low_triggers:
            confidence = 0.50
            priority = 'low'
            triggers = low_triggers
        elif project_type_detected:
            confidence = 0.60
            priority = 'medium'
            triggers = ['project_type_detected']
        else:
            confidence = 0.0
            priority = 'none'
            triggers = []
        
        needed = confidence >= 0.50
        
        # Generate reasoning
        reasoning = self._generate_reasoning(triggers, project_type_detected, confidence)
        
        # Generate suggestion
        suggestion = self._generate_suggestion(priority, confidence)
        
        return {
            'needed': needed,
            'confidence': confidence,
            'priority': priority,
            'triggers': triggers,
            'reasoning': reasoning,
            'suggestion': suggestion
        }
    
    def _check_existing_identity(self, context: str) -> bool:
        """Check if visual identity already exists"""
        return any(indicator in context for indicator in self.existing_identity_indicators)
    
    def _find_triggers(self, context: str, trigger_list: List[str]) -> List[str]:
        """Find which triggers are present in context"""
        return [trigger for trigger in trigger_list if trigger in context]
    
    def _generate_reasoning(self, triggers: List[str], project_type: bool, confidence: float) -> str:
        """Generate human-readable reasoning"""
        if not triggers and not project_type:
            return "No indicators of visual identity need detected"
        
        reasons = []
        
        if triggers:
            reasons.append(f"Detected keywords: {', '.join(triggers[:3])}")
        
        if project_type:
            reasons.append("Project type typically requires visual identity")
        
        reasons.append(f"Confidence: {confidence*100:.0f}%")
        
        return " | ".join(reasons)
    
    def _generate_suggestion(self, priority: str, confidence: float) -> str:
        """Generate actionable suggestion"""
        if priority == 'high':
            return "🎨 Strongly recommend creating complete design system before proceeding"
        elif priority == 'medium':
            return "🎨 Consider creating visual identity to ensure consistency"
        elif priority == 'low':
            return "🎨 Optional: Create basic style guide for consistency"
        else:
            return "No visual identity needed at this time"
    
    def should_auto_create(self, detection_result: Dict, automation_level: int = 1) -> Tuple[bool, str]:
        """
        Determine if design system should be auto-created based on automation level
        
        Args:
            detection_result: Result from detect()
            automation_level: 1=suggest, 2=ask, 3=auto
            
        Returns:
            (should_create: bool, action: str)
        """
        if not detection_result['needed']:
            return False, 'skip'
        
        priority = detection_result['priority']
        confidence = detection_result['confidence']
        
        if automation_level == 1:
            # Level 1: Always suggest, never auto-create
            return False, 'suggest'
        
        elif automation_level == 2:
            # Level 2: Ask for high priority, suggest for others
            if priority == 'high' and confidence >= 0.90:
                return False, 'ask'
            else:
                return False, 'suggest'
        
        elif automation_level == 3:
            # Level 3: Auto-create for high priority, ask for medium
            if priority == 'high' and confidence >= 0.90:
                return True, 'auto'
            elif priority == 'medium' and confidence >= 0.70:
                return False, 'ask'
            else:
                return False, 'suggest'
        
        return False, 'suggest'


def detect_visual_identity_need(context: str, automation_level: int = 1) -> Dict:
    """
    Main function to detect visual identity need
    
    Args:
        context: User request or project description
        automation_level: 1=suggest, 2=ask, 3=auto
        
    Returns:
        Detection result with action recommendation
    """
    detector = VisualIdentityDetector()
    result = detector.detect(context)
    
    should_create, action = detector.should_auto_create(result, automation_level)
    
    result['should_auto_create'] = should_create
    result['action'] = action
    
    return result


# CLI for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python visual_identity_detector.py <context> [automation_level]")
        print("Example: python visual_identity_detector.py 'criar website para IntellTech' 2")
        sys.exit(1)
    
    context = sys.argv[1]
    automation_level = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    result = detect_visual_identity_need(context, automation_level)
    
    print("\n" + "="*80)
    print("VISUAL IDENTITY NEED DETECTION")
    print("="*80)
    print(f"\nContext: {context}")
    print(f"\nNeeded: {'✅ YES' if result['needed'] else '❌ NO'}")
    print(f"Confidence: {result['confidence']*100:.0f}%")
    print(f"Priority: {result['priority'].upper()}")
    print(f"Triggers: {', '.join(result['triggers']) if result['triggers'] else 'None'}")
    print(f"\nReasoning: {result['reasoning']}")
    print(f"Suggestion: {result['suggestion']}")
    print(f"\nAction: {result['action'].upper()}")
    print(f"Auto-create: {'✅ YES' if result['should_auto_create'] else '❌ NO'}")
    print("\n" + "="*80)
