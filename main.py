import os
import subprocess
import modal

# --- Modal Configuration ---
APP_NAME = "alphacomfy-modal"
VOLUME_NAME = "vo-jIx4luG87E8uTijb2Ut8Lu"
MODELS_VOLUME_PATH = "/vol/models"
CUSTOM_NODES_VOLUME_PATH = "/vol/custom_nodes"

app = modal.App(APP_NAME)

models_volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)

# Container image: PyTorch CUDA + ComfyUI + All Node Dependencies Baked In
comfy_image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "git",
        "ffmpeg",
        "libgl1-mesa-glx",
        "libglib2.0-0",
        "ca-certificates",
        "libsm6",
        "libxext6",
        "libxrender-dev",
        "cmake",
        "build-essential",
    )
    .uv_pip_install(
        "torch",
        "torchvision",
        "torchaudio",
        extra_index_url="https://download.pytorch.org/whl/cu121",
    )
    .uv_pip_install(
        # Web & Core Frameworks
        "websocket-client",
        "requests",
        "pillow",
        "pyyaml",
        "aiohttp",
        "aiosignal",
        "aiohappyeyeballs",
        "anyio",
        "async-timeout",
        "attrs",
        "annotated-types",
        "annotated-doc",
        "fastapi",
        "uvicorn",
        "starlette",
        "httpx",
        "httpcore",
        "httplib2",
        "urllib3",
        "chardet",
        "certifi",
        "charset-normalizer",
        "idna",
        "yarl",
        "multidict",
        "frozenlist",
        "propcache",
        "exceptiongroup",
        "click",
        "typer",
        "rich",
        "typing-extensions",
        "typing-inspection",
        "typeguard",
        "toml",
        "tomli",
        "tomlkit",
        "uv",
        "psutil",
        "packaging",
        "platformdirs",
        "filelock",
        "fsspec",
        "jinja2",
        "markupsafe",
        "tqdm",
        "more-itertools",
        "diskcache",
        "cachetools",
        # Git & GitHub
        "gitpython",
        "gitdb",
        "smmap",
        "PyGithub",
        "matrix-nio",
        # Cloud & APIs
        "boto3",
        "botocore",
        "s3transfer",
        "jmespath",
        "huggingface_hub",
        "hf-xet",
        "hf-gradio",
        "openai",
        "openai-whisper",
        "fal-client",
        "runwayml",
        "ollama",
        "google-genai",
        "google-generativeai",
        "google-ai-generativelanguage",
        "google-api-core",
        "google-api-python-client",
        "google-auth",
        "google-auth-httplib2",
        "googleapis-common-protos",
        "google-cloud-storage",
        "gdown",
        "gradio",
        "gradio-client",
        "spaces",
        "modelscope",
        "modelscope-hub",
        "aliyun-python-sdk-core",
        "aliyun-python-sdk-kms",
        "oss2",
        "grpcio",
        "grpcio-status",
        "proto-plus",
        "protobuf",
        # Computer Vision & Deep Learning
        "diffusers>=0.33.0",
        "accelerate>=1.2.1",
        "transformers>=4.46.2",
        "tokenizers",
        "datasets",
        "einops>=0.7.0",
        "safetensors",
        "peft>=0.17.0",
        "timm>=1.0.8",
        "kornia>=0.8.2",
        "kornia_rs",
        "open_clip_torch>=2.29.0",
        "sentencepiece>=0.2.0",
        "spandrel",
        "clip_interrogator",
        "segment_anything",
        "scikit-image",
        "scikit-learn",
        "scipy",
        "numba",
        "llvmlite",
        "dill",
        "multiprocess",
        "rotary_embedding_torch",
        "torchdiffeq>=0.2.3",
        "torchmetrics",
        "torch_complex",
        "torchcodec",
        "tensorboardX",
        "pytorch_lightning",
        "lightning-utilities",
        "fairscale",
        "gguf>=0.17.1",
        "llama-cpp-python",
        "opencv-python-headless",
        "albumentations",
        "albucore",
        "simsimd",
        "stringzilla",
        "pydantic",
        "pydantic-core",
        "piexif",
        "webcolors",
        "color-matcher",
        "mss",
        "pilgram",
        "easydict",
        "pywavelets",
        "pycocotools",
        "pycocoevalcap",
        "contourpy",
        "matplotlib",
        "kiwisolver",
        "cycler",
        "fonttools",
        "pyparsing",
        "python-dateutil",
        "pytz",
        "tzdata",
        "pandas",
        "pyarrow",
        "numpy",
        "sympy",
        "mpmath",
        "tifffile",
        "lazy_loader",
        "pooch",
        "rembg",
        "pymatting",
        "colour-science",
        "transparent-background",
        "pixeloe",
        "jsonschema",
        "jsonschema-specifications",
        "referencing",
        "rpds-py",
        "qrcode[pil]",
        "omegaconf>=2.3.0",
        "hydra-core",
        "antlr4-python3-runtime",
        # Audio, Speech & Video
        "librosa>=0.10.1",
        "soundfile",
        "sounddevice",
        "audioread",
        "soxr",
        "pydub",
        "pyloudnorm",
        "demucs",
        "stable-ts",
        "funasr",
        "voxcpm",
        "sphn",
        "julius",
        "lameenc",
        "imageio",
        "imageio-ffmpeg",
        "av",
        "moviepy==1.0.3",
        "decorator<5.0,>=4.0.2",
        # Language, Text & Cryptography
        "cryptography",
        "pycryptodome",
        "pyasn1",
        "pyasn1-modules",
        "rsa",
        "ftfy>=6.1.1",
        "tiktoken",
        "regex",
        "rapidfuzz",
        "inflect",
        "contractions",
        "anyascii",
        "textsearch",
        "pyahocorasick",
        "jieba",
        "jamo",
        "jaconv",
        "wetext",
        "sortedcontainers",
        "docstring-parser",
        "argbind",
        "python-dotenv",
        "python-multipart",
        "safehttpx",
        "msgpack",
        "orjson",
        "xxhash",
        "crcmod",
        "brotli",
        "websockets",
        "wget",
        "addict",
        "pathspec",
        "markdown-it-py",
        "mdurl",
        "pygments",
        "shellingham",
        "simplejson",
        "six",
        "cffi",
        "pycparser",
        "beautifulsoup4",
        "soupsieve",
        "PySocks",
        "uritemplate",
        # PDF & Documents
        "reportlab",
        "PyPDF2",
        "pdf2image",
        "PyMuPDF",
        # 3D / OpenGL / UI Rendering
        "PyOpenGL",
        "PyOpenGL-accelerate",
        "glfw",
        # Build Tools & Extra Libs
        "Cython",
        "scikit-build-core",
        "semantic-version",
        "umap-learn",
        "pynndescent",
        # WAS Node Suite Special Git Packages
        "git+https://github.com/WASasquatch/cstr.git",
        "git+https://github.com/WASasquatch/ffmpy.git",
        "git+https://github.com/WASasquatch/img2texture.git",
    )
    .run_commands(
        "git clone https://github.com/comfyanonymous/ComfyUI.git /root/ComfyUI",
        "cd /root/ComfyUI && pip install -r requirements.txt",
    )
)


