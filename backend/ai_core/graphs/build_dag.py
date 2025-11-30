import asyncio
from datetime import datetime
from time import sleep
from collections import defaultdict, deque
from backend.schemas.mail import EmailAnalysisSchema, EmailConnectionSchema
from backend.ai_core.llm_api.api import  async_get_response
from backend.ai_core.graphs.utils import try_parse_datetime
from backend.ai_core.llm_api.helper import get_response

def _create_connection(older_email: EmailAnalysisSchema, newer_email: EmailAnalysisSchema) -> EmailConnectionSchema | None:
    """
    Create a connection between two emails if a relationship is detected.
    """
    prompt = (
        f"Consider the following two emails.\n"
        f"\n"
        f"Older email:"
        f"Sender: {older_email.sender}\n"
        f"Recipients: {', '.join(older_email.recipients)}\n"
        f"Timestamp: {older_email.timestamp}\n"
        f"Topic: {older_email.topic}\n"
        f"Summary <AI generated, may contain mistakes>: {older_email.summary}\n"
        f"Content:\n{older_email.extra.get('data', 'No content available')}\n"
        f"\n"
        f"Newer email:"
        f"Sender: {newer_email.sender}\n"
        f"Recipients: {', '.join(newer_email.recipients)}\n"
        f"Timestamp: {newer_email.timestamp}\n"
        f"Topic: {newer_email.topic}\n"
        f"Summary <AI generated, may contain mistakes>: {newer_email.summary}\n"
        f"Content:\n{newer_email.extra.get('data', 'No content available')}\n"
        f"\n"
        f"\n"
        f"Identify if the newer email is a follow-up/response/related to the older email.\n"
        f"If yes, extract the following information:\n"
        f"> Decisions made in the newer email related to the older email (that were not yet mentioned in the older email)\n"
        f"> Inquiries raised in the newer email related to the older email (that were not mentioned in the older email)\n"
        f"> Risks mentioned in the newer email related to the older email (that were not mentioned in the older email)\n"
        f"Each of those lists should contain zero or more items.\n"
        f"\n"
        f"FORMAT:\n"
        f"Decisions:\n"
        f"> decision 1\n"
        f"> decision 2\n"
        f"...\n"
        f"Inquiries:\n"
        f"> inquiry 1\n"
        f"> inquiry 2\n"
        f"...\n"
        f"Risks:\n"
        f"> risk 1\n"
        f"> risk 2\n"
        f"...\n"
        f"\n"
        f"If there are no decisions, inquiries, or risks, just leave the section empty (no > items). NO additional text.\n"
        f"The data should be in the same language as the emails. keep the 'Decisions', 'Inquiries', 'Risks' headings in english. Keep the > signs.\n"
        f"If there is no relationship (or it's very unlikely), respond with 'No Relationship'."
    )

    response = get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")

    while not response:
        print("Retrying LLM call for email connection...")
        sleep(1)
        response = get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")

    if "No Relationship" in response:
        return None
    
    # Parse the response
    decisions, inquiries, risks = [], [], []
    current_section = None

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("Decisions:"):
            current_section = "decisions"
        elif line.startswith("Inquiries:"):
            current_section = "inquiries"
        elif line.startswith("Risks:"):
            current_section = "risks"
        elif line.startswith(">"):
            item = line[1:].strip()
            if current_section == "decisions":
                decisions.append(item)
            elif current_section == "inquiries":
                inquiries.append(item)
            elif current_section == "risks":
                risks.append(item)

    return EmailConnectionSchema(
        older_email=older_email,
        newer_email=newer_email,
        decisions=decisions,
        inquiries=inquiries,
        risks=risks
    )

async def _async_create_connection(older_email: EmailAnalysisSchema, newer_email: EmailAnalysisSchema) -> EmailConnectionSchema | None:
    """
    Create a connection between two emails if a relationship is detected.
    """
    prompt = (
        f"Consider the following two emails.\n"
        f"\n"
        f"Older email:"
        f"Sender: {older_email.sender}\n"
        f"Recipients: {', '.join(older_email.recipients)}\n"
        f"Timestamp: {older_email.timestamp}\n"
        f"Topic: {older_email.topic}\n"
        f"Summary <AI generated, may contain mistakes>: {older_email.summary}\n"
        f"Content:\n{older_email.extra.get('data', 'No content available')}\n"
        f"\n"
        f"Newer email:"
        f"Sender: {newer_email.sender}\n"
        f"Recipients: {', '.join(newer_email.recipients)}\n"
        f"Timestamp: {newer_email.timestamp}\n"
        f"Topic: {newer_email.topic}\n"
        f"Summary <AI generated, may contain mistakes>: {newer_email.summary}\n"
        f"Content:\n{newer_email.extra.get('data', 'No content available')}\n"
        f"\n"
        f"\n"
        f"Identify if the newer email is a follow-up/response/related to the older email.\n"
        f"If yes, extract the following information:\n"
        f"> Decisions made in the newer email related to the older email (that were not yet mentioned in the older email)\n"
        f"> Inquiries raised in the newer email related to the older email (that were not mentioned in the older email)\n"
        f"> Risks mentioned in the newer email related to the older email (that were not mentioned in the older email)\n"
        f"Each of those lists should contain zero or more items.\n"
        f"\n"
        f"FORMAT:\n"
        f"Decisions:\n"
        f"> decision 1\n"
        f"> decision 2\n"
        f"...\n"
        f"Inquiries:\n"
        f"> inquiry 1\n"
        f"> inquiry 2\n"
        f"...\n"
        f"Risks:\n"
        f"> risk 1\n"
        f"> risk 2\n"
        f"...\n"
        f"\n"
        f"If there are no decisions, inquiries, or risks, just leave the section empty (no > items). NO additional text.\n"
        f"The data should be in the same language as the emails. keep the 'Decisions', 'Inquiries', 'Risks' headings in english. Keep the > signs.\n"
        f"If there is no relationship (or it's very unlikely), respond with 'No Relationship'."
    )
    response = await async_get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")

    # Retry when the model fails to respond
    while not response:
        print("Retrying LLM call for email connection (async)...")
        await asyncio.sleep(1)
        response = await async_get_response(prompt, model="meta-llama/Llama-3.3-70B-Instruct")

    if "No Relationship" in response:
        return None

    # Parse the response
    decisions, inquiries, risks = [], [], []
    current_section = None

    for line in response.split("\n"):
        line = line.strip()
        if line.startswith("Decisions:"):
            current_section = "decisions"
        elif line.startswith("Inquiries:"):
            current_section = "inquiries"
        elif line.startswith("Risks:"):
            current_section = "risks"
        elif line.startswith(">"):
            item = line[1:].strip()
            if current_section == "decisions":
                decisions.append(item)
            elif current_section == "inquiries":
                inquiries.append(item)
            elif current_section == "risks":
                risks.append(item)

    return EmailConnectionSchema(
        older_email=older_email,
        newer_email=newer_email,
        decisions=decisions,
        inquiries=inquiries,
        risks=risks
    )


