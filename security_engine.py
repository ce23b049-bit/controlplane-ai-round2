import re

# Configurable policy layer to handle different use-case risk appetites
POLICIES = {
    "customer_support": {"block_threshold": 0.75, "flag_threshold": 0.50, "allow_edit": True},
    "internal_copilot": {"block_threshold": 0.90, "flag_threshold": 0.65, "allow_edit": True}
}

INJECTION_KEYWORDS = ["ignore previous", "override", "jailbreak", "system prompt"]
PII_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

def analyze_risk(prompt: str, use_case: str) -> dict:
    """Evaluates risk and determines tiered action: Block, Flag, Edit, or Allow."""
    prompt_lower = prompt.lower()
    policy = POLICIES.get(use_case, POLICIES["internal_copilot"])
    
    injection_score = 0.95 if any(kw in prompt_lower for kw in INJECTION_KEYWORDS) else 0.0
    pii_matches = PII_REGEX.findall(prompt)
    pii_score = 0.85 if pii_matches else 0.0
    
    max_risk = max(injection_score, pii_score)
    
    if max_risk >= policy["block_threshold"]:
        return {"action": "BLOCK", "confidence": max_risk, "reason": "High-confidence policy violation"}
    elif pii_matches and policy["allow_edit"]:
        return {"action": "EDIT", "confidence": pii_score, "reason": "PII detected, applying inline mask"}
    elif max_risk >= policy["flag_threshold"]:
        return {"action": "FLAG", "confidence": max_risk, "reason": "Ambiguous risk, escalating to human review"}
    else:
        return {"action": "ALLOW", "confidence": max_risk, "reason": "Clear"}

def mask_pii(text: str) -> str:
    return PII_REGEX.sub("[REDACTED_SSN]", text)