def _setup_model_symlink():
    """
    Fast container setup:
    - Symlinks ComfyUI models directory to the persistent Modal volume.
    - Symlinks ComfyUI custom_nodes directory to the persistent Modal volume.
    """
    import shutil
    import os

    # --- Models Symlink ---
    comfy_models = "/root/ComfyUI/models"
    if os.path.isdir(comfy_models) and not os.path.islink(comfy_models):
        shutil.rmtree(comfy_models)
    if not os.path.islink(comfy_models):
        os.symlink(MODELS_VOLUME_PATH, comfy_models)
    
    for s in ["checkpoints", "loras", "vae", "clip", "controlnet", "embeddings", "upscale_models"]:
        os.makedirs(f"{MODELS_VOLUME_PATH}/{s}", exist_ok=True)

    # --- Custom Nodes Symlink ---
    os.makedirs(CUSTOM_NODES_VOLUME_PATH, exist_ok=True)
    comfy_nodes_dir = "/root/ComfyUI/custom_nodes"

    if os.path.isdir(comfy_nodes_dir) and not os.path.islink(comfy_nodes_dir):
        shutil.rmtree(comfy_nodes_dir)

    if not os.path.exists(comfy_nodes_dir):
        os.symlink(CUSTOM_NODES_VOLUME_PATH, comfy_nodes_dir)



# --------------------------------------------------------------------------
# 1. CPU Mode
# --------------------------------------------------------------------------
@app.cls(
    image=comfy_image,
    volumes={"/vol": models_volume},
    scaledown_window=300,
    timeout=7200,
    max_containers=1,
)
class ComfyUICPU:
    @modal.enter()
    def setup(self):
        _setup_model_symlink()

    @modal.web_server(port=8188, startup_timeout=180.0)
    def ui(self):
        subprocess.Popen(
            "python /root/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --cpu",
            shell=True,
        )


# --------------------------------------------------------------------------
# 2. GPU Mode
# --------------------------------------------------------------------------
@app.cls(
    gpu="A10G",
    image=comfy_image,
    volumes={"/vol": models_volume},
    scaledown_window=60,
    timeout=3600,
    max_containers=1,
)
class ComfyUIGPU:
    @modal.enter()
    def setup(self):
        _setup_model_symlink()

    @modal.web_server(port=8188, startup_timeout=180.0)
    def ui(self):
        subprocess.Popen(
            "python /root/ComfyUI/main.py --listen 0.0.0.0 --port 8188",
            shell=True,
        )


# --------------------------------------------------------------------------
# 3. Interactive Launcher
# --------------------------------------------------------------------------
launcher_image = modal.Image.debian_slim(python_version="3.10").pip_install("fastapi")