def _transitive_reduction(connections: list[EmailConnectionSchema]) -> list[EmailConnectionSchema]:
    """
    Filters the connections to remove redundant transitive edges.
    Example: If A->B and B->C and A->C exist, remove A->C to keep the graph sparse.
    """
    
    # 1. Build an adjacency map for easy traversal: Parent -> Set of Children
    # Using object identity or hash as key
    adj = defaultdict(set)
    for conn in connections:
        adj[conn.older_email].add(conn.newer_email)

    def has_indirect_path(start_node, target_node):
        """
        BFS to check if there is a path from start_node to target_node
        NOT using the direct edge between them.
        """
        queue = deque([child for child in adj[start_node] if child != target_node])
        visited = {start_node}

        while queue:
            current = queue.popleft()
            if current == target_node:
                return True
            
            if current not in visited:
                visited.add(current)
                # Add neighbors of current
                for neighbor in adj[current]:
                    queue.append(neighbor)
        return False

    # 2. Filter edges
    filtered_connections = []
    
    for conn in connections:
        parent = conn.older_email
        child = conn.newer_email
        
        # If we can reach Child from Parent via another node, this direct edge is redundant.
        if has_indirect_path(parent, child):
            continue # Skip this connection
        else:
            filtered_connections.append(conn)
            
    return filtered_connections


def build_dag(emails: list[EmailAnalysisSchema]) -> list[EmailConnectionSchema]:
    """
    Build a sparse DAG representing relationships between emails.
    This process involves:
    1. Sorting emails by date.
    2. Generating potential edges using LLM pairwise comparison.
    3. Performing transitive reduction to remove shortcut edges.

    Args:
        emails (list[EmailAnalysisSchema]): List of email analysis schemas.
    Returns:
        list[EmailConnectionSchema]: List of filtered email connections.
    """

    # 1. Sort Phase
    # Sort strictly by time to ensure DAG directionality (Past -> Future)
    emails = sorted(emails, key=lambda e: try_parse_datetime(e.timestamp or "12 dec 1950 00:00:00") or datetime.min)

    raw_connections = []

    # 2. Candidate Generation Phase
    # We compare every pair (O(N^2)) to find potential relationships.
    # Note: For very large bundles (>50 emails), we might want to window this search.
    for i in range(len(emails)):
        for j in range(i + 1, len(emails)):
            older_email = emails[i]
            newer_email = emails[j]

            # Optimization: If using a vector DB previously, we could check similarity threshold 
            # here again to save LLM tokens before calling _create_connection.
            
            connection = _create_connection(older_email, newer_email)
            if connection:
                raw_connections.append(connection)

    # 3. Graph Simplification Phase (Transitive Reduction)
    sparse_connections = _transitive_reduction(raw_connections)

    return sparse_connections

async def async_build_dag(emails: list[EmailAnalysisSchema]) -> list[EmailConnectionSchema]:
    """
    Build a sparse DAG representing relationships between emails.
    This process involves:
    1. Sorting emails by date.
    2. Generating potential edges using LLM pairwise comparison.
    3. Performing transitive reduction to remove shortcut edges.
    Args:
        emails (list[EmailAnalysisSchema]): List of email analysis schemas.
    Returns:
        list[EmailConnectionSchema]: List of filtered email connections.
    """
    
    # 1. Sort Phase
    # Sort strictly by time to ensure DAG directionality (Past -> Future)
    emails = sorted(emails, key=lambda e: try_parse_datetime(e.timestamp or "12 dec 1950 00:00:00") or datetime.min)

    raw_connections = []

    # 2. Candidate Generation Phase
    # We compare every pair (O(N^2)) to find potential relationships.
    # Note: For very large bundles (>50 emails), we might want to window this search.
    tasks = []
    email_pairs = []

    for i in range(len(emails)):
        for j in range(i + 1, len(emails)):
            older_email = emails[i]
            newer_email = emails[j]

            email_pairs.append((older_email, newer_email))
            tasks.append(_async_create_connection(older_email, newer_email))

    connections_results = await asyncio.gather(*tasks)

    for connection in connections_results:
        if connection:
            raw_connections.append(connection)

    # 3. Graph Simplification Phase (Transitive Reduction)
    sparse_connections = _transitive_reduction(raw_connections)
    return sparse_connections

def sync_async_build_dag(emails: list[EmailAnalysisSchema]) -> list[EmailConnectionSchema]:
    return asyncio.run(async_build_dag(emails))