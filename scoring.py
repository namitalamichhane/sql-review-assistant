def calculate_score(issues):
    score = 100
    
    for issue in issues:
        # Match the exact prefix text from your updated analyzer
        if "Critical Hazard" in issue or "Security Vulnerability" in issue:
            score -= 30  
        elif "Performance Risk" in issue or "Architectural Issue" in issue or "Complexity Risk" in issue:
            score -= 15  
        else:
            score -= 10  # Standard tip or logical warning penalty
            
    return max(score, 0)