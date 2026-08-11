import json
import urllib.request
import urllib.parse
import uuid
import websocket
import argparse
import sys
from openai import OpenAI

# --- Configuration ---
LM_STUDIO_URL = "http://localhost:1234/v1"
COMFYUI_URL = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

# --- LM Studio Integration ---
def get_expanded_prompt(user_input):
    print(f"[*] Consulting LM Studio Brain for: '{user_input}'...")
    try:
        client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")
        response = client.chat.completions.create(
            model="local-model",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Stable Diffusion prompt engineer. Your task is to take a simple user idea and expand it into a detailed, descriptive prompt that includes artistic style, lighting, composition, and high-quality keywords. Output ONLY the refined prompt. No conversation, no 'Here is your prompt', just the text."
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        expanded = response.choices[0].message.content.strip()
        print(f"[+] Expanded Prompt: {expanded}")
        return expanded
    except Exception as e:
        print(f"[!] Error connecting to LM Studio: {e}")
        print("[!] Falling back to original prompt.")
        return user_input

# --- ComfyUI Integration ---
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": CLIENT_ID}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{COMFYUI_URL}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{COMFYUI_URL}/history/{prompt_id}") as response:
        return json.loads(response.read())

def track_progress(prompt_id):
    ws = websocket.WebSocket()
    ws.connect(f"ws://{COMFYUI_URL}/ws?clientId={CLIENT_ID}")
    
    print("[*] Generation in progress...")
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break # Execution is done
            elif message['type'] == 'progress':
                data = message['data']
                print(f"    Progress: {data['value']}/{data['max']}", end='\r')
        else:
            continue
    ws.close()
    print("\n[+] Generation complete!")

def run_workflow(positive_prompt):
    # Load workflow from file
    try:
        with open("workflow_api.json", "r") as f:
            workflow = json.load(f)
    except FileNotFoundError:
        print("[!] Error: workflow_api.json not found.")
        return

    # Inject the prompt (Node 6 is our positive prompt node)
    workflow["6"]["inputs"]["text"] = positive_prompt
    
    # Randomize seed for KSampler (Node 3)
    import random
    workflow["3"]["inputs"]["seed"] = random.randint(0, 1125899906842624)

    # Queue the task
    print("[*] Queuing task in ComfyUI...")
    prompt_response = queue_prompt(workflow)
    prompt_id = prompt_response['prompt_id']

    # Track progress via WebSocket
    track_progress(prompt_id)

    # Get final image info
    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            for image in node_output['images']:
                print(f"[+] Image saved as: {image['filename']}")

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AlphaComfy Bridge")
    parser.add_argument("prompt", type=str, help="The simple idea for the image")
    args = parser.parse_args()

    # 1. Expand prompt using LM Studio
    refined = get_expanded_prompt(args.prompt)

    # 2. Run ComfyUI workflow
    run_workflow(refined)