@app.function(image=launcher_image)
@modal.asgi_app(label="comfy-launcher")
def launcher():
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    web_app = FastAPI()

    LAUNCHER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaComfy Launcher</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0c0e14;
            --surface: #161923;
            --surface-hover: #1c2030;
            --border: rgba(255,255,255,0.08);
            --text: #e8eaed;
            --text-dim: #8b8fa3;
            --cpu-accent: #34d399;
            --cpu-bg: rgba(52,211,153,0.08);
            --cpu-border: rgba(52,211,153,0.2);
            --gpu-accent: #f59e0b;
            --gpu-bg: rgba(245,158,11,0.08);
            --gpu-border: rgba(245,158,11,0.2);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .launcher {
            max-width: 720px;
            width: 100%;
        }
        .header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        .header h1 {
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }
        .header p {
            color: var(--text-dim);
            font-size: 0.9rem;
            line-height: 1.5;
        }
        .modes {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
            margin-bottom: 2rem;
        }
        @media (max-width: 600px) {
            .modes { grid-template-columns: 1fr; }
        }
        .mode-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            transition: background 0.2s, border-color 0.2s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }
        .mode-card:hover {
            background: var(--surface-hover);
        }
        .mode-card.cpu:hover { border-color: var(--cpu-border); }
        .mode-card.gpu:hover { border-color: var(--gpu-border); }
        .mode-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0.3rem 0.65rem;
            border-radius: 6px;
            width: fit-content;
        }
        .cpu .mode-badge {
            background: var(--cpu-bg);
            color: var(--cpu-accent);
            border: 1px solid var(--cpu-border);
        }
        .gpu .mode-badge {
            background: var(--gpu-bg);
            color: var(--gpu-accent);
            border: 1px solid var(--gpu-border);
        }
        .mode-card h2 {
            font-size: 1.15rem;
            font-weight: 600;
        }
        .mode-card p {
            font-size: 0.82rem;
            color: var(--text-dim);
            line-height: 1.55;
        }
        .mode-card .cost {
            font-size: 0.78rem;
            color: var(--text-dim);
            border-top: 1px solid var(--border);
            padding-top: 0.75rem;
            margin-top: auto;
        }
        .cost strong {
            color: var(--text);
            font-weight: 600;
        }
        .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }
        .cpu .dot { background: var(--cpu-accent); }
        .gpu .dot { background: var(--gpu-accent); }
        .workflow-tip {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
        }
        .workflow-tip h3 {
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .workflow-tip ol {
            padding-left: 1.25rem;
            font-size: 0.85rem;
            color: var(--text-dim);
            line-height: 1.8;
        }
        .workflow-tip ol strong { color: var(--text); }
        .workflow-tip code {
            background: rgba(255,255,255,0.06);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="launcher">
        <div class="header">
            <h1>AlphaComfy Launcher</h1>
            <p>Split-architecture ComfyUI on Modal. Edit workflows for free on CPU, switch to GPU only when generating.</p>
        </div>

        <div class="modes">
            <a class="mode-card cpu" id="cpu-link" href="#" target="_blank">
                <span class="mode-badge"><span class="dot"></span> CPU Mode</span>
                <h2>Workflow Editor</h2>
                <p>Full native ComfyUI node editor. Build, connect, and configure your workflows. No GPU billing while you work.</p>
                <div class="cost">Idle: <strong>$0.00/hr</strong> &nbsp;·&nbsp; Active: <strong>~$0.03/hr</strong></div>
            </a>

            <a class="mode-card gpu" id="gpu-link" href="#" target="_blank">
                <span class="mode-badge"><span class="dot"></span> GPU Mode</span>
                <h2>Image Generation</h2>
                <p>Full ComfyUI on A10G GPU. Load your workflow, hit Queue Prompt, and render at full speed. Auto-shuts down after 60s idle.</p>
                <div class="cost">Idle: <strong>$0.00/hr</strong> &nbsp;·&nbsp; Active: <strong>~$1.10/hr</strong></div>
            </a>
        </div>

        <div class="workflow-tip">
            <h3>Workflow</h3>
            <ol>
                <li>Open <strong>CPU Mode</strong> and build your node graph</li>
                <li>Save your workflow: click the <strong>Save</strong> button in ComfyUI (or <code>Ctrl+S</code> to download JSON)</li>
                <li>Open <strong>GPU Mode</strong> when ready to render</li>
                <li>Load your saved workflow and click <strong>Queue Prompt</strong></li>
                <li>Close the GPU tab when done — it auto-shuts down in 60 seconds</li>
            </ol>
        </div>
    </div>

    <script>
        // Derive CPU/GPU URLs from the launcher's hostname
        const host = window.location.hostname;
        const workspace = host.split("--")[0];
        const domain = host.includes(".modal.run") ? "modal.run" : host.split(".").slice(-2).join(".");

        const cpuUrl = "https://" + workspace + "--alphacomfy-modal-comfyuicpu-ui." + domain;
        const gpuUrl = "https://" + workspace + "--alphacomfy-modal-comfyuigpu-ui." + domain;

        document.getElementById("cpu-link").href = cpuUrl;
        document.getElementById("gpu-link").href = gpuUrl;
    </script>
</body>
</html>"""

    @web_app.get("/", response_class=HTMLResponse)
    def index():
        return LAUNCHER_HTML

    return web_app