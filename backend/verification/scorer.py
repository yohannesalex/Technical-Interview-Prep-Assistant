"""
Faithfulness scoring and threshold-based decision making.
"""
from typing import Dict
import sys
sys.path.append('..')
from config import FAITHFULNESS_THRESHOLD, VERIFICATION_ENABLED


class FaithfulnessScorer:
    """Score and evaluate faithfulness of generated answers."""
    
    def __init__(self, threshold: float = FAITHFULNESS_THRESHOLD):
        """
        Initialize scorer.
        
        Args:
            threshold: Minimum faithfulness score to pass (0-1)
        """
        self.threshold = threshold
        self.enabled = VERIFICATION_ENABLED
    
    def evaluate(self, verification_report: Dict) -> Dict:
        """
        Evaluate verification report and make decision.
        
        Args:
            verification_report: Report from FaithfulnessChecker
            
        Returns:
            Evaluation dictionary with status and decision
        """
        if not self.enabled:
            return {
                'status': 'disabled',
                'passed': True,
                'message': 'Verification disabled'
            }
        
        score = verification_report.get('faithfulness_score', 0.0)
        unsupported = verification_report.get('unsupported_sentences', [])
        
        if score >= self.threshold:
            status = 'passed'
            passed = True
            message = f'Answer is faithful to sources (score: {score:.2f})'
        elif score >= self.threshold * 0.7:  # Warning zone
            status = 'warning'
            passed = True
            message = f'Answer partially supported (score: {score:.2f}). Some claims may not be fully verified.'
        else:
            status = 'failed'
            passed = False
            message = f'Answer has low faithfulness score ({score:.2f}). Many claims are not supported by the provided materials.'
        
        return {
            'status': status,
            'passed': passed,
            'message': message,
            'score': score,
            'unsupported_count': len(unsupported)
        }
    
    def should_refuse(self, evaluation: Dict) -> bool:
        """
        Determine if answer should be refused based on evaluation.
        
        Args:
            evaluation: Evaluation dictionary
            
        Returns:
            True if answer should be refused
        """
        return not evaluation.get('passed', True)
    
    def create_refusal_message(self, evaluation: Dict) -> str:
        """
        Create a refusal message.
        
        Args:
            evaluation: Evaluation dictionary
            
        Returns:
            Refusal message
        """
        return (
            "I cannot provide a reliable answer to this question based on the available materials. "
            f"The generated response had a low faithfulness score ({evaluation.get('score', 0):.2f}), "
            "indicating that many claims could not be verified against the source documents. "
            "Please try rephrasing your question or check if the relevant materials have been uploaded."
        )


def get_scorer() -> FaithfulnessScorer:
    """Get a faithfulness scorer instance."""
    return FaithfulnessScorer()
