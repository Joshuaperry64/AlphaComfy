import modal

app = modal.App("clone-custom-node")
vol = modal.Volume.from_name("vo-jIx4luG87E8uTijb2Ut8Lu")

image = modal.Image.debian_slim(python_version="3.10").apt_install("git")

@app.function(volumes={"/vol": vol}, image=image)
def clone():
    import subprocess, os
    dest = "/vol/custom_nodes/ComfyUI-Manager"
    if os.path.exists(dest):
        print("Already exists, pulling latest...")
        subprocess.check_call(["git", "-C", dest, "pull"])
    else:
        print("Cloning ComfyUI-Manager...")
        subprocess.check_call(["git", "clone", "https://github.com/ltdrdata/ComfyUI-Manager", dest])
    vol.commit()
    print("Done. Volume committed.")

@app.local_entrypoint()
def main():
    clone.remote()
