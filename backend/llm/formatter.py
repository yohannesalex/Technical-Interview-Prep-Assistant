"""
Answer formatting and citation extraction.
"""
import re
from typing import List, Dict, Tuple


class AnswerFormatter:
    """Format and parse LLM responses."""
    
    @staticmethod
    def extract_citations(response: str) -> Tuple[str, List[str]]:
        """
        Extract citations from response.
        
        Args:
            response: LLM response
            
        Returns:
            Tuple of (answer_text, list_of_citations)
        """
        # Split on "Sources:" or "References:" section
        sources_pattern = r'\n\s*(Sources?|References?):\s*\n'
        parts = re.split(sources_pattern, response, flags=re.IGNORECASE)
        
        if len(parts) >= 3:
            # Answer is before the sources section
            answer = parts[0].strip()
            # Citations are after
            citations_text = parts[2].strip()
            citations = AnswerFormatter._parse_citations(citations_text)
        else:
            # No explicit sources section, try to extract inline citations
            answer = response.strip()
            citations = AnswerFormatter._extract_inline_citations(answer)
        
        return answer, citations
    
    @staticmethod
    def _parse_citations(citations_text: str) -> List[str]:
        """Parse citations from sources section."""
        citations = []
        # Split by newlines or bullet points
        lines = citations_text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Remove bullet points or dashes
            line = re.sub(r'^[-•*]\s*', '', line)
            if line:
                citations.append(line)
        
        return citations
    
    @staticmethod
    def _extract_inline_citations(text: str) -> List[str]:
        """Extract inline citations in [Source, Page X] format."""
        # Pattern: [anything, Page/Section ...]
        pattern = r'\[([^\]]+(?:Page|Section|Chapter)[^\]]+)\]'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        return list(set(matches))  # Remove duplicates
    
    @staticmethod
    def format_response(answer: str, sources: List[Dict]) -> str:
        """
        Format a response with answer and sources.
        
        Args:
            answer: Answer text
            sources: List of source dictionaries
            
        Returns:
            Formatted response
        """
        response = answer + "\n\nSources:\n"
        
        for source in sources:
            metadata = source.get('metadata', {})
            title = metadata.get('material_title', 'Unknown')
            
            source_line = f"- {title}"
            if 'page' in metadata:
                source_line += f", Page {metadata['page']}"
            elif 'section' in metadata:
                source_line += f", Section: {metadata['section']}"
            
            response += source_line + "\n"
        
        return response
