import os
import json
from mistralai.client import Mistral

from tools.tool_registry import tools
from tools.calendar_tool import create_calendar_event
from tools.task_tool import create_task
from overall.guardrails import end_guardrails


# Initialize the client and model
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

names_to_functions = {
    'create_calendar_event': create_calendar_event,
    'create_task': create_task,
}

iterations = 0
messages = []

def loop_function(max_iterations=6):
    # Chat loop
    while True:
    iterations += 1

    # The user query, example: "What's the status of my transaction T1001? After receiving the answer, provide the current status of T1001. Afte that, look for the next one between T1002 if previous status was 'Paid' and T1003 if previous status was 'Unpaid'."
    user_query = input("User: ")
    if not user_query:
        break
    messages.append({"role": "user", "content": user_query})

    # Call the model
    response = client.chat.complete(
        model = model,
        messages = messages,
        tools = tools
    )

    # Add the response message to the messages list
    messages.append(response.choices[0].message)

    # Retrieve the function name and arguments if any, interactively until the model returns a final answer
    while response.choices[0].message.tool_calls:

        if end_guardrails(response.choices[0].message.tool_calls, iterations, max_iterations=6):
            break

        # Print content in case we have interleaved tool calls and text content
        if response.choices[0].message.content:
            print("Assistant:", response.choices[0].message.content)

        # Handle each tool call
        for tool_call in response.choices[0].message.tool_calls:

            function_name = tool_call.function.name # The function name to call
            function_params = json.loads(tool_call.function.arguments) # The function arguments
            function_result = names_to_functions[function_name](**function_params) # The function result

            # Print the function call
            print(f"Tool {tool_call.id}:", f"{function_name}({function_params}) -> {function_result}")

            # Add the function result to the messages list and call model
            messages.append({
                "role":"tool",
                "name":function_name,
                "content":json.dumps(function_result),
                "tool_call_id":tool_call.id
            })

        response = client.chat.complete(
            model = model,
            messages = messages,
            tools = tools
        )

        # Add the new response message to the messages list
        messages.append(response.choices[0].message)

        iterations += 1

    # Print the final answer
    return messages

if __name__ == "__main__":
    loop_function()