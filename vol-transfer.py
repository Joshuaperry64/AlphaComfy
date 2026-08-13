import shutil
from pathlib import Path
import modal

app = modal.App("volume-copier")

# Define your source and destination volumes
volume_source = modal.Volume.from_name("hf-hub-cache")
volume_dest = modal.Volume.from_name("vo-jIx4luG87E8uTijb2Ut8Lu", create_if_missing=True)

# Mount both volumes to different target directories
@app.function(
    volumes={
        "/mnt/source": volume_source,
        "/mnt/dest": volume_dest,
    }
)
def copy_between_volumes():
    src_dir = Path("/mnt/source/loras")
    dest_dir = Path("/mnt/dest/loras")
    
    # Perform standard Python filesystem operations
    if src_dir.is_dir():
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
    else:
        shutil.copy(src_dir, dest_dir)
        
    # Explicitly commit changes to ensure persistence
    volume_dest.commit()
    print("Copy completed successfully.")
