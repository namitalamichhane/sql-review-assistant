import sqlparse

def analyze_query(query):
    issues = []
    query_upper = query.upper().strip()
    
    # 1. Basic Validation
    if not query_upper:
        return ["Input is empty. Please enter a SQL query."]
        
    parsed = sqlparse.parse(query)
    if not parsed or len(parsed) == 0:
        issues.append("Syntax Error: The input could not be parsed as valid SQL.")
        return issues

    valid_starts = ("SELECT", "WITH", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")
    if not query_upper.startswith(valid_starts):
        issues.append("Structural Error: Query does not begin with a valid SQL keyword like SELECT or WITH.")
        return issues

    # 2. Performance and Optimization Rules
    if "SELECT *" in query_upper:
        issues.append("Performance Risk: Avoid SELECT *. Explicitly name your columns to optimize network traffic and disk memory.")
        
    if "LIKE '%" in query_upper or "LIKE  '%" in query_upper:
        issues.append("Performance Risk: Using a leading wildcard like '%text' prevents the database from using indexes and forces a full table scan.")

    if "UNION" in query_upper and "UNION ALL" not in query_upper:
        issues.append("Optimization Tip: UNION forces a slow sorting operation to remove duplicates. Use UNION ALL if duplicates are not an issue.")

    # 3. Architecture and Complexity Rules
    join_count = query_upper.count("JOIN")
    if join_count > 4:
        issues.append(f"Architectural Issue: High complexity detected with {join_count} JOINs. Consider breaking this query down using Common Table Expressions (CTEs).")

    if "ORDER BY" in query_upper and "LIMIT" not in query_upper and "TOP" not in query_upper:
        issues.append("Resource Risk: Found ORDER BY without a LIMIT clause. Sorting large datasets without a limit uses heavy server memory.")

    if query_upper.count("SELECT") > 3 and "WITH" not in query_upper:
        issues.append("Complexity Risk: Deeply nested subqueries detected. Consider rewriting them into clean Common Table Expressions (CTEs) for readability.")

    # 4. Logic and Data Filtering Rules
    if "FROM" in query_upper and "WHERE" not in query_upper:
        if "INFORMATION_SCHEMA" not in query_upper and "LIMIT" not in query_upper and "TOP" not in query_upper:
            issues.append("Logical Warning: Missing a WHERE clause filter. This query will pull the entire table dataset.")

    if "= NULL" in query_upper or "!= NULL" in query_upper:
        issues.append("Logic Warning: Evaluating NULL with '=' or '!=' does not work correctly. Use 'IS NULL' or 'IS NOT NULL' instead.")

    # 5. Security and Destructive Action Rules
    if "='" in query_upper or "= '" in query_upper:
        if "+" in query_upper or "{" in query_upper or "%S" in query_upper:
            issues.append("Security Vulnerability: Potential SQL Injection risk. Detected dynamic text concatenation. Use parameterized variables instead.")

    if ("DELETE FROM" in query_upper or "UPDATE " in query_upper) and "WHERE" not in query_upper:
        issues.append("Critical Hazard: Running a DELETE or UPDATE command without a WHERE filter will modify or delete all rows in the table.")

    if "DROP TABLE" in query_upper or "DROP DATABASE" in query_upper:
        issues.append("Critical Hazard: Direct DROP command executed. Ensure this action is restricted to migration scripts.")

    return issues