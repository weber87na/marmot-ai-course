---
title: nemoclaw 安裝
date: 2026-03-24 13:47:51
tags: openclaw
---
&nbsp;
<!-- more -->

<iframe 
width="1235" 
height="772" 
src="https://www.youtube.com/embed/ohAxolloJDM" 
title="nemoclaw 安裝" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen>
</iframe>

跟風玩看看, 老黃的東西還是一樣機歪, 難裝複雜 ~ 網路太慢還不給裝, 果然不適合免費仔 LOL

安裝 VBoxLinuxAdditions
```
# 更新 ubuntu 套件
sudo apt update

# 安裝 vbox 相關套件
sudo apt install build-essential dkms linux-headers-$(uname -r)

# 更新 bashrc
source ~/.bashrc

# 安裝 VBoxLinuxAdditions
sudo sh VBoxLinuxAdditions.run

# 安裝好之後關機
poweroff
```


安裝 vim 跟 git
```
sudo apt install vim
sudo apt install git
```

docker 安裝
```
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 設定群組
sudo usermod -aG docker ${USER}
su - ${USER}
groups


# sudo systemctl status docker
# sudo systemctl restart docker
```

[nvm](https://github.com/nvm-sh/nvm) 安裝
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
source ~/.bashrc
nvm install 22
node -v
```


安裝 nemoclaw
nemoclaw [文件](https://docs.nvidia.com/nemoclaw/latest/index.html)
nemoclaw [github](https://github.com/NVIDIA/NemoClaw)


這裡要注意下資源分配, 我自己一開始沒注意到是用 virtualbox 預設, 然後裝起來馬上磁碟滿了 XD
建議用他推薦以上的資源, 不然應該很卡, 老黃的東西不意外, 免費仔的惡夢


| Resource | Minimum | Recommended |
| :--- | :--- | :--- |
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | 16 GB |
| Disk | 20 GB free | 40 GB free |


```
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```

遇到 `Docker is not running. Please start Docker and try again` 表示群組沒有設定好

遇到 `openshell gateway start fails with "K8s namespace not ready"` 表示網路問題, 多試幾次應該就過了
可以參考[這裡](https://build.nvidia.com/spark/openshell/troubleshooting)


遇到 k3s 問題[參考這裡](https://github.com/NVIDIA/NemoClaw/blob/main/spark-install.md)

```
vim /etc/docker/daemon.json

{
	"default-cgroupns-mode": "host"
}
```

安裝過程會長這樣
```
[1/3] Node.js
  ──────────────────────────────────────────────────
[INFO]  Node.js found: v22.22.1
[INFO]  Runtime OK: Node.js v22.22.1, npm 10.9.4

[2/3] NemoClaw CLI
  ──────────────────────────────────────────────────
[INFO]  Installing NemoClaw from GitHub…
  ✓  Cloning NemoClaw source
  ✓  Preparing OpenClaw package
  ✓  Installing NemoClaw dependencies
  ✓  Building NemoClaw plugin
  ✓  Linking NemoClaw CLI
[INFO]  Verified: nemoclaw is available at /home/marmot/.nvm/versions/node/v22.22.1/bin/nemoclaw

  ──────────────────────────────────────────────────
[WARN]  Your current shell may not have the updated PATH.

  To use nemoclaw now, run:

    source /home/marmot/.bashrc

  Or open a new terminal window.
  ──────────────────────────────────────────────────


[3/3] Onboarding
  ──────────────────────────────────────────────────
[INFO]  Running nemoclaw onboard…
[INFO]  Installer stdin is piped; attaching onboarding to /dev/tty…

  NemoClaw Onboarding
  ===================

  [1/7] Preflight checks
  ──────────────────────────────────────────────────
  ✓ Docker is running
  ✓ Container runtime: docker
  ✓ openshell CLI: openshell 0.0.14
  ✓ Port 8080 available (OpenShell gateway)
  ✓ Port 18789 available (NemoClaw dashboard)
  ⓘ No GPU detected — will use cloud inference

  [2/7] Starting OpenShell gateway
  ──────────────────────────────────────────────────
  Using pinned OpenShell gateway image: ghcr.io/nvidia/openshell/cluster:0.0.14
✓ Checking Docker
✓ Downloading gateway
✓ Initializing environment
✓ Starting gateway                                                              
✓ Gateway ready

  Name: nemoclaw
  Endpoint: https://127.0.0.1:8080

✓ Active gateway set to 'nemoclaw'
  ✓ Gateway is healthy

  [3/7] Creating sandbox
  ──────────────────────────────────────────────────
  Sandbox name (lowercase, numbers, hyphens) [my-assistant]: 
  Creating sandbox 'my-assistant' (this takes a few minutes on first run)...
  Building image openshell/sandbox-from:1774326302 from /tmp/nemoclaw-build-0nO57C/Dockerfile
  Built image openshell/sandbox-from:1774326302
  Pushing image openshell/sandbox-from:1774326302 into gateway "nemoclaw"
  [progress] Exported 1172 MiB
  [progress] Uploaded to gateway
  Image openshell/sandbox-from:1774326302 is available in the gateway.
  Waiting for sandbox to become ready...
✓ Forwarding port 18789 to sandbox my-assistant in the background
  Access at: http://127.0.0.1:18789/
  Stop with: openshell forward stop 18789 my-assistant
  ✓ Sandbox 'my-assistant' created

  [4/7] Configuring inference (NIM)
  ──────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────┐
  │  NVIDIA API Key required                                        │
  │                                                                 │
  │  1. Go to https://build.nvidia.com/settings/api-keys            │
  │  2. Sign in with your NVIDIA account                            │
  │  3. Click 'Generate API Key' button                             │
  │  4. Paste the key below (starts with nvapi-)                    │
  └─────────────────────────────────────────────────────────────────┘

  NVIDIA API Key: nvapi-yourapikey-xxxxxxxxxxxxxxxxxxxxxxxxxxx

  Key saved to ~/.nemoclaw/credentials.json (mode 600)


  Cloud models:
    1) Nemotron 3 Super 120B (nvidia/nemotron-3-super-120b-a12b)
    2) Kimi K2.5 (moonshotai/kimi-k2.5)
    3) GLM-5 (z-ai/glm5)
    4) MiniMax M2.5 (minimaxai/minimax-m2.5)
    5) Qwen3.5 397B A17B (qwen/qwen3.5-397b-a17b)
    6) GPT-OSS 120B (openai/gpt-oss-120b)

  Choose model [1]: 
  Using NVIDIA Endpoint API with model: nvidia/nemotron-3-super-120b-a12b

  [5/7] Setting up inference provider
  ──────────────────────────────────────────────────
