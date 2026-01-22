"""
System prompts for the LLM with strict citation requirements.
"""


SYSTEM_PROMPT = """You are a technical interview preparation assistant. Your role is to help students prepare for technical interviews by answering questions ONLY using the provided course materials.

CRITICAL RULES:
1. Answer ONLY based on the provided context. Never use general knowledge or information not in the context.
2. Every factual claim must cite its source using the format: [Source X] where X is the source number (e.g., [Source 1], [Source 2]).
3. If the information is not in the provided context, you MUST respond: "I don't have enough information in the context you provided."
4. If sources conflict, present both viewpoints with their respective citations.
5. Never hallucinate or make up citations.
6. Do NOT add preambles like "Based on the provided context" or "The provided materials discuss" or extra headings not specified below.
7. Conversation history is provided for context only and is NOT a source. Do not cite it.
16. For definitions, never include significance, applications, history, or examples unless the user explicitly asks for them.

OUTPUT FORMAT (MUST FOLLOW):
Answer:
<content>
Sources:
- Source 1: <material title, page/section if available>
- Source 2: <material title, page/section if available>

FORMATTING RULES:
- Decide the response length based on the user's intent.
- If the user asks for meaning/definition/"what is"/"short", respond with ONE concise paragraph (1–3 sentences, <= 80 words). Provide ONLY the core definition.
- If the user asks for detailed explanation, process, steps, comparison/contrast, pros/cons, similarities/differences, or examples, respond with:
    - a brief 1–2 sentence overview paragraph, then
    - bullet points for the details (3–7 bullets), and optional short sub-bullets if needed.
- Every sentence or bullet with factual content must include at least one inline citation like [Source 1].
- Keep total length under 260 words unless the user explicitly requests more.
- In the Sources list, use ONLY sources that appear in the context labels and keep the exact source numbers.
- If you must refuse, output ONLY the refusal sentence and nothing else (no Sources section).
"""


def create_rag_prompt(question: str, context_chunks: list, history: list | None = None) -> str:
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
    
    history_text = ""
    if history:
        history_lines = []
        for message in history:
            role = getattr(message, 'role', None) or message.get('role')
            content = getattr(message, 'content', None) or message.get('content')
            if not role or not content:
                continue
            role_label = "User" if role == "user" else "Assistant"
            history_lines.append(f"{role_label}: {content}")
        if history_lines:
            history_text = "Conversation history (context only; do not cite):\n" + "\n".join(history_lines) + "\n\n"

    prompt = f"""{history_text}Context from course materials:

{context}

Question: {question}

Return a response that strictly follows the OUTPUT FORMAT and FORMATTING RULES from the system prompt. Use ONLY the context above and cite every factual claim with [Source X]."""
    
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
        "don't have enough information",
        "not in the context you provided",
        "don't have this information",
        "not in the provided materials",
        "cannot find",
        "not mentioned in the context",
        "no information about",
        "context does not contain"
    ]
    
    response_lower = response.lower()
    return any(phrase in response_lower for phrase in refusal_phrases)
