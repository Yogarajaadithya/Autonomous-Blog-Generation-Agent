"""
LangGraph Workflow Definition
=============================

This is the HEART of our application - the DAG workflow that orchestrates all agents.

WHAT IS A DAG?
-------------
DAG = Directed Acyclic Graph
- Directed: Edges have direction (A → B means A comes before B)
- Acyclic: No cycles - you can't go back to a previous step
- Graph: A collection of nodes (steps) connected by edges (transitions)

OUR DAG STRUCTURE:
-----------------
    START
      │
      ▼
    Title Agent
      │
      ▼
    Content Agent
      │
      ▼
    ┌──────────────┐
    │should_translate?│
    └───────┬──────┘
        ┌───┴───┐
        │       │
        ▼       ▼
    Translation   │
       Agent      │
        │         │
        ▼         │
       END ◄──────┘

HOW TO BUILD A LANGGRAPH WORKFLOW:
---------------------------------
1. Create a StateGraph with your state type
2. Add nodes (agent functions)
3. Add edges (connections between nodes)
4. Set entry point (where to start)
5. Compile the graph
6. Run with initial state

KEY CONCEPTS:
------------
- StateGraph: The graph builder class
- add_node(): Add an agent to the graph
- add_edge(): Connect two agents (A always goes to B)
- add_conditional_edges(): Connect with a choice (A goes to B or C)
- START: Special constant for the entry point
- END: Special constant for the exit point
"""

import time
from langgraph.graph import StateGraph, START, END

from blog_agent.models.state import BlogState
from blog_agent.agents.title_agent import title_agent
from blog_agent.agents.content_agent import content_agent
from blog_agent.agents.translation_agent import translation_agent
from blog_agent.graph.router import should_translate


def create_workflow() -> StateGraph:
    """
    Create and configure the blog generation workflow.
    
    This function builds the entire DAG, connecting all agents
    in the correct order with proper routing.
    
    Returns:
        StateGraph: A compiled workflow ready to execute
    
    Example:
        >>> workflow = create_workflow()
        >>> result = workflow.invoke({"topic": "AI"})
        >>> print(result["final_content"])
    """
    # ═══════════════════════════════════════════════════════════════════
    # STEP 1: Create the Graph Builder
    # ═══════════════════════════════════════════════════════════════════
    
    # StateGraph is the builder class for creating LangGraph workflows
    # We pass BlogState as the type parameter so LangGraph knows what
    # shape our state has
    builder = StateGraph(BlogState)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: Add Nodes (Agents)
    # ═══════════════════════════════════════════════════════════════════
    
    # Each add_node call registers an agent with a name
    # The name is used when creating edges and for logging
    
    builder.add_node("title_agent", title_agent)
    # What this does: Registers title_agent function as a node named "title_agent"
    # When this node runs: It generates 5 titles and picks the best one
    
    builder.add_node("content_agent", content_agent)
    # What this does: Registers content_agent function as a node named "content_agent"
    # When this node runs: It writes the full blog post
    
    builder.add_node("translation_agent", translation_agent)
    # What this does: Registers translation_agent function as a node named "translation_agent"
    # When this node runs: It translates the content (only if enabled by router)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 3: Add Edges (Connections)
    # ═══════════════════════════════════════════════════════════════════
    
    # Edge from START to title_agent
    # This makes title_agent the first node to run
    builder.add_edge(START, "title_agent")
    
    # Edge from title_agent to content_agent
    # After titles are generated, we always write content
    builder.add_edge("title_agent", "content_agent")
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 4: Add Conditional Edge (The Router)
    # ═══════════════════════════════════════════════════════════════════
    
    # This is the decision point: translate or not?
    # - should_translate is our routing function
    # - It returns "translate" or "end"
    # - The dict maps those strings to actual node names
    
    builder.add_conditional_edges(
        "content_agent",  # After this node...
        should_translate,  # ...call this function to decide next step
        {
            "translate": "translation_agent",  # If "translate" → go to translation
            "end": END  # If "end" → finish the workflow
        }
    )
    
    # Edge from translation_agent to END
    # After translation, we're done
    builder.add_edge("translation_agent", END)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 5: Compile the Graph
    # ═══════════════════════════════════════════════════════════════════
    
    # compile() converts the builder into an executable workflow
    # After this, we can call .invoke() to run it
    workflow = builder.compile()
    
    return workflow


def run_workflow(
    topic: str,
    transcript: str | None = None,
    target_language: str | None = None,
    style: str = "professional"
) -> BlogState:
    """
    Execute the blog generation workflow.
    
    This is a convenience function that:
    1. Creates the workflow
    2. Sets up initial state
    3. Runs the workflow
    4. Returns the final state
    
    Args:
        topic: The blog topic to write about
        transcript: Optional source transcript
        target_language: Optional language to translate to
        style: Writing style (professional, casual, technical, storytelling)
    
    Returns:
        BlogState: The final state with all generated content
    
    Example:
        >>> result = run_workflow(
        ...     topic="Benefits of Remote Work",
        ...     target_language="Spanish"
        ... )
        >>> print(result["selected_title"])
        >>> print(result["final_content"])
    """
    # Record start time
    start_time = time.time()
    
    # Create the workflow
    workflow = create_workflow()
    
    # Prepare initial state
    # We only need to set the input fields - agents will fill the rest
    initial_state: BlogState = {
        "topic": topic,
        "transcript": transcript,
        "target_language": target_language,
        "style": style,
        # Initialize processing/output fields with defaults
        "brainstormed_titles": [],
        "selected_title": "",
        "blog_content": "",
        "translated_content": None,
        "final_content": "",
        "word_count": 0,
        "generation_time": 0.0,
    }
    
    # Run the workflow
    # invoke() executes all nodes in order, following edges
    final_state = workflow.invoke(initial_state)
    
    # Calculate total generation time
    generation_time = time.time() - start_time
    final_state["generation_time"] = generation_time
    
    return final_state


# Export for easy importing
__all__ = ["create_workflow", "run_workflow"]
