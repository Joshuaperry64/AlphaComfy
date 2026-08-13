import modal, os

app = modal.App("setup-dirs")
vol = modal.Volume.from_name("vo-jIx4luG87E8uTijb2Ut8Lu")

@app.function(volumes={"/vol": vol})
def setup():
    for path in [
        "/vol/models/checkpoints",
        "/vol/models/loras",
        "/vol/models/vae",
        "/vol/models/clip",
        "/vol/models/controlnet",
        "/vol/models/embeddings",
        "/vol/models/upscale_models",
        "/vol/custom_nodes",
    ]:
        os.makedirs(path, exist_ok=True)
        print(f"OK: {path}")
    vol.commit()
    print("Volume committed.")

@app.local_entrypoint()
def main():
    setup.remote()
