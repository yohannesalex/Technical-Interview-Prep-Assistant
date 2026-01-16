"""
Recall@K evaluation script for retrieval quality testing.
"""
import sys
sys.path.append('..')
from retrieval import get_embedder, get_vector_store
from db import get_db, models
from typing import List, Dict
import json
from pathlib import Path
from config import LOGS_DIR


def evaluate_recall_at_k(test_queries: List[Dict], k_values: List[int] = [5, 10, 12, 20]):
    """
    Evaluate Recall@K for test queries.
    
    Args:
        test_queries: List of dicts with 'query' and 'relevant_chunk_ids'
        k_values: List of K values to test
        
    Returns:
        Evaluation results
    """
    embedder = get_embedder()
    vector_store = get_vector_store()
    
    results = {k: [] for k in k_values}
    
    for test_query in test_queries:
        query = test_query['query']
        relevant_ids = set(test_query['relevant_chunk_ids'])
        
        # Embed query
        query_emb = embedder.embed_text(query)
        
        # Retrieve for each K
        for k in k_values:
            retrieved = vector_store.search(query_emb, top_k=k)
            retrieved_ids = set([chunk_id for chunk_id, _ in retrieved])
            
            # Calculate recall
            if len(relevant_ids) > 0:
                recall = len(retrieved_ids & relevant_ids) / len(relevant_ids)
            else:
                recall = 0.0
            
            results[k].append(recall)
    
    # Calculate average recall for each K
    avg_results = {k: sum(recalls) / len(recalls) if recalls else 0.0 
                   for k, recalls in results.items()}
    
    return avg_results


def save_evaluation_results(results: Dict, filename: str = "recall_at_k.json"):
    """Save evaluation results to logs directory."""
    logs_path = Path(LOGS_DIR) / filename
    with open(logs_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {logs_path}")


if __name__ == "__main__":
    # Example test queries (you should customize these)
    test_queries = [
        {
            "query": "What is backpropagation?",
            "relevant_chunk_ids": []  # Add actual chunk IDs from your database
        },
        # Add more test queries
    ]
    
    print("Running Recall@K evaluation...")
    results = evaluate_recall_at_k(test_queries)
    
    print("\nResults:")
    for k, recall in results.items():
        print(f"Recall@{k}: {recall:.3f}")
    
    save_evaluation_results(results)
