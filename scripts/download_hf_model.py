import argparse
from huggingface_hub import snapshot_download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", type=str, required=True, help="HuggingFace model repo ID")
    parser.add_argument("--local-dir", type=str, required=True, help="Local directory to download to")
    args = parser.parse_args()

    print(f"Downloading {args.repo_id} to {args.local_dir}...")
    
    # We ignore large safetensors.index.json or heavy non-fp16 variants if needed, 
    # but for snapshot_download we usually just get everything.
    # To save space, we can filter to only download the safetensors.
    snapshot_download(
        repo_id=args.repo_id,
        local_dir=args.local_dir,
        ignore_patterns=["*.msgpack", "*.h5", "*.pt", "*.ckpt", "*.bin"], # Download safetensors
        local_dir_use_symlinks=False
    )
    
    print("Download complete.")

if __name__ == "__main__":
    main()
