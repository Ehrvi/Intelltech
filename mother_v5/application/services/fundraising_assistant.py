"""
MOTHER V5 - Fundraising Assistant

Automates fundraising preparation and execution for Intelltech.
Supports pitch deck generation, investor targeting, and due diligence.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI
import json


class InvestorStage(Enum):
    """Investor stage focus"""
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    GROWTH = "growth"


@dataclass
class CompanyData:
    """Company information for fundraising"""
    name: str
    tagline: str
    problem: str
    solution: str
    market_size: str
    business_model: str
    traction: Dict  # ARR, customers, growth rate
    team: List[Dict]  # Name, role, background
    financials: Dict  # Revenue, expenses, runway
    ask: Dict  # Amount, use of funds
    

@dataclass
class Investor:
    """Investor information"""
    name: str
    firm: str
    stage: InvestorStage
    sectors: List[str]
    check_size: str
    portfolio: List[str]
    contact: Optional[str] = None
    score: float = 0.0


class FundraisingAssistant:
    """
    Automates fundraising preparation and execution.
    
    Generates pitch decks, researches investors, and prepares due diligence materials.
    """
    
    def __init__(self):
        """Initialize Fundraising Assistant"""
        self.client = OpenAI()
        self.slide_templates = self._load_slide_templates()
    
    def _load_slide_templates(self) -> Dict[str, str]:
        """Load pitch deck slide templates"""
        return {
            "cover": "# {company_name}\n\n**{tagline}**\n\n{date}",
            "problem": "# The Problem\n\n{problem_statement}\n\n**Market Pain:**\n{pain_points}",
            "solution": "# Our Solution\n\n{solution_description}\n\n**Key Benefits:**\n{benefits}",
            "market": "# Market Opportunity\n\n**TAM:** {tam}\n**SAM:** {sam}\n**SOM:** {som}\n\n{market_trends}",
            "product": "# Product\n\n{product_description}\n\n**Key Features:**\n{features}",
            "business_model": "# Business Model\n\n{model_description}\n\n**Revenue Streams:**\n{revenue_streams}",
            "traction": "# Traction\n\n**ARR:** {arr}\n**Customers:** {customers}\n**Growth:** {growth}\n\n{milestones}",
            "competition": "# Competition\n\n{competitive_landscape}\n\n**Our Advantage:**\n{competitive_advantage}",
            "team": "# Team\n\n{team_members}\n\n**Advisors:**\n{advisors}",
            "financials": "# Financials\n\n{financial_projections}\n\n**Unit Economics:**\n{unit_economics}",
            "ask": "# The Ask\n\n**Raising:** {amount}\n\n**Use of Funds:**\n{use_of_funds}\n\n**Milestones:**\n{milestones}",
            "vision": "# Vision\n\n{long_term_vision}\n\n**Join us in {mission}**"
        }
    
    def generate_pitch_deck(self, company_data: CompanyData) -> Dict[str, str]:
        """
        Generate investor-ready pitch deck.
        
        Args:
            company_data: Company information
            
        Returns:
            Dictionary of slides (slide_name -> content)
        """
        slides = {}
        
        # 1. Cover slide
        slides["01_cover"] = self._generate_cover_slide(company_data)
        
        # 2. Problem slide
        slides["02_problem"] = self._generate_problem_slide(company_data)
        
        # 3. Solution slide
        slides["03_solution"] = self._generate_solution_slide(company_data)
        
        # 4. Market slide
        slides["04_market"] = self._generate_market_slide(company_data)
        
        # 5. Product slide
        slides["05_product"] = self._generate_product_slide(company_data)
        
        # 6. Business model slide
        slides["06_business_model"] = self._generate_business_model_slide(company_data)
        
        # 7. Traction slide
        slides["07_traction"] = self._generate_traction_slide(company_data)
        
        # 8. Competition slide
        slides["08_competition"] = self._generate_competition_slide(company_data)
        
        # 9. Team slide
        slides["09_team"] = self._generate_team_slide(company_data)
        
        # 10. Financials slide
        slides["10_financials"] = self._generate_financials_slide(company_data)
        
        # 11. Ask slide
        slides["11_ask"] = self._generate_ask_slide(company_data)
        
        # 12. Vision slide
        slides["12_vision"] = self._generate_vision_slide(company_data)
        
        return slides
    
    def _generate_cover_slide(self, data: CompanyData) -> str:
        """Generate cover slide"""
        from datetime import datetime
        return self.slide_templates["cover"].format(
            company_name=data.name,
            tagline=data.tagline,
            date=datetime.now().strftime("%B %Y")
        )
    
    def _generate_problem_slide(self, data: CompanyData) -> str:
        """Generate problem slide"""
        # Use OpenAI to expand problem statement
        prompt = f"""Expand this problem statement into a compelling pitch deck slide:

