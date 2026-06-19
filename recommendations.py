def get_recommendations(issues):
    recommendations = []
    
    for issue in issues:
        if "Performance Risk: Avoid SELECT *" in issue:
            recommendations.append("Rewrite your SELECT clause to explicitly list out only the exact columns your application needs.")
        elif "Performance Risk: Using a leading wildcard" in issue:
            recommendations.append("Remove the leading wildcard if possible, or use a full-text search index if you are querying massive text fields.")
        elif "Optimization Tip: UNION" in issue:
            recommendations.append("Change 'UNION' to 'UNION ALL' to bypass the expensive background duplicate sorting process.")
        elif "Architectural Issue: High complexity" in issue:
            recommendations.append("Break down this large query by pulling distinct segments into Common Table Expressions (WITH statements).")
        elif "Resource Risk: Found ORDER BY" in issue:
            recommendations.append("Append a LIMIT or TOP clause to restrict the maximum number of rows sorted in memory.")
        elif "Complexity Risk: Deeply nested subqueries" in issue:
            recommendations.append("Refactor the nested subqueries into sequential Common Table Expressions (CTEs) to make the code maintainable.")
        elif "Logical Warning: Missing a WHERE clause" in issue:
            recommendations.append("Add a targeted WHERE clause filter to restrict the data volume before running this query on a production table.")
        elif "Logic Warning: Evaluating NULL" in issue:
            recommendations.append("Modify the syntax from '= NULL' or '!= NULL' to the standard 'IS NULL' or 'IS NOT NULL'.")
        elif "Security Vulnerability" in issue:
            recommendations.append("Stop using inline string concatenation. Bind user inputs using parameterized query variables.")
        elif "Critical Hazard: Running a DELETE or UPDATE" in issue:
            recommendations.append("Immediately append a specific WHERE clause to restrict which exact rows are being altered.")
        elif "Critical Hazard: Direct DROP" in issue:
            recommendations.append("Ensure this destructive command is wrapped inside formal database migration scripts with explicit rollback paths.")
            
    return recommendations