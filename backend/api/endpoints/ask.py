"""
/ask endpoint - Main query endpoint with RAG pipeline.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
sys.path.append('../..')
from db import get_db, crud, schema
from retrieval import get_embedder, get_vector_store, MetadataFilter
from llm import get_ollama_client, SYSTEM_PROMPT, create_rag_prompt, extract_refusal_keywords
from verification import get_faithfulness_checker, get_scorer
from config import TOP_K

router = APIRouter()


@router.post("/ask", response_model=schema.QueryResponse)
async def ask_question(
    request: schema.QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Answer a question using RAG.
    
    Args:
        request: Query request with question and optional filters
        db: Database session
        
    Returns:
        Query response with answer, sources, and verification info
    """
    try:
        # Handle Chat Session: User Message
        if request.session_id:
            session = crud.get_chat_session(db, request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            crud.create_chat_message(db, request.session_id, "user", request.question)

        # Get components
        embedder = get_embedder()
        vector_store = get_vector_store()
        ollama = get_ollama_client()
        faithfulness_checker = get_faithfulness_checker()
        scorer = get_scorer()
        
        # Embed query
        query_embedding = embedder.embed_text(request.question)
        
        # Retrieve chunks
        top_k = request.top_k or TOP_K
        results = vector_store.search(query_embedding, top_k=top_k * 2)  # Get more for filtering
        
        # Helper to save assistant response and return
        def save_and_return(response: schema.QueryResponse):
            if request.session_id:
                crud.create_chat_message(
                    db, 
                    request.session_id, 
                    "assistant", 
                    response.answer,
                    [s.dict() for s in response.sources],
                    {"faithfulness": response.faithfulness_score, "status": response.verification_status}
                )
            return response

        if not results:
            return save_and_return(schema.QueryResponse(
                answer="I don't have any materials to answer this question. Please upload course materials first.",
                sources=[],
                faithfulness_score=0.0,
                verification_status="no_materials",
                confidence=0.0
            ))
        
        # Apply metadata filters
        if request.filters:
            results = MetadataFilter.apply_filters_to_results(
                db, results,
                material_type=request.filters.material_type,
                lecture_number=request.filters.lecture_number,
                topic=request.filters.topic,
                material_ids=request.filters.material_ids
            )
        
        # Limit to top_k after filtering
        results = results[:top_k]
        
        if not results:
            return save_and_return(schema.QueryResponse(
                answer="No materials match your filters. Try adjusting the filters or uploading more materials.",
                sources=[],
                faithfulness_score=0.0,
                verification_status="no_matches",
                confidence=0.0
            ))
        
        # Build context with metadata
        context_chunks = []
        sources_info = []
        
        for chunk_id, score in results:
            chunk = crud.get_chunk(db, chunk_id)
            if not chunk:
                continue
            
            context_chunks.append({
                'text': chunk.text,
                'metadata': chunk.chunk_metadata
            })
            
            # Prepare source info
            sources_info.append(schema.SourceInfo(
                chunk_id=chunk.chunk_id,
                material_id=chunk.material_id,
                material_title=chunk.chunk_metadata.get('material_title', 'Unknown'),
                page=chunk.chunk_metadata.get('page'),
                section=chunk.chunk_metadata.get('section'),
                material_type=chunk.chunk_metadata.get('material_type', 'unknown'),
                similarity_score=score
            ))
        
        # Create RAG prompt
        prompt = create_rag_prompt(request.question, context_chunks)
        
        # Generate answer
        answer = ollama.generate(prompt, system_prompt=SYSTEM_PROMPT)
        
        # Check for refusal
        if extract_refusal_keywords(answer):
            # LLM refused to answer
            crud.create_query_log(
                db, request.question, answer, None, 0.0, "llm_refused",
                request.filters.dict() if request.filters else None, top_k,
                session_id=request.session_id
            )
            
            return save_and_return(schema.QueryResponse(
                answer=answer,
                sources=sources_info,
                faithfulness_score=0.0,
                verification_status="llm_refused",
                confidence=sum(s.similarity_score for s in sources_info) / len(sources_info)
            ))
        
        # Verify faithfulness
        verification_report = faithfulness_checker.verify_answer(answer, context_chunks)
        evaluation = scorer.evaluate(verification_report)
        
        # Check if we should refuse based on faithfulness
        if scorer.should_refuse(evaluation):
            refusal_message = scorer.create_refusal_message(evaluation)
            
            crud.create_query_log(
                db, request.question, refusal_message, None,
                verification_report['faithfulness_score'], "verification_failed",
                request.filters.dict() if request.filters else None, top_k,
                session_id=request.session_id
            )
            
            return save_and_return(schema.QueryResponse(
                answer=refusal_message,
                sources=sources_info,
                faithfulness_score=verification_report['faithfulness_score'],
                verification_status="failed",
                confidence=sum(s.similarity_score for s in sources_info) / len(sources_info)
            ))
        
        # Log successful query
        crud.create_query_log(
            db, request.question, answer,
            [s.dict() for s in sources_info],
            verification_report['faithfulness_score'],
            evaluation['status'],
            request.filters.dict() if request.filters else None, top_k,
            session_id=request.session_id
        )
        
        # Return successful response
        return save_and_return(schema.QueryResponse(
            answer=answer,
            sources=sources_info,
            faithfulness_score=verification_report['faithfulness_score'],
            verification_status=evaluation['status'],
            confidence=sum(s.similarity_score for s in sources_info) / len(sources_info)
        ))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")
