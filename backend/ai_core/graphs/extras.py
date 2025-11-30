from collections import defaultdict
from typing import Dict, List, Set
import json
import re

from .utils import try_parse_datetime
from datetime import datetime

from ...schemas.mail import EmailAnalysisSchema, EmailConnectionSchema
from backend.ai_core.llm_api.helper import get_response

def _build_parent_map(connections: list[EmailConnectionSchema]) -> Dict[EmailAnalysisSchema, List[EmailAnalysisSchema]]:
    """
    Helper to create an adjacency list (Child -> [Parents]) for efficient traversal.
    """
    parent_map = defaultdict(list)
    for conn in connections:
        # conn.older_email is the parent, conn.newer_email is the child
        parent_map[conn.newer_email].append(conn.older_email)
    return parent_map

def calculate_rolling_states(
    emails: list[EmailAnalysisSchema], 
    connections: list[EmailConnectionSchema]
) -> Dict[EmailAnalysisSchema, str]:
    """
    Traverses the DAG to generate a 'State Snapshot' for each email.
    It takes the state of the parent(s) and applies the 'diff' of the current email.
    """
    
    # 1. Sort by date to ensure we process parents before children
    # (Assuming your sorting logic from build_dag is accessible, repeating it here for safety)
    sorted_emails = sorted(
        emails, 
        key=lambda e: try_parse_datetime(e.timestamp or "12 dec 1950 00:00:00") or datetime.min
    )
    
    parent_map = _build_parent_map(connections)
    states: Dict[EmailAnalysisSchema, str] = {}

    print("Calculating rolling states...")

    for email in sorted_emails:
        parents = parent_map.get(email, [])
        
        # 1. Aggregate Parent States
        if not parents:
            previous_context = "Project Start / No previous context."
        else:
            # If multiple parents (branch merge), we concatenate their states
            # In a production app, you might want an LLM to 'merge' these states first if they conflict
            parent_states_text = "\n---\n".join(
                [f"Parent Source ({p.sender}): {states.get(p, 'Unknown State')}" for p in parents]
            )
            previous_context = f"Previous States:\n{parent_states_text}"

        # 2. The Prompt
        prompt = (
            f"You are maintaining the 'Rolling State' of a project based on an email thread.\n"
            f"Input:\n"
            f"1. PREVIOUS STATE (where the project was before this email):\n{previous_context}\n\n"
            f"2. NEW EMAIL (the update):\n"
            f"From: {email.sender}\n"
            f"Subject/Topic: {email.topic}\n"
            f"Content Summary: {email.summary}\n"
            f"Content: {email.extra.get('data', 'See summary')}\n\n"
            f"TASK:\n"
            f"Update the state. The state should be a concise snapshot of:\n"
            f"- Current status (e.g., Planning, Blocked, Deployed)\n"
            f"- Active Action Items (Who is doing what)\n"
            f"- Key Decisions currently in effect\n"
            f"RULES:\n"
            f"- The rolling state should be in the same language as the email.\n"
            f"- OVERWRITE obsolete info (e.g. if Previous says 'Meeting Tue', and New says 'Meeting moved to Wed', only keep 'Meeting Wed').\n"
            f"- Keep it under 100 words.\n"
            f"- Output raw text only, no markdown formatting."
        )

        # 3. Call LLM
        new_state = get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")
        
        # Retry logic could go here
        if not new_state: 
            new_state = "State generation failed."
            
        states[email] = new_state.strip()
        # Sleep slightly to avoid rate limits if necessary
        # sleep(0.2) 

    return states


def assign_topic_tags(
    emails: list[EmailAnalysisSchema], 
    connections: list[EmailConnectionSchema]
) -> Dict[EmailAnalysisSchema, List[str]]:
    """
    Traverses the DAG to flow tags from parents to children.
    Allows new tags to be added if the topic diverges.
    """
    
    sorted_emails = sorted(
        emails, 
        key=lambda e: try_parse_datetime(e.timestamp or "12 dec 1950 00:00:00") or datetime.min
    )
    
    parent_map = _build_parent_map(connections)
    tags_map: Dict[EmailAnalysisSchema, List[str]] = {}

    print("Assigning topic tags...")

    for email in sorted_emails:
        parents = parent_map.get(email, [])
        
        # 1. Inherit Tags
        inherited_tags = set()
        for p in parents:
            if p in tags_map:
                inherited_tags.update(tags_map[p])
        
        inherited_list = list(sorted(inherited_tags))
        
        # 2. The Prompt
        # We handle the "Root Node" case inside the prompt logic by passing empty inherited tags
        prompt = (
            f"Analyze the following email to assign Project/Topic tags.\n"
            f"Context:\n"
            f"- Incoming/Inherited Tags from thread: {inherited_list if inherited_list else 'None (New Thread)'}\n"
            f"- Email Sender: {email.sender}\n"
            f"- Email Topic/Subject: {email.topic}\n"
            f"- Content: {email.summary}\n\n"
            f"TASK:\n"
            f"Return a JSON list of strings representing the tags for this specific email.\n"
            f"Logic:\n"
            f"1. KEEP valid inherited tags (e.g., if it's still about 'Project A', keep 'Project A').\n"
            f"2. DROP tags if the conversation explicitly ends that topic.\n"
            f"3. ADD new tags if a new project or distinct sub-module is introduced.\n"
            f"4. Tags should be high-level (e.g., 'Project Alpha', 'Budget Q3', 'Server Migration').\n\n"
            f"Example Output format: [\"Project Alpha\", \"Budget Q3\"]\n"
            f"Respond ONLY with the JSON list."
        )

        response = get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")
        
        # 3. Parse JSON Response
        # If the LLM returns None or an empty string, fall back to inherited tags
        if not response:
            tags_map[email] = inherited_list
            continue

        try:
            # Basic cleanup if LLM is chatty
            response_text = response.strip()
            
            # Find the JSON bracket part
            match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if match:
                current_tags = json.loads(match.group())
            else:
                # Fallback if regex fails but response is simple
                current_tags = json.loads(response_text)
                
            # Sanity check: ensure it's a list of strings
            if isinstance(current_tags, list):
                tags_map[email] = sorted([str(t) for t in current_tags])
            else:
                tags_map[email] = sorted(inherited_list) # Fallback
                
        except Exception as e:
            print(f"Tag parsing failed for email {email.timestamp}: {e}")
            tags_map[email] = sorted(inherited_list)

    return tags_map