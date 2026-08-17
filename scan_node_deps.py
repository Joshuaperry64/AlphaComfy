import modal
import os

app = modal.App("collect-deps")
vol = modal.Volume.from_name("vo-jIx4luG87E8uTijb2Ut8Lu")

@app.function(volumes={"/vol": vol})
def get_deps():
    custom_nodes_path = "/vol/custom_nodes"
    if not os.path.exists(custom_nodes_path):
        print("No custom_nodes directory found.")
        return []
    
    all_requirements = []
    nodes = os.listdir(custom_nodes_path)
    print(f"Installed Custom Nodes: {nodes}\n")
    
    for node in sorted(nodes):
        node_dir = os.path.join(custom_nodes_path, node)
        req_file = os.path.join(node_dir, "requirements.txt")
        if os.path.isfile(req_file):
            print(f"=== {node} / requirements.txt ===")
            with open(req_file, "r") as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                for l in lines:
                    print(f"  {l}")
                    all_requirements.append(l)
            print()
    return all_requirements

@app.local_entrypoint()
def main():
    get_deps.remote()
