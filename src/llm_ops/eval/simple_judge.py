from llm_ops.eval.schemas import EvalSample, EvalResult

class SimpleJudge:
    def __init__(self):
        pass

    def evaluate(self, sample: EvalSample, response: str) -> EvalResult:
        response_lower = response.lower()
        
        missing_includes = []
        for word in sample.must_include:
            if word.lower() not in response_lower:
                missing_includes.append(word)
                
        present_excludes = []
        for word in sample.must_not_include:
            if word.lower() in response_lower:
                present_excludes.append(word)
                
        reasoning_parts = []
        passed = True
        score = sample.max_score
        
        if missing_includes:
            passed = False
            reasoning_parts.append(f"Missing required terms: {', '.join(missing_includes)}")
            score -= len(missing_includes)
            
        if present_excludes:
            passed = False
            reasoning_parts.append(f"Contains forbidden terms: {', '.join(present_excludes)}")
            # Forbid words is a big penalty
            score = 0
            
        if passed:
            reasoning_parts.append("Passed all criteria.")
            
        # Ensure score isn't negative
        score = max(0, score)
        
        return EvalResult(
            sample_id=sample.id,
            domain=sample.domain,
            prompt=sample.prompt,
            response=response,
            score=float(score),
            passed=passed,
            reasoning="; ".join(reasoning_parts)
        )
