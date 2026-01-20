"""
Title Generation Prompts
========================

This module contains the prompts used by the Title Brainstorming Agent.

WHY PROMPTS MATTER:
------------------
The quality of AI output depends heavily on how you ask for it.
Good prompts:
- Are specific about what you want
- Give examples
- Define the format of the output
- Include constraints (length, style, etc.)

WHY SEPARATE PROMPTS FROM AGENTS?
--------------------------------
1. Easy to update prompts without touching agent code
2. Can A/B test different prompts
3. Non-developers can review/edit prompts
4. Keeps agent code clean and focused
"""

# System prompt sets the "personality" of the AI
TITLE_SYSTEM_PROMPT = """You are an expert blog title writer with years of experience in SEO and content marketing.

Your titles are:
- Attention-grabbing (make people WANT to click)
- SEO-friendly (include relevant keywords naturally)
- Clear and specific (reader knows what they'll learn)
- Appropriately formatted (use numbers, power words)

You understand different writing styles:
- Professional: Industry terms, authoritative tone
- Casual: Friendly, conversational, relatable
- Technical: Precise, detailed, jargon-appropriate
- Storytelling: Narrative hooks, curiosity-building"""


TITLE_GENERATION_PROMPT = """Generate 5 creative and engaging blog post titles for the following topic.

TOPIC: {topic}

{transcript_section}

WRITING STYLE: {style}

REQUIREMENTS:
1. Generate exactly 5 title options
2. Each title should be unique in approach
3. Use proven title formats (how-to, listicles, questions, etc.)
4. Keep titles under 60 characters for SEO
5. Include power words that trigger emotion

TITLE TYPES TO INCLUDE:
- One "How to..." title
- One numbered list title (e.g., "10 Ways to...")
- One question-based title
- One benefit-focused title
- One creative/unique title

OUTPUT FORMAT:
Return ONLY the 5 titles, one per line, numbered 1-5.
Do not include any explanation or additional text.

Example output:
1. How to Master Remote Work in 30 Days
2. 7 Secrets Top Remote Workers Never Share
3. Why Are Remote Workers 40% More Productive?
4. The Ultimate Guide to Work-From-Home Success
5. Remote Work Revolution: Transform Your Career Today
"""


TITLE_SELECTION_PROMPT = """From the following title options, select the BEST one for SEO and engagement.

TITLES:
{titles}

TOPIC: {topic}
STYLE: {style}

Consider:
1. SEO value (keywords, length, searchability)
2. Click-through potential (would YOU click this?)
3. Accuracy (does it promise something the content can deliver?)
4. Style match (does it fit the requested writing style?)

OUTPUT FORMAT:
Return ONLY the single best title, nothing else.
"""


# Export for easy importing
__all__ = [
    "TITLE_SYSTEM_PROMPT",
    "TITLE_GENERATION_PROMPT",
    "TITLE_SELECTION_PROMPT"
]
