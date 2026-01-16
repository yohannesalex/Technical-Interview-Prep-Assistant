"""
System prompts for the LLM with strict citation requirements.
"""


SYSTEM_PROMPT = """You are a technical interview preparation assistant. Your role is to help students prepare for technical interviews by answering questions ONLY using the provided course materials.

CRITICAL RULES:
1. Answer ONLY based on the provided context. Never use general knowledge or information not in the context.
2. Every factual claim must cite its source using the format: [Material Title, Page X] or [Material Title, Section Y]
3. If the information is not in the provided context, you MUST respond: "I don't have this information in the provided materials."
4. If sources conflict, present both viewpoints with their respective citations.
5. Never hallucinate or make up citations.

OUTPUT FORMAT:
- Provide a brief, clear answer in bullet points or short paragraphs
- After the answer, include a "Sources:" section listing all citations
- Be concise but complete

Example response:
"A binary search tree (BST) is a data structure where each node has at most two children, and for each node, all values in the left subtree are smaller and all values in the right subtree are larger [Data Structures Lecture, Page 45].

The time complexity for search operations is O(log n) in the average case for balanced trees [Algorithms Textbook, Chapter 7, Section 3.2].

Sources:
- Data Structures Lecture, Page 45
- Algorithms Textbook, Chapter 7, Section 3.2"
"""


def create_rag_prompt(question: str, context_chunks: list) -> str:
    """
    Create a RAG prompt with question and context.
    
    Args:
        question: User's question
        context_chunks: List of context dictionaries with 'text' and 'metadata'
        
    Returns:
        Formatted prompt
    """
    # Build context section
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        metadata = chunk.get('metadata', {})
        text = chunk.get('text', '')
        
        # Format source info
        source_info = metadata.get('material_title', 'Unknown')
        if 'page' in metadata:
            source_info += f", Page {metadata['page']}"
        elif 'section' in metadata:
            source_info += f", Section: {metadata['section']}"
        
        context_parts.append(f"[Source {i}: {source_info}]\n{text}\n")
    
    context = "\n".join(context_parts)
    
    prompt = f"""Context from course materials:

{context}

Question: {question}

Provide a clear, concise answer based ONLY on the context above. Include citations for all claims."""
    
    return prompt


def extract_refusal_keywords(response: str) -> bool:
    """
    Check if the response indicates the LLM refused to answer.
    
    Args:
        response: LLM response
        
    Returns:
        True if response is a refusal
    """
    refusal_phrases = [
        "don't have this information",
        "not in the provided materials",
        "cannot find",
        "not mentioned in the context",
        "no information about",
        "context does not contain"
    ]
    
    response_lower = response.lower()
    return any(phrase in response_lower for phrase in refusal_phrases)
