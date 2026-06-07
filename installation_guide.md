Below is the **final clean end-to-end setup runbook** for next time. Use this exactly for a new WSL2 Ubuntu LLM project.

---

# A. One-time WSL setup

Run inside **WSL Ubuntu**, not CMD/PowerShell:

```bash
cd ~

sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  build-essential \
  git \
  curl \
  wget \
  cmake \
  ninja-build \
  python3-pip \
  python3-venv
```

Check:

```bash
git --version
cmake --version
curl --version
ninja --version
```

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

Check GPU is visible inside WSL:

```bash
nvidia-smi
```

---

# B. Create main training project env

This env is for:

```text
SFT
LoRA
QLoRA
TRL
PEFT
bitsandbytes
MLflow
W&B
data prep
training
```

Run:

```bash
cd ~

mkdir -p ~/LLM_Ops
cd ~/LLM_Ops

uv python install 3.11
uv init --python 3.11
uv venv --python 3.11
source .venv/bin/activate

python --version
which python
```

Expected:

```text
Python 3.11.x
/home/rajiv/LLM_Ops/.venv/bin/python
```

---

# C. Create clean `pyproject.toml`

Run this inside `~/LLM_Ops`:

```bash
cat > pyproject.toml <<'EOF'
[project]
name = "llm-ops"
version = "0.1.0"
description = "Local LLM training, fine-tuning, evaluation, and LLMOps project"
readme = "README.md"
requires-python = ">=3.11,<3.12"
dependencies = [
    "accelerate>=1.13.0",
    "datasets>=2.14.4",
    "numpy>=2.4.4",
    "pandas>=2.2,<3",
    "pyarrow<21",
    "pydantic>=2.13.4",
    "python-dotenv>=1.2.2",
    "pyyaml>=6.0.3",
    "rich>=15.0.0",
    "safetensors>=0.7.0",
    "scikit-learn>=1.9.0",
    "scipy>=1.17.1",
    "sentencepiece>=0.2.1",
    "tokenizers>=0.22.2",
    "torch>=2.12.0",
    "torchaudio>=2.11.0",
    "torchvision>=0.27.0",
    "tqdm>=4.66.5",
    "transformers>=4.57.6",
    "typer>=0.26.7",
]

[[tool.uv.index]]
name = "pytorch-cu126"
url = "https://download.pytorch.org/whl/cu126"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cu126" }
torchvision = { index = "pytorch-cu126" }
torchaudio = { index = "pytorch-cu126" }

[dependency-groups]
train = [
    "bitsandbytes>=0.49.2",
    "deepspeed>=0.19.1",
    "einops>=0.8.2",
    "evaluate>=0.4.6",
    "mlflow>=3.5,<4",
    "peft>=0.19.1",
    "trl>=0.10.1",
    "wandb>=0.27.2",
]

serve = [
    "fastapi>=0.136.3",
    "openai>=2.41.0",
    "opentelemetry-api>=1.42.1",
    "opentelemetry-sdk>=1.42.1",
    "prometheus-client>=0.25.0",
    "sse-starlette>=3.4.4",
    "uvicorn>=0.49.0",
]

eval = [
    "pytest",
    "rouge-score",
    "bert-score",
    "sacrebleu",
    "matplotlib",
    "plotly",
]

rag = [
    "qdrant-client",
    "chromadb",
    "faiss-cpu",
    "sentence-transformers",
    "FlagEmbedding",
    "llama-index",
    "langchain",
    "rank-bm25",
    "ragas",
]

[tool.uv]
environments = [
    "sys_platform == 'linux' and platform_machine == 'x86_64'",
]
EOF
```

---

# D. Install main training env

Run:

```bash
UV_HTTP_TIMEOUT=600 UV_INDEX_STRATEGY=unsafe-best-match uv sync --group train --group serve
```

Then test base stack:

```bash
uv run python - <<'PY'
import torch, transformers, datasets, accelerate, tokenizers, pyarrow, pandas

print("BASE STACK OK")
print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
print("gpu:", torch.cuda.get_device_name(0))
print("torch cuda:", torch.version.cuda)
print("transformers:", transformers.__version__)
print("datasets:", datasets.__version__)
print("pyarrow:", pyarrow.__version__)
print("pandas:", pandas.__version__)
print("accelerate:", accelerate.__version__)
print("tokenizers:", tokenizers.__version__)
PY
```

Test training stack:

```bash
uv run python -c "import trl, peft, bitsandbytes, einops, wandb, mlflow, evaluate; print('training stack ok')"
```

Test bitsandbytes CUDA:

```bash
uv run python - <<'PY'
import torch
import bitsandbytes as bnb

print("torch cuda:", torch.cuda.is_available())
print("gpu:", torch.cuda.get_device_name(0))
print("bnb version:", bnb.__version__)

x = torch.randn(1024, 1024, device="cuda", dtype=torch.float16)
linear = bnb.nn.Linear8bitLt(1024, 1024).cuda()
y = linear(x)

print("bitsandbytes cuda test ok:", y.shape)
PY
```

