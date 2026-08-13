# Native ComfyUI on Modal Serverless

Run the **full native ComfyUI node graph web interface** on [Modal.com](https://modal.com) with on-demand GPU acceleration and zero idle billing.

## Highlights
- **Full Native ComfyUI Web UI**: Access the complete ComfyUI node canvas, workflow editor, queue, history, and previewer in your browser.
- **Serverless Billing ($0 Idle)**: The GPU container automatically spins up when you open the URL and shuts down 60 seconds after closing your browser tab.
- **Mounted Model Storage**: Volume `vo-jIx4luG87E8uTijb2Ut8Lu` is mounted to `/root/ComfyUI/models`.

---

## 1. Uploading Models to Modal Volume (`vo-jIx4luG87E8uTijb2Ut8Lu`)

```bash
# Upload a checkpoint file
modal volume put vo-jIx4luG87E8uTijb2Ut8Lu path/to/v1-5-pruned-emaonly.ckpt /checkpoints/

# Upload a LoRA file
modal volume put vo-jIx4luG87E8uTijb2Ut8Lu path/to/style.safetensors /loras/

# Check volume files
modal volume ls vo-jIx4luG87E8uTijb2Ut8Lu
```

---

## 2. Deploying

Deploy to Modal:

```bash
modal deploy main.py
```

Modal will output your application URL (e.g., `https://<your-username>--alphacomfy-modal-ui.modal.run`). Open that URL in your browser to access the full native ComfyUI web app!
