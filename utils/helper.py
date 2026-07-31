def calculate_estimated_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float = 0.10,
    output_price_per_million: float = 0.40,
) -> float:
    """
    Calculate the estimated API cost in USD.

    Args:
        input_tokens: Number of input (prompt) tokens.
        output_tokens: Number of output (completion) tokens.
        input_price_per_million: USD cost per 1M input tokens.
        output_price_per_million: USD cost per 1M output tokens.

    Returns:
        Estimated cost in USD.
    """
    input_cost = (input_tokens / 1_000_000) * input_price_per_million
    output_cost = (output_tokens / 1_000_000) * output_price_per_million

    return round(input_cost + output_cost, 8)