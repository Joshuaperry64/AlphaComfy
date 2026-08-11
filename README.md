# AlphaComfy Bridge

A bridge between **LM Studio** (Local LLM) and **ComfyUI** (Image Generation).

## Prerequisites
1. **LM Studio** running with a local server at `http://localhost:1234`.
2. **ComfyUI** running at `http://localhost:8188`.
3. Python 3.10+ installed.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the bridge script with a simple prompt:
```bash
python bridge.py "a futuristic city with neon lights"
```

The script will:
1. Ask the local LLM to expand your prompt into a high-quality SD prompt.
2. Send the expanded prompt to ComfyUI.
3. Save the resulting image information.
