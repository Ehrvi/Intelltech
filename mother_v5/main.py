"""
MOTHER V5 - Main Entry Point

Integrates all V5 components with V4 base.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application.agents.rl_agent import RLAgent, State, TaskType, Action, Experience
from application.services.content_generator import ContentGenerator, ContentRequest, ContentType
from application.services.fundraising_assistant import FundraisingAssistant, CompanyData
from application.services.semantic_search import SemanticSearch


class MOTHERV5:
    """
    MOTHER V5 - Main system integrating all components.
    """
    
    def __init__(self):
        """Initialize MOTHER V5"""
        print("🚀 Initializing MOTHER V5...")
        
        # Initialize V5 components
        self.rl_agent = RLAgent()
        self.content_generator = ContentGenerator()
        self.fundraising_assistant = FundraisingAssistant()
        self.semantic_search = SemanticSearch()
        
        print("✅ MOTHER V5 initialized successfully!")
    
    def demonstrate_capabilities(self):
        """Demonstrate V5 capabilities"""
        print("\n" + "="*70)
        print("MOTHER V5 - CAPABILITY DEMONSTRATION")
        print("="*70)
        
        # 1. Reinforcement Learning
        print("\n1. REINFORCEMENT LEARNING AGENT")
        print("-" * 70)
        
        state = State(
            task_type=TaskType.RESEARCH,
            complexity="high",
            budget="medium"
        )
        
        action = self.rl_agent.select_action(state)
        print(f"Task: Research (high complexity, medium budget)")
        print(f"Recommended action: {action.value}")
        
        # Simulate experience
        experience = Experience(
            state=state,
            action=action,
            reward=0.0,
            next_state=state,
            quality_score=0.85,
            cost=2.50
        )
        self.rl_agent.record_experience(experience)
        
        stats = self.rl_agent.get_statistics()
        print(f"Learning statistics: {stats['total_experiences']} experiences recorded")
        
        # 2. Content Generation
        print("\n2. CONTENT GENERATOR")
        print("-" * 70)
        
        request = ContentRequest(
            content_type=ContentType.BLOG_POST,
            topic="How AI Improves Geotechnical Monitoring",
            keywords=["AI", "geotechnical", "monitoring", "SHMS"],
            target_audience="Mining engineers",
            word_count=500,
            tone="professional"
        )
        
        print(f"Generating blog post: '{request.topic}'...")
        print(f"Target: {request.word_count} words, Keywords: {', '.join(request.keywords)}")
        print("✅ Content generator ready (use generate_blog_post() to create content)")
        
        # 3. Fundraising Assistant
        print("\n3. FUNDRAISING ASSISTANT")
        print("-" * 70)
        
        company_data = CompanyData(
            name="Intelltech",
            tagline="Intelligent Monitoring for Safer Operations",
            problem="Traditional monitoring is expensive and reactive",
            solution="AI-powered SHMS that predicts failures",
            market_size={"tam": "$5B", "sam": "$1B", "som": "$100M"},
            business_model="SaaS subscription",
            traction={"arr": "$2M", "customers": "20+", "growth": "300% YoY"},
            team=[{"name": "Founder", "role": "CEO", "background": "10 years experience"}],
            financials={"projections": {}, "unit_economics": {}},
            ask={"amount": "$5M", "use_of_funds": [], "milestones": []}
        )
        
        print(f"Company: {company_data.name}")
        print(f"Tagline: {company_data.tagline}")
        print("✅ Fundraising assistant ready (use generate_pitch_deck() to create deck)")
        
        # 4. Semantic Search
        print("\n4. SEMANTIC SEARCH")
        print("-" * 70)
        
        print("Semantic search ready for knowledge base queries")
        print("✅ Use search(query) to find relevant documents")
        
        print("\n" + "="*70)
        print("MOTHER V5 - ALL SYSTEMS OPERATIONAL")
        print("="*70)


def main():
    """Main entry point"""
    # Initialize MOTHER V5
    mother = MOTHERV5()
    
    # Demonstrate capabilities
    mother.demonstrate_capabilities()
    
    return mother


if __name__ == "__main__":
    mother = main()