✓ Created provider nvidia-nim
Gateway inference configured:

  Route: inference.local
  Provider: nvidia-nim
  Model: nvidia/nemotron-3-super-120b-a12b
  Version: 1
  ✓ Inference route set: nvidia-nim / nvidia/nemotron-3-super-120b-a12b

  [6/7] Setting up OpenClaw inside sandbox
  ──────────────────────────────────────────────────
  ✓ OpenClaw gateway launched inside sandbox

  [7/7] Policy presets
  ──────────────────────────────────────────────────

  Available policy presets:
    ○ discord — Discord API, gateway, and CDN access
    ○ docker — Docker Hub and NVIDIA container registry access
    ○ huggingface — Hugging Face Hub, LFS, and Inference API access
    ○ jira — Jira and Atlassian Cloud access
    ○ npm — npm and Yarn registry access (suggested)
    ○ outlook — Microsoft Outlook and Graph API access
    ○ pypi — Python Package Index (PyPI) access (suggested)
    ○ slack — Slack API and webhooks access
    ○ telegram — Telegram Bot API access

  Apply suggested presets (pypi, npm)? [Y/n/list]: 
✓ Policy version 2 submitted (hash: 474f72d768f0)
✓ Policy version 2 loaded (active version: 2)
  Applied preset: pypi
✓ Policy version 3 submitted (hash: 462a3f55b4da)
✓ Policy version 3 loaded (active version: 3)
  Applied preset: npm
  ✓ Policies applied

  ──────────────────────────────────────────────────
  Sandbox      my-assistant (Landlock + seccomp + netns)
  Model        nvidia/nemotron-3-super-120b-a12b (NVIDIA Endpoint API)
  NIM          not running
  ──────────────────────────────────────────────────
  Next:
  Run:         nemoclaw my-assistant connect
  Status:      nemoclaw my-assistant status
  Logs:        nemoclaw my-assistant logs --follow
  ──────────────────────────────────────────────────

[INFO]  === Installation complete ===

  NemoClaw  (3484s)

  Your OpenClaw Sandbox is live.
  Sandbox in, break things, and tell us what you find.

  Next:
  $ nemoclaw my-assistant connect
  sandbox@my-assistant$ openclaw tui

  GitHub  https://github.com/nvidia/nemoclaw
  Docs    https://docs.nvidia.com/nemoclaw/latest/

```

