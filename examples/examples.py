"""
Orangic Python SDK - Usage Examples
"""

import orangic
import os


def basic_completion():
    """Basic chat completion example"""
    print("=== Basic Completion ===\n")
    
    client = orangic.Orangic(api_key=os.getenv("ORANGIC_API_KEY"))
    
    response = client.chat.completions.create(
        model="org-1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    
    print(f"Response: {response.choices[0].message['content']}")
    print(f"Tokens used: {response.usage}")
    print()


def streaming_completion():
    """Streaming chat completion example"""
    print("=== Streaming Completion ===\n")
    
    client = orangic.Orangic()
    
    stream = client.chat.completions.create(
        model="org-1",
        messages=[
            {"role": "user", "content": "Write a short poem about coding"}
        ],
        stream=True
    )
    
    print("Streaming response: ", end="")
    for chunk in stream:
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].get("delta", {})
            if "content" in delta:
                print(delta["content"], end="", flush=True)
    
    print("\n")


def conversation_example():
    """Multi-turn conversation example"""
    print("=== Multi-turn Conversation ===\n")
    
    client = orangic.Orangic()
    
    messages = [
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "What is 15 * 24?"},
    ]
    
    # First response
    response = client.chat.completions.create(
        model="org-1",
        messages=messages
    )
    
    assistant_message = response.choices[0].message
    print(f"Assistant: {assistant_message['content']}\n")
    
    # Add to conversation history
    messages.append(assistant_message)
    messages.append({"role": "user", "content": "Can you show me how to solve it step by step?"})
    
    # Second response
    response = client.chat.completions.create(
        model="org-1",
        messages=messages
    )
    
    print(f"Assistant: {response.choices[0].message['content']}\n")


def with_parameters():
    """Example with advanced parameters"""
    print("=== Advanced Parameters ===\n")
    
    client = orangic.Orangic()
    
    response = client.chat.completions.create(
        model="org-1",
        messages=[
            {"role": "user", "content": "Write three creative company names for a coffee shop"}
        ],
        temperature=0.9,  # Higher creativity
        max_tokens=100,
        top_p=0.95,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    
    print(f"Response: {response.choices[0].message['content']}\n")


def error_handling():
    """Example with error handling"""
    print("=== Error Handling ===\n")
    
    try:
        # This will fail with invalid API key
        client = orangic.Orangic(api_key="invalid-key")
        response = client.chat.completions.create(
            model="org-1",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except orangic.AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except orangic.RateLimitError as e:
        print(f"Rate Limit Error: {e}")
    except orangic.APIError as e:
        print(f"API Error: {e}")
    
    print()



def quick_completion():
    """Quick completion without client instance"""
    print("=== Quick Completion ===\n")
    
    response = orangic.completion(
        model="org-1",
        messages=[{"role": "user", "content": "Say hello!"}]
    )
    
    print(f"Response: {response.choices[0].message['content']}\n")


def using_message_objects():
    """Example using Message objects"""
    print("=== Using Message Objects ===\n")
    
    client = orangic.Orangic()
    
    messages = [
        orangic.Message(role="system", content="You are a helpful assistant"),
        orangic.Message(role="user", content="Explain recursion in simple terms")
    ]
    
    response = client.chat.completions.create(
        model="org-1",
        messages=messages
    )
    
    print(f"Response: {response.choices[0].message['content']}\n")


if __name__ == "__main__":
    # Make sure to set ORANGIC_API_KEY environment variable before running
    
    if not os.getenv("ORANGIC_API_KEY"):
        print("Please set ORANGIC_API_KEY environment variable")
        print("Example: export ORANGIC_API_KEY='your-api-key'")
        exit(1)
    
    print("Orangic Python SDK Examples")
    print("=" * 50)
    print()
    
    # Run examples (comment out the ones that require valid API)
    # basic_completion()
    # streaming_completion()
    # conversation_example()
    # with_parameters()
    # error_handling()
    # quick_completion()
    # using_message_objects()
    
    print("Examples completed!")