import modal
import sys

# ==========================================
# 📜 CONFIGURATION
# ==========================================
APP_NAME = "alphacore-installer-dr34ml4y"
VOLUME_NAME = "vo-jIx4luG87E8uTijb2Ut8Lu"
CIVITAI_SECRET_NAME = "civitai-secret"

# --- Model Details ---
MODEL_VERSION_ID = "2553271"
OUTPUT_FILENAME = "Dr34mL4Y_AllinOne_NSFW.safetensors"
SUBFOLDER = "checkpoints"
# ==========================================


# --- Modal App Definition ---
app = modal.App(APP_NAME)
cache_volume = modal.Volume.from_name(VOLUME_NAME)

# The image definition tells Modal what to install in the remote container.
# This is where 'tqdm' and 'requests' are specified for the remote environment.
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("requests", "tqdm")
)

def _get_secret():
    """Safely gets the Civitai secret if it exists."""
    try:
        return modal.Secret.from_name(CIVITAI_SECRET_NAME)
    except modal.exception.NotFoundError:
        print("ⓘ Civitai secret not found. Proceeding without an API key.")
        return None

@app.function(
    image=image,
    volumes={"/vol": cache_volume},
    timeout=3600,  # 1 hour
    secrets=[s for s in [_get_secret()] if s], # Only add secret if found
    region="us-west",
)
def install_model():
    """
    This is the core remote function that runs on Modal.
    All necessary imports are moved INSIDE this function.
    """
    # --- Imports for the REMOTE environment ---
    import os
    import requests
    from pathlib import Path
    from tqdm import tqdm

    def _stream_download(url: str, dest: Path, headers: dict = {}):
        """Helper function to download a file with a progress bar."""
        resp = requests.get(url, headers=headers, stream=True, timeout=60, allow_redirects=True)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        chunk_size = 1024 * 1024
        with open(dest, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, unit_divisor=1024, desc=dest.name,
        ) as bar:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        print(f"✅ Download complete: {dest} ({dest.stat().st_size / 1024**2:.1f} MB)")

    # --- Main download logic ---
    dest_dir = Path("/vol/models") / SUBFOLDER
    dest_dir.mkdir(parents=True, exist_ok=True)
    api_key = os.environ.get("CIVITAI_API_KEY", "")
    meta_url = f"https://civitai.com/api/v1/model-versions/{MODEL_VERSION_ID}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    print(f"🔍 Fetching Civitai metadata for version {MODEL_VERSION_ID}...")
    meta = requests.get(meta_url, headers=headers, timeout=30)
    if meta.status_code != 200:
        raise RuntimeError(f"Civitai API error {meta.status_code}: {meta.text[:300]}")
    
    meta_json = meta.json()
    model_name = meta_json.get("model", {}).get("name", "unknown")
    primary = next((f for f in meta_json.get("files", []) if f.get("primary", False)), None)
    if not primary: raise RuntimeError("No downloadable files found in Civitai response")

    download_url = primary["downloadUrl"] + (f"?token={api_key}" if api_key else "")
    dest_path = dest_dir / OUTPUT_FILENAME

    print(f"📦 Model: {model_name}")
    print(f"📄 File: {primary['name']}")
    print(f"📥 Saving to: {dest_path}")

    _stream_download(download_url, dest_path, headers=headers)
    cache_volume.commit()
    print("✅ Volume committed — model is ready.")


@app.local_entrypoint()
def main():
    """This function runs locally and triggers the remote download job."""
    print("🚀 AlphaCore Standalone Installer")
    print("===================================")
    print(f"   Destination: /vol/models/{SUBFOLDER}/{OUTPUT_FILENAME}")
    print("-----------------------------------")
    install_model.remote()
    print("\n🎉 Success! The download job has been dispatched to Modal.")
    print("   You can monitor its progress on your Modal dashboard.")