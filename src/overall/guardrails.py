

def end_guardrails(tool_calls, iterations, max_iterations) -> bool:
    if (iterations >= max_iterations):
        return True
    
    if (len(tool_calls) == 0):
        return True

    # if ():
    #     return True

    return False

    