Test API serving stack:

```bash
uv run python -c "import fastapi, uvicorn, openai, prometheus_client, opentelemetry; print('api serving stack ok')"
```

---

# E. Create separate vLLM env

Do **not** install vLLM inside the main training env.

Run:

```bash
cd ~

mkdir -p ~/LLM_Ops_vllm
cd ~/LLM_Ops_vllm

uv init --python 3.11
uv venv --python 3.11
source .venv/bin/activate

python --version
```

Install vLLM:

```bash
UV_HTTP_TIMEOUT=600 uv add "vllm>=0.22,<0.23" openai
```

Test:

```bash
uv run python -c "import vllm; print('vllm ok:', vllm.__version__)"
```

GPU test:

```bash
uv run python - <<'PY'
import torch

print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
print("gpu:", torch.cuda.get_device_name(0))
print("torch cuda:", torch.version.cuda)
PY
```

CLI test:

```bash
vllm --help | head -40
uv run python -m vllm.entrypoints.openai.api_server --help | head -40
```

Expected:

```text
vLLM CLI help appears
OpenAI API server help appears
```

The WSL warning below is okay:

```text
Using 'pin_memory=False' as WSL is detected.
```

---

# F. Create shared model folders

Run once:

```bash
mkdir -p ~/models/base
mkdir -p ~/models/adapters
mkdir -p ~/models/merged
mkdir -p ~/models/gguf
mkdir -p ~/models/vllm
mkdir -p ~/datasets/raw
mkdir -p ~/datasets/processed
mkdir -p ~/datasets/eval
```

Use:

```text
~/models/base      = downloaded base models
~/models/adapters  = LoRA / QLoRA adapters
~/models/merged    = merged HF models
~/models/gguf      = llama.cpp GGUF models
~/models/vllm      = vLLM-ready models
```

---

# G. Add easy aliases

Run:

```bash
cat >> ~/.bashrc <<'EOF'

# LLM Ops aliases
alias llm-train='cd ~/LLM_Ops && source .venv/bin/activate'
alias llm-serve='cd ~/LLM_Ops_vllm && source .venv/bin/activate'
alias llm-where='echo "PWD=$PWD"; echo "PYTHON=$(which python)"; python --version'
EOF

source ~/.bashrc
```

Usage:

```bash
llm-train
llm-where
```

Switch to vLLM:

```bash
deactivate
llm-serve
llm-where
```

---

# H. Final health checks

## Training env

```bash
llm-train

uv run python - <<'PY'
import torch, transformers, trl, peft, bitsandbytes, mlflow, wandb

print("TRAINING ENV OK")
print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
print("gpu:", torch.cuda.get_device_name(0))
print("transformers:", transformers.__version__)
print("trl:", trl.__version__)
print("peft:", peft.__version__)
print("bnb:", bitsandbytes.__version__)
print("mlflow:", mlflow.__version__)
PY
```

## vLLM env

```bash
llm-serve

uv run python - <<'PY'
import torch, vllm

print("VLLM ENV OK")
print("vllm:", vllm.__version__)
print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
print("gpu:", torch.cuda.get_device_name(0))
print("torch cuda:", torch.version.cuda)
PY
```

---

# I. Rules to avoid future breakage

Use these rules strictly:

```text
1. Use WSL2 Ubuntu, not Windows CMD, for LLM work.
2. Work inside /home/rajiv, not /mnt/c.
3. Use Python 3.11 only.
4. Use uv, not conda.
5. Keep training env and vLLM serving env separate.
6. Keep PyTorch index explicit, never loose/global.
7. Use UV_INDEX_STRATEGY=unsafe-best-match when syncing this project.
8. Do not install flash-attn at the beginning.
9. Do not install lighteval in the base/training env yet.
10. Do not force vLLM into the training env.
11. Pin pandas <3 because MLflow needs pandas 2.x.
12. Pin pyarrow <21 if using datasets 2.14.x.
```

---

# J. One-shot full setup summary

For a new machine/project, the core sequence is:

```bash
# WSL system setup
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget cmake ninja-build python3-pip python3-venv

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# training env
mkdir -p ~/LLM_Ops
cd ~/LLM_Ops
uv python install 3.11
uv init --python 3.11
uv venv --python 3.11
source .venv/bin/activate

# create pyproject.toml from section C
# then:
UV_HTTP_TIMEOUT=600 UV_INDEX_STRATEGY=unsafe-best-match uv sync --group train --group serve

# vLLM env
cd ~
mkdir -p ~/LLM_Ops_vllm
cd ~/LLM_Ops_vllm
uv init --python 3.11
uv venv --python 3.11
source .venv/bin/activate
UV_HTTP_TIMEOUT=600 uv add "vllm>=0.22,<0.23" openai

# shared folders
mkdir -p ~/models/base ~/models/adapters ~/models/merged ~/models/gguf ~/models/vllm
mkdir -p ~/datasets/raw ~/datasets/processed ~/datasets/eval
```

This is the stable setup we learned from the errors.
