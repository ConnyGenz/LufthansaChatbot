import asyncio

# Define a decorator that retries asynchronous functions
# With synchronous programming, the agent will process one request after the next
# With asynchronous programming, the agent can process several requests at once and
# wait for the answers as they arrive.
# If there are connection errors, e.g. with the neo4j database, the program should not
# produce an error message, but try again.
# In synchronous programming, we have the @retry decorator for that. In asynchronous
# programming, we need an asynchronous equivalent.

def async_retry(max_retries: int=3, delay: int=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    await asyncio.sleep(delay)

            raise ValueError(f"Failed after {max_retries} attempts")

        return wrapper

    return decorator