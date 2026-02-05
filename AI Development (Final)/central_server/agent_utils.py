import logging

def format_agent_response(text, handoff=False, escalated=False):
    """
    Return a standardized response JSON for frontend.
    """
    return {
        "response": text,
        "handoff": handoff,
        "escalated": escalated
    }

def safe_llm_call(llm_function, *args, **kwargs):
    """
    Call an LLM function safely; fallback if it fails.
    """
    try:
        return llm_function(*args, **kwargs)
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return "Sorry, I couldn't process that request."
