import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_explainer():
    try:
        # We set a timeout/max token constraint to keep it lightweight
        return pipeline("text-generation", model="gpt2", device=-1) # -1 forces CPU mode safely
    except Exception:
        return None

def generate_ai_explanation(issue):
    # --- INSTANT LOCAL ENGINEERING GLOSSARY (Fallback Engine) ---
    glossary = {
        "SELECT *": "Retrieving all columns disables covering indexes, increases network I/O, and forces the engine to read unnecessary data blocks from disk.",
        "JOINs": "Excessive joins exponentially increase the complexity of the execution plan, forcing the query optimizer to evaluate massive permutation matrices.",
        "WHERE clause": "Filtering data after structural execution forces full table scans, processing millions of rows instead of utilizing b-tree index pointers.",
        "LIMIT or TOP": "Uncapped queries risk overwhelming web application memory layers by fetching full database segments instead of targeted pagination rows.",
        "ORDER BY without a LIMIT": "Sorting massive tables requires temporary disk space allocation (Spooling) to process merge-sort algorithms when RAM limits are exceeded.",
        "Table Scan": "A sequential scan means no appropriate index was found, forcing the storage engine to check every single row sequentially on the hard drive."
    }
    
    # 1. Quick check: Match key terms to return an instant explanation
    for key, text in glossary.items():
        if key in issue:
            return f"{text} (Served via Local Analytics Index Engine)"
            
    # 2. Try the Transformer pipeline if the glossary missed it
    try:
        generator = load_explainer()
        if generator:
            prompt = f"In SQL performance tuning, why is this an issue: '{issue}'? Reason:"
            res = generator(prompt, max_new_tokens=30, num_return_sequences=1, temperature=0.6)
            return res[0]['generated_text'].replace(prompt, "").strip()
    except Exception:
        pass
        
    return "Optimizing this query layout minimizes relational data execution risk and lowers server compute usage."