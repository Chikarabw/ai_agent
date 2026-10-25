import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("No key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="user_answer")
parser.add_argument("user_prompt", type=str, help="Add your content")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for i in range (20):
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        messages=messages,
        tools=available_functions
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    if not response.usage:
        raise RuntimeError("response is empty")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)

            if not result_message["content"]:
                raise Exception("Content is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(response_message.content)
        break
else:
    print("The call limit has been reached")
