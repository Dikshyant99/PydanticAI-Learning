from pydantic_ai import ModelResponse
#usd per million tokens
PRICES={
    'claude-haiku-5-5':{
        'threshold' :100_000,#Prompt size where the price tier changes
        'short':(0.10,0.50),#input and output for the prompts <= threshold
        'long':(0.50,2.50,)#input and output for the prompts > threshold
            
        
    },
}
def request_cost(input_tokens:int,output_tokens:int,model:str='claude-haiku-5-5')->float:
    p=PRICES[model]
    in_price, out_price = p['long'] if input_tokens > p['threshold'] else p['short']
    return input_tokens / 1_000_000 * in_price + output_tokens / 1_000_000 * out_price


def print_usage_report(result, model: str = 'claude-haiku-5-5') -> float:
    """Print tokens and cost for every model request in a run, plus the total."""
    print('\n=== Usage & cost ===')
    total_cost = 0.0
    n = 0
    for message in result.all_messages():
        if isinstance(message, ModelResponse):   # one per round trip to the model
            n += 1
            u = message.usage
            cost = request_cost(u.input_tokens, u.output_tokens, model)
            total_cost += cost
            print(f'Request {n}: {u.input_tokens:>6} in  {u.output_tokens:>5} out   ${cost:.6f}')
    usage= result.usage()
    print('_'*48)
    print(f'Total: {usage.input_tokens} in, {usage.output_tokens} out, '
          f'{usage.requests} requests, {usage.tool_calls} tool calls')
    print(f'Cost:  ${total_cost:.6f}  (≈ ${total_cost * 1000:.4f} per 1,000 runs)')
    
    return total_cost

