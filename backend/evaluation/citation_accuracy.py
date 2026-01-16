"""
Citation accuracy evaluation script.
"""
import sys
sys.path.append('..')
from db import get_db, models
from llm import AnswerFormatter
from typing import List, Dict
import json
from pathlib import Path
from config import LOGS_DIR


def evaluate_citation_accuracy(query_log_ids: List[int]):
    """
    Evaluate citation accuracy for query logs.
    
    Args:
        query_log_ids: List of query log IDs to evaluate
        
    Returns:
        Evaluation results
    """
    db = next(get_db())
    results = []
    
    for log_id in query_log_ids:
        log = db.query(models.QueryLog).filter(models.QueryLog.id == log_id).first()
        
        if not log:
            continue
        
        # Extract citations from answer
        answer = log.answer or ""
        _, citations = AnswerFormatter.extract_citations(answer)
        
        # Get sources from log
        sources = log.sources or []
        
        # Check if citations match sources
        cited_materials = set()
        for citation in citations:
            # Extract material title from citation
            # Simple heuristic: first part before comma
            parts = citation.split(',')
            if parts:
                cited_materials.add(parts[0].strip())
        
        source_materials = set()
        for source in sources:
            if isinstance(source, dict):
                source_materials.add(source.get('material_title', ''))
        
        # Calculate accuracy
        if len(source_materials) > 0:
            accuracy = len(cited_materials & source_materials) / len(source_materials)
        else:
            accuracy = 0.0
        
        results.append({
            'log_id': log_id,
            'question': log.question,
            'citations_found': len(citations),
            'sources_used': len(sources),
            'accuracy': accuracy,
            'cited_materials': list(cited_materials),
            'source_materials': list(source_materials)
        })
    
    return results


def save_citation_results(results: List[Dict], filename: str = "citation_accuracy.json"):
    """Save citation evaluation results."""
    logs_path = Path(LOGS_DIR) / filename
    with open(logs_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {logs_path}")


if __name__ == "__main__":
    # Example: evaluate recent query logs
    db = next(get_db())
    recent_logs = db.query(models.QueryLog).order_by(models.QueryLog.timestamp.desc()).limit(10).all()
    log_ids = [log.id for log in recent_logs]
    
    print(f"Evaluating citation accuracy for {len(log_ids)} queries...")
    results = evaluate_citation_accuracy(log_ids)
    
    print("\nResults:")
    for result in results:
        print(f"Log {result['log_id']}: Accuracy = {result['accuracy']:.2f}, "
              f"Citations = {result['citations_found']}, Sources = {result['sources_used']}")
    
    avg_accuracy = sum(r['accuracy'] for r in results) / len(results) if results else 0.0
    print(f"\nAverage Citation Accuracy: {avg_accuracy:.3f}")
    
    save_citation_results(results)
