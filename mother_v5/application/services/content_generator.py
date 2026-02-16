"""
MOTHER V5 - Content Generator

Automates content creation for Intelltech lead generation.
Supports blog posts, case studies, white papers, and social media.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI


class ContentType(Enum):
    """Types of content to generate"""
    BLOG_POST = "blog_post"
    CASE_STUDY = "case_study"
    WHITE_PAPER = "white_paper"
    SOCIAL_MEDIA = "social_media"


@dataclass
class ContentRequest:
    """Request for content generation"""
    content_type: ContentType
    topic: str
    keywords: List[str]
    target_audience: str
    word_count: int = 1500
    tone: str = "professional"
    additional_context: Optional[Dict] = None


@dataclass
class GeneratedContent:
    """Generated content result"""
    title: str
    content: str
    meta_description: str
    keywords: List[str]
    seo_score: float
    estimated_read_time: int


class ContentGenerator:
    """
    Automates content creation for marketing and lead generation.
    
    Uses OpenAI for generation and knowledge base for context.
    """
    
    def __init__(self, knowledge_base_path: str = None):
        """
        Initialize Content Generator.
        
        Args:
            knowledge_base_path: Path to knowledge base directory
        """
        self.client = OpenAI()
        self.kb_path = knowledge_base_path or "/home/ubuntu/manus_global_knowledge/docs"
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[ContentType, str]:
        """Load content templates"""
        return {
            ContentType.BLOG_POST: """
# {title}

## Introduction
{introduction}

## {section_1_title}
{section_1_content}

## {section_2_title}
{section_2_content}

## {section_3_title}
{section_3_content}

## Conclusion
{conclusion}

## Call to Action
{cta}
""",
            ContentType.CASE_STUDY: """
# Case Study: {customer_name}

## Executive Summary
{executive_summary}

## Challenge
{challenge}

## Solution
{solution}

## Results
{results}

## Testimonial
"{testimonial}"
— {testimonial_author}, {testimonial_title}

## About {customer_name}
{customer_about}
""",
            ContentType.WHITE_PAPER: """
# {title}

## Abstract
{abstract}

## Table of Contents
{toc}

## Introduction
{introduction}

## Background
{background}

## Analysis
{analysis}

## Recommendations
{recommendations}

## Conclusion
{conclusion}

## References
{references}
""",
            ContentType.SOCIAL_MEDIA: """
{hook}

{body}

{cta}

{hashtags}
"""
        }
    
    def generate_blog_post(self, request: ContentRequest) -> GeneratedContent:
        """
        Generate SEO-optimized blog post.
        
        Args:
            request: Content request
            
        Returns:
            Generated content
        """
        # Research topic in knowledge base
        context = self._search_knowledge_base(request.topic)
        
        # Generate outline
        outline = self._generate_outline(request.topic, request.keywords)
        
        # Generate full post
        content = self._generate_full_content(
            content_type=ContentType.BLOG_POST,
            outline=outline,
            context=context,
            request=request
        )
        
        # Optimize for SEO
        optimized = self._optimize_seo(content, request.keywords)
        
        return optimized
    
    def generate_case_study(self, customer_data: Dict) -> GeneratedContent:
        """
        Generate customer case study.
        
        Args:
            customer_data: Customer information and results
            
        Returns:
            Generated case study
        """
        template = self.templates[ContentType.CASE_STUDY]
        
        # Generate each section
        sections = {
            "customer_name": customer_data.get("name", ""),
            "executive_summary": self._generate_section(
                "executive summary",
                customer_data,
                max_words=150
            ),
            "challenge": self._generate_section(
                "challenge",
                customer_data,
                max_words=300
            ),
            "solution": self._generate_section(
                "solution",
                customer_data,
                max_words=400
            ),
            "results": self._generate_section(
                "results",
                customer_data,
                max_words=300
            ),
            "testimonial": customer_data.get("testimonial", ""),
            "testimonial_author": customer_data.get("testimonial_author", ""),
            "testimonial_title": customer_data.get("testimonial_title", ""),
            "customer_about": self._generate_section(
                "company background",
                customer_data,
                max_words=150
            )
        }
        
        # Fill template
        content = template.format(**sections)
        
        return GeneratedContent(
            title=f"Case Study: {customer_data.get('name', '')}",
            content=content,
            meta_description=sections["executive_summary"][:160],
            keywords=["case study", "success story", customer_data.get("industry", "")],
            seo_score=0.85,
            estimated_read_time=self._calculate_read_time(content)
        )
    
    def _search_knowledge_base(self, topic: str) -> str:
        """
        Search knowledge base for relevant context.
        
        Args:
            topic: Topic to search
            
        Returns:
            Relevant context
        """
        # Simple grep-based search (can be replaced with semantic search)
        import subprocess
        
        try:
            result = subprocess.run(
                ["grep", "-r", "-i", topic, self.kb_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout[:5000]  # Limit context size
        except:
            return ""
    
    def _generate_outline(self, topic: str, keywords: List[str]) -> Dict:
        """
        Generate content outline.
        
        Args:
            topic: Main topic
            keywords: Target keywords
            
        Returns:
            Outline dictionary
        """
        prompt = f"""Generate a detailed outline for a blog post about "{topic}".
        
