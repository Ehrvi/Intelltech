"""
MOTHER V5 - Comprehensive Tests

Tests all V5 components.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.agents.rl_agent import RLAgent, State, TaskType, Action
from application.services.content_generator import ContentGenerator, ContentRequest, ContentType
from application.services.fundraising_assistant import FundraisingAssistant, CompanyData
from application.services.semantic_search import SemanticSearch


def test_rl_agent():
    """Test Reinforcement Learning Agent"""
    print("\n🧪 Testing RLAgent...")
    
    agent = RLAgent()
    
    # Test action selection
    state = State(
        task_type=TaskType.RESEARCH,
        complexity="high",
        budget="medium"
    )
    
    action = agent.select_action(state)
    assert isinstance(action, Action)
    print(f"✅ Action selection: {action.value}")
    
    # Test learning
    from application.agents.rl_agent import Experience
    experience = Experience(
        state=state,
        action=action,
        reward=0.0,
        next_state=state,
        quality_score=0.85,
        cost=2.50
    )
    agent.record_experience(experience)
    
    stats = agent.get_statistics()
    assert stats['total_experiences'] == 1
    print(f"✅ Learning: {stats['total_experiences']} experiences")
    
    print("✅ RLAgent: PASS")


def test_content_generator():
    """Test Content Generator"""
    print("\n🧪 Testing ContentGenerator...")
    
    generator = ContentGenerator()
    
    # Test initialization
    assert generator.client is not None
    assert generator.templates is not None
    print("✅ Initialization: PASS")
    
    # Test template loading
    assert ContentType.BLOG_POST in generator.templates
    assert ContentType.CASE_STUDY in generator.templates
    print("✅ Templates loaded: PASS")
    
    # Test SEO score calculation
    content = "# Test\n\nThis is a test article about AI and machine learning."
    score = generator._calculate_seo_score(content, ["AI", "machine learning"])
    assert 0 <= score <= 1
    print(f"✅ SEO scoring: {score:.2f}")
    
    # Test read time calculation
    read_time = generator._calculate_read_time(content)
    assert read_time > 0
    print(f"✅ Read time calculation: {read_time} min")
    
    print("✅ ContentGenerator: PASS")


def test_fundraising_assistant():
    """Test Fundraising Assistant"""
    print("\n🧪 Testing FundraisingAssistant...")
    
    assistant = FundraisingAssistant()
    
    # Test initialization
    assert assistant.client is not None
    assert assistant.slide_templates is not None
    print("✅ Initialization: PASS")
    
    # Test template loading
    assert "cover" in assistant.slide_templates
    assert "problem" in assistant.slide_templates
    assert "ask" in assistant.slide_templates
    print(f"✅ Templates loaded: {len(assistant.slide_templates)} slides")
    
    # Test cover slide generation
    company_data = CompanyData(
        name="Test Company",
        tagline="Test Tagline",
        problem="Test problem",
        solution="Test solution",
        market_size={"tam": "$1B"},
        business_model="SaaS",
        traction={"arr": "$1M"},
        team=[],
        financials={},
        ask={}
    )
    
    cover_slide = assistant._generate_cover_slide(company_data)
    assert "Test Company" in cover_slide
    assert "Test Tagline" in cover_slide
    print("✅ Slide generation: PASS")
    
    print("✅ FundraisingAssistant: PASS")


def test_semantic_search():
    """Test Semantic Search"""
    print("\n🧪 Testing SemanticSearch...")
    
    search = SemanticSearch()
    
    # Test initialization
    assert search.client is not None
    print("✅ Initialization: PASS")
    
    # Test cosine similarity
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    similarity = search._cosine_similarity(vec1, vec2)
    assert abs(similarity - 1.0) < 0.01  # Should be 1.0 (identical)
    print(f"✅ Cosine similarity: {similarity:.3f}")
    
    vec3 = [0.0, 1.0, 0.0]
    similarity2 = search._cosine_similarity(vec1, vec3)
    assert abs(similarity2) < 0.01  # Should be 0.0 (orthogonal)
    print(f"✅ Orthogonal vectors: {similarity2:.3f}")
    
    print("✅ SemanticSearch: PASS")


def test_integration():
    """Test component integration"""
    print("\n🧪 Testing Integration...")
    
    # Import main system
    from main import MOTHERV5
    
    mother = MOTHERV5()
    
    # Test all components initialized
    assert mother.rl_agent is not None
    assert mother.content_generator is not None
    assert mother.fundraising_assistant is not None
    assert mother.semantic_search is not None
    print("✅ All components initialized")
    
    print("✅ Integration: PASS")


def main():
    """Run all tests"""
    print("="*70)
    print("MOTHER V5 - TEST SUITE")
    print("="*70)
    
    tests = [
        test_rl_agent,
        test_content_generator,
        test_fundraising_assistant,
        test_semantic_search,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
