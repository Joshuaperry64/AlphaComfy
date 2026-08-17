raw = """accelerate, addict, aiohappyeyeballs, aiohttp, aiosignal, albucore, albumentations, aliyun-python-sdk-core, aliyun-python-sdk-kms, annotated-doc, annotated-types, antlr4-python3-runtime, anyascii, anyio, argbind, async-timeout, attrs, audioread, av, beautifulsoup4, boto3, botocore, brotli, certifi, cffi, charset_normalizer, click, cmake, colour-science, contourpy, contractions, crcmod, cryptography, cycler, Cython, datasets, decorator<5.0,>=4.0.2, demucs, dill, diskcache, docstring-parser, easydict, einops, exceptiongroup, fairscale, fastapi, filelock, fonttools, frozenlist, fsspec, funasr, gdown, git+https://github.com/WASasquatch/cstr.git, git+https://github.com/WASasquatch/ffmpy.git, git+https://github.com/WASasquatch/img2texture.git, gitdb, gitpython, google-ai-generativelanguage, google-api-core, google-api-python-client, google-auth, google-auth-httplib2, google-generativeai, googleapis-common-protos, gradio, gradio-client, groovy, grpcio, grpcio-status, h11, hf-gradio, hf-xet, httpcore, httplib2, httpx, huggingface_hub, hydra-core, idna, imageio, inflect, jaconv, jamo, jieba, jinja2, jmespath, joblib, jsonschema, jsonschema-specifications, julius, kaldifst, kaldiio, kiwisolver, kornia, kornia_rs, lameenc, lazy-loader, librosa, lightning-utilities, llama-cpp-python, llvmlite, markdown-it-py, markupsafe, matplotlib, mdurl, modelscope, modelscope-hub, more-itertools, mpmath, msgpack, multidict, multiprocess, networkx, numba, numpy, ollama, omegaconf, openai-whisper, opencv-python-headless, orjson, oss2, packaging, pandas, pathspec, pilgram, pillow, pixeloe, platformdirs, pooch, propcache, proto-plus, protobuf, psutil, pyahocorasick, pyarrow, pyasn1, pyasn1-modules, pycocoevalcap, pycocotools, pycparser, pycryptodome, pydantic, pydantic-core, pydub, pygments, pymatting, pynndescent, pyparsing, PySocks, python-dateutil, python-dotenv, python-multipart, pytorch_lightning, pytz, pywavelets, pyyaml, qrcode, rapidfuzz, referencing, regex, rembg, requests, rich, rpds-py, s3transfer, safehttpx, safetensors, scikit-build-core, scikit-image, scikit-learn, scipy, segment_anything, semantic-version, sentencepiece, setuptools, shellingham, simplejson, simsimd, six, smmap, sortedcontainers, soundfile, soupsieve, soxr, spaces, sphn, stable-ts, starlette, stringzilla, sympy, tensorboardX, textsearch, threadpoolctl, tifffile, tiktoken, timm, tokenizers, tomli, tomlkit, torch_complex, torchcodec, torchmetrics, tqdm, transformers, transparent-background, typeguard, typer, typing-extensions, typing-inspection, tzdata, umap_learn, uritemplate, urllib3, uvicorn, voxcpm, websockets, wetext, wget, xxhash, yarl, PyOpenGL, PyOpenGL-accelerate, glfw, diffusers, peft, spandrel, clip_interrogator, rotarty_embedding_torch, torchdiffeq, gguf, piexif, webcolors, cachetools, color-matcher, mss, sounddevice, imageio-ffmpeg, pyloudnorm, moviepy==1.0.3, reportlab, PyPDF2, pdf2image, PyMuPDF, openai, fal-client, runwayml, google-genai, google-cloud-storage, PyGithub, matrix-nio, toml, uv, chardet"""

items = [x.strip() for x in raw.split(",") if x.strip()]
seen = {}

for it in items:
    key = it.lower().replace("_", "-")
    if "==" in key:
        k = key.split("==")[0]
    elif ">=" in key:
        k = key.split(">=")[0]
    elif "<" in key:
        k = key.split("<")[0]
    else:
        k = key
    
    if k not in seen:
        seen[k] = it

canonical = sorted(list(seen.values()), key=lambda s: s.lower())
print(f"Total Unique Canonical Packages: {len(canonical)}")

with open("packages_clean.py", "w") as f:
    f.write("PACKAGES = [\n" + ",\n".join(f'    "{p}"' for p in canonical) + "\n]\n")