Target keywords: {', '.join(keywords)}

The outline should include:
1. Engaging title
2. Introduction (hook + overview)
3. 3-4 main sections with subsections
4. Conclusion
5. Call to action

Format as JSON with keys: title, introduction, sections (array), conclusion, cta"""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        # Parse response (simplified - should handle JSON parsing)
        return {"outline": response.output}
    
    def _generate_full_content(self, 
                              content_type: ContentType,
                              outline: Dict,
                              context: str,
                              request: ContentRequest) -> str:
        """
        Generate full content from outline.
        
        Args:
            content_type: Type of content
            outline: Content outline
            context: Knowledge base context
            request: Original request
            
        Returns:
            Full content
        """
        prompt = f"""Write a {request.word_count}-word {content_type.value} about "{request.topic}".

Outline:
{outline}

Context from knowledge base:
{context[:2000]}

Target audience: {request.target_audience}
Tone: {request.tone}
Keywords to include: {', '.join(request.keywords)}

Requirements:
- SEO-optimized (include keywords naturally)
- Engaging and informative
- Professional tone
- Include examples and data where relevant
- End with clear call to action"""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _generate_section(self, 
                         section_name: str,
                         data: Dict,
                         max_words: int = 300) -> str:
        """
        Generate a specific section.
        
        Args:
            section_name: Name of section
            data: Data for section
            max_words: Maximum word count
            
        Returns:
            Generated section
        """
        prompt = f"""Write the {section_name} section for a case study.

Data:
{data}

Requirements:
- Maximum {max_words} words
- Professional tone
- Specific and concrete
- Include metrics where available"""
        
        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )
        
        return response.output
    
    def _optimize_seo(self, content: str, keywords: List[str]) -> GeneratedContent:
        """
        Optimize content for SEO.
        
        Args:
            content: Generated content
            keywords: Target keywords
            
        Returns:
            Optimized content with metadata
        """
        # Extract title (first H1)
        lines = content.split('\n')
        title = next((line.strip('# ') for line in lines if line.startswith('# ')), "Untitled")
        
        # Generate meta description
        intro_paragraph = next((line for line in lines if len(line) > 50 and not line.startswith('#')), "")
        meta_description = intro_paragraph[:160]
        
        # Calculate SEO score (simplified)
        seo_score = self._calculate_seo_score(content, keywords)
        
        # Calculate read time
        read_time = self._calculate_read_time(content)
        
        return GeneratedContent(
            title=title,
            content=content,
            meta_description=meta_description,
            keywords=keywords,
            seo_score=seo_score,
            estimated_read_time=read_time
        )
    
    def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        """
        Calculate SEO score (0-1).
        
        Args:
            content: Content text
            keywords: Target keywords
            
        Returns:
            SEO score
        """
        content_lower = content.lower()
        score = 0.0
        
        # Check keyword presence
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 0.2
        
        # Check title presence
        if content.startswith('# '):
            score += 0.1
        
        # Check length (1000-2000 words is ideal)
        word_count = len(content.split())
        if 1000 <= word_count <= 2000:
            score += 0.2
        
        # Check headings
        heading_count = content.count('\n## ')
        if heading_count >= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_read_time(self, content: str) -> int:
        """
        Calculate estimated read time in minutes.
        
        Args:
            content: Content text
            
        Returns:
            Read time in minutes
        """
        word_count = len(content.split())
        return max(1, word_count // 200)  # 200 words per minute


# Example usage
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Generate blog post
    request = ContentRequest(
        content_type=ContentType.BLOG_POST,
        topic="How SHMS Improves Tailings Dam Safety",
        keywords=["SHMS", "tailings dam", "safety", "monitoring"],
        target_audience="Mining safety managers",
        word_count=1500,
        tone="professional"
    )
    
    print("Generating blog post...")
    result = generator.generate_blog_post(request)
    print(f"\nTitle: {result.title}")
    print(f"SEO Score: {result.seo_score}")
    print(f"Read Time: {result.estimated_read_time} minutes")
    print(f"\nContent preview:\n{result.content[:500]}...")
