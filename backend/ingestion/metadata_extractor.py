"""
Metadata extraction from filenames and document structure.
"""
import re
from pathlib import Path
from typing import Dict, Optional
import uuid


class MetadataExtractor:
    """Extract and structure metadata from documents."""
    
    @staticmethod
    def extract_from_filename(filename: str, material_type: str, course: Optional[str] = None) -> Dict:
        """
        Extract metadata from filename using pattern matching.
        
        Common patterns:
        - Lecture_05_RNN.pdf -> lecture_number=5, topic=RNN
        - Chapter_7_Neural_Networks.pdf -> chapter=7, topic=Neural Networks
        - Assignment_3.pdf -> lecture_number=3
        
        Args:
            filename: Name of the file
            material_type: Type of material (lecture, textbook, etc.)
            course: Course name
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            'material_type': material_type,
            'material_title': filename,
            'course': course or 'Unknown'
        }
        
        # Extract lecture number
        lecture_match = re.search(r'[Ll]ecture[_\s-]*(\d+)', filename)
        if lecture_match:
            metadata['lecture_number'] = int(lecture_match.group(1))
        
        # Extract chapter
        chapter_match = re.search(r'[Cc]hapter[_\s-]*(\d+)', filename)
        if chapter_match:
            metadata['chapter'] = chapter_match.group(1)
        
        # Extract assignment number
        assignment_match = re.search(r'[Aa]ssignment[_\s-]*(\d+)', filename)
        if assignment_match:
            metadata['lecture_number'] = int(assignment_match.group(1))
        
        # Extract lab number
        lab_match = re.search(r'[Ll]ab[_\s-]*(\d+)', filename)
        if lab_match:
            metadata['lecture_number'] = int(lab_match.group(1))
        
        # Extract topic (text after number or between underscores)
        topic_match = re.search(r'(?:\d+[_\s-]+)([A-Za-z][A-Za-z0-9_\s-]+?)(?:\.|$)', filename)
        if topic_match:
            topic = topic_match.group(1).replace('_', ' ').replace('-', ' ').strip()
            metadata['topic'] = topic
        
        return metadata
    
    @staticmethod
    def create_chunk_metadata(
        base_metadata: Dict,
        chunk_text: str,
        section: Optional[str] = None,
        page: Optional[int] = None
    ) -> Dict:
        """
        Create full metadata for a chunk following the required schema.
        
        Args:
            base_metadata: Base metadata from file
            chunk_text: Text of the chunk
            section: Section name if available
            page: Page number if available
            
        Returns:
            Complete metadata dictionary
        """
        metadata = {
            'chunk_id': str(uuid.uuid4()),
            'course': base_metadata.get('course', 'Unknown'),
            'material_type': base_metadata.get('material_type', 'unknown'),
            'material_title': base_metadata.get('material_title', 'Unknown'),
            'material_file': base_metadata.get('material_file', ''),
            'text': chunk_text[:200] + '...' if len(chunk_text) > 200 else chunk_text  # Preview
        }
        
        # Optional fields
        if 'lecture_number' in base_metadata:
            metadata['lecture_number'] = base_metadata['lecture_number']
        
        if 'chapter' in base_metadata:
            metadata['chapter'] = base_metadata['chapter']
        
        if 'topic' in base_metadata:
            metadata['topic'] = base_metadata['topic']
        
        if section:
            metadata['section'] = section
        
        if page:
            metadata['page'] = page
        elif 'page' in base_metadata:
            metadata['page'] = base_metadata['page']
        
        return metadata
    
    @staticmethod
    def merge_metadata(base: Dict, additional: Dict) -> Dict:
        """Merge additional metadata into base metadata."""
        result = base.copy()
        result.update(additional)
        return result
