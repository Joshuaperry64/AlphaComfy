# Plan: AlphaComfy Bridge Integration

This plan outlines the creation of a Python-based bridge that uses LM Studio as a "Prompt Engineer" and ComfyUI as the "Image Engine".

## Objective
Enable a workflow where a user provides a simple idea, a local LLM (via LM Studio) expands it into a high-quality Stable Diffusion prompt, and ComfyUI generates the image automatically.

## Key Files & Context
- `bridge.py`: Main execution script.
- `workflow_api.json`: ComfyUI workflow in API format.
- `requirements.txt`: Python dependencies (`openai`, `websocket-client`, `requests`).

## Implementation Steps

### 1. Project Initialization
- Create `requirements.txt` with necessary libraries.
- Create a basic `README.md` for user guidance.

### 2. ComfyUI Workflow Template
- Create `workflow_api.json`. This will be a standard Text-to-Image workflow compatible with Stable Diffusion 1.5 or SDXL. It will include:
    - Load Checkpoint
    - CLIP Text Encode (Positive & Negative)
    - Empty Latent Image
    - KSampler
    - VAE Decode
    - Save Image

### 3. Bridge Script Development
- **LM Studio Client:** Setup a client to talk to `http://localhost:1234/v1`.
- **ComfyUI Client:** Implement functions to:
    - Connect via WebSocket (to monitor progress).
    - Queue the prompt JSON.
    - Retrieve the generated image filename.
- **Integration Logic:**
    1. Receive user input.
    2. Send to LM Studio for prompt expansion.
    3. Inject expanded prompt into `workflow_api.json`.
    4. Send modified JSON to ComfyUI.
    5. Wait for generation and report success.

## Verification & Testing
- Instructions for the user to start LM Studio and ComfyUI.
- Running `python bridge.py "a majestic dragon in a library"`.
- Checking the `output` folder of ComfyUI for the result.

## Future Enhancements
- Support for multiple workflows.
- Vision-based feedback loops (AI critiquing the image).
- GUI for the bridge itself.