Problem: {data.problem}

Include:
1. Clear problem statement (1-2 sentences)
2. 3-4 specific pain points
3. Quantify the impact where possible

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_solution_slide(self, data: CompanyData) -> str:
        """Generate solution slide"""
        prompt = f"""Create a solution slide for a pitch deck:

Solution: {data.solution}

Include:
1. Clear solution description (2-3 sentences)
2. 3-4 key benefits
3. Why now? (timing/technology enablers)

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_market_slide(self, data: CompanyData) -> str:
        """Generate market slide"""
        return self.slide_templates["market"].format(
            tam=data.market_size.get("tam", ""),
            sam=data.market_size.get("sam", ""),
            som=data.market_size.get("som", ""),
            market_trends=data.market_size.get("trends", "")
        )
    
    def _generate_product_slide(self, data: CompanyData) -> str:
        """Generate product slide"""
        prompt = f"""Create a product slide for a pitch deck:

Solution: {data.solution}

Include:
1. Product description (2-3 sentences)
2. Key features (3-4 bullet points)
3. Demo/screenshot description

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_business_model_slide(self, data: CompanyData) -> str:
        """Generate business model slide"""
        prompt = f"""Create a business model slide for a pitch deck:

Business Model: {data.business_model}

Include:
1. How we make money (1-2 sentences)
2. Revenue streams (2-3 bullet points)
3. Pricing strategy

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_traction_slide(self, data: CompanyData) -> str:
        """Generate traction slide"""
        traction = data.traction
        return self.slide_templates["traction"].format(
            arr=traction.get("arr", ""),
            customers=traction.get("customers", ""),
            growth=traction.get("growth", ""),
            milestones="\n".join(f"- {m}" for m in traction.get("milestones", []))
        )
    
    def _generate_competition_slide(self, data: CompanyData) -> str:
        """Generate competition slide"""
        prompt = f"""Create a competition slide for a pitch deck:

Solution: {data.solution}
Market: {data.market_size}

Include:
1. Competitive landscape (2-3 sentences)
2. Key competitors (2-3)
3. Our competitive advantage (3-4 points)

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_team_slide(self, data: CompanyData) -> str:
        """Generate team slide"""
        team_members = "\n\n".join([
            f"**{member['name']}** - {member['role']}\n{member['background']}"
            for member in data.team
        ])
        
        return self.slide_templates["team"].format(
            team_members=team_members,
            advisors="[To be added]"
        )
    
    def _generate_financials_slide(self, data: CompanyData) -> str:
        """Generate financials slide"""
        financials = data.financials
        return self.slide_templates["financials"].format(
            financial_projections=json.dumps(financials.get("projections", {}), indent=2),
            unit_economics=json.dumps(financials.get("unit_economics", {}), indent=2)
        )
    
    def _generate_ask_slide(self, data: CompanyData) -> str:
        """Generate ask slide"""
        ask = data.ask
        return self.slide_templates["ask"].format(
            amount=ask.get("amount", ""),
            use_of_funds="\n".join(f"- {item}" for item in ask.get("use_of_funds", [])),
            milestones="\n".join(f"- {item}" for item in ask.get("milestones", []))
        )
    
    def _generate_vision_slide(self, data: CompanyData) -> str:
        """Generate vision slide"""
        prompt = f"""Create a vision slide for a pitch deck:

Company: {data.name}
Solution: {data.solution}

Include:
1. Long-term vision (3-5 years)
2. Impact on the industry
3. Inspiring call to action

Format as markdown."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def research_investors(self, criteria: Dict) -> List[Investor]:
        """
        Find and prioritize target investors.
        
        Args:
            criteria: Search criteria (stage, sectors, check_size, geography)
            
        Returns:
            List of scored investors
        """
        # Use OpenAI to generate investor list based on criteria
        prompt = f"""Generate a list of 20 venture capital investors matching these criteria:

Stage: {criteria.get('stage', '')}
Sectors: {', '.join(criteria.get('sectors', []))}
Check Size: {criteria.get('check_size', '')}
Geography: {criteria.get('geography', '')}

For each investor, provide:
1. Name
2. Firm
3. Stage focus
4. Sectors
5. Typical check size
6. Notable portfolio companies

Format as JSON array."""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        # Parse response (simplified - should handle JSON parsing)
        # In production, this would query databases like Crunchbase, PitchBook
        investors = []
        
        # Score investors based on fit
        for inv_data in []:  # Would parse from response
            investor = Investor(
                name=inv_data.get("name", ""),
                firm=inv_data.get("firm", ""),
                stage=InvestorStage(inv_data.get("stage", "seed")),
                sectors=inv_data.get("sectors", []),
                check_size=inv_data.get("check_size", ""),
                portfolio=inv_data.get("portfolio", [])
            )
            investor.score = self._score_investor(investor, criteria)
            investors.append(investor)
        
        return sorted(investors, key=lambda x: x.score, reverse=True)
    
    def _score_investor(self, investor: Investor, criteria: Dict) -> float:
        """
        Score investor fit (0-1).
        
        Args:
            investor: Investor data
            criteria: Search criteria
            
        Returns:
            Fit score
        """
        score = 0.0
        
        # Stage match
        if investor.stage.value == criteria.get("stage"):
            score += 0.3
        
        # Sector match
        target_sectors = set(criteria.get("sectors", []))
        investor_sectors = set(investor.sectors)
        sector_overlap = len(target_sectors & investor_sectors) / len(target_sectors)
        score += 0.4 * sector_overlap
        
        # Check size match (simplified)
        score += 0.2
        
        # Portfolio relevance (simplified)
        score += 0.1
        
        return score


# Example usage
if __name__ == "__main__":
    assistant = FundraisingAssistant()
    
    # Example company data
    company_data = CompanyData(
        name="Intelltech",
        tagline="Intelligent Monitoring for Safer Operations",
        problem="Traditional geotechnical monitoring is expensive, slow, and reactive",
        solution="AI-powered SHMS that predicts failures before they happen at 10x lower cost",
        market_size={"tam": "$5B", "sam": "$1B", "som": "$100M"},
        business_model="SaaS subscription model",
        traction={
            "arr": "$2M",
            "customers": "20+",
            "growth": "300% YoY",
            "milestones": ["Launched product", "First enterprise customer", "Expanded to 3 countries"]
        },
        team=[
            {"name": "Founder 1", "role": "CEO", "background": "10 years in mining technology"},
            {"name": "Founder 2", "role": "CTO", "background": "PhD in AI, ex-Google"}
        ],
        financials={
            "projections": {"Y1": "$5M", "Y2": "$15M", "Y3": "$40M"},
            "unit_economics": {"LTV": "$500K", "CAC": "$50K", "LTV:CAC": "10:1"}
        },
        ask={
            "amount": "$5M Series A",
            "use_of_funds": ["Product development (40%)", "Sales & marketing (40%)", "Operations (20%)"],
            "milestones": ["Reach $10M ARR", "Expand to 5 countries", "Launch v2.0"]
        }
    )
    
    print("Generating pitch deck...")
    slides = assistant.generate_pitch_deck(company_data)
    print(f"\nGenerated {len(slides)} slides")
    print(f"\nCover slide:\n{slides['01_cover']}")
