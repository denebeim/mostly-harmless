# Hermes Desktop: keep the files local, move inference first

2026-11-08, issue #5. The laptop source install, Eddie's old source install and the pinned Docker image all report Hermes 0.23.0, upstream 2bd378ed, Python 3.14.9 and OpenAI SDK 2.54.0. The image reports Docker installation. Laptop checkout source includes Desktop connection registry, SSH terminal, profile routing and roster code. This is source inspection, not a live Desktop connection test.

## Recommended split

1. Run Desktop and its local gateway on the laptop. Keep VSCodium, the working tree (including unsaved changes), Git credentials and commit decisions on the laptop. Use a local Hermes profile configured for Ollama on Eddie (`http://192.168.42.132:11434/v1`, `qwen3.5:4b`) for routine tasks. Tools execute with access to laptop files while the K5200 handles model inference. A cloud profile can remain an explicit choice for harder tasks; don't assume a failed provider automatically changes profiles or keeps the same session.
2. Add Eddie as a separate Desktop connection only for remote sessions and jobs that should outlive the laptop. Use SSH or a loopback backend through a tunnel. Do not publish the agent dashboard, Docker socket or browser workspace to the LAN. A remote file browser, terminal and agent see the remote environment. Use a disposable Git checkout on Eddie for long builds/tests; send an explicit commit or patch from the laptop, then review and apply the returned patch on the laptop. Never bidirectionally sync the laptop working tree, credentials or private NFS home into the container.
3. Choose the local and remote sessions deliberately in the Desktop connection selector. Use the roster for discovery and the shared gateway for profile routing. Keep remote background jobs constrained to their own project checkout. Enable cross-profile delegation only after a small, read-only test confirms the selected model, profile, host and file boundary.

## Features that matter here

- The [0.23.0 release notes](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.0) describe shared sessions and one gateway serving profiles. Eddie's container confirmed the installed CLI rejects a separate gateway for a named profile. A profile gives distinct settings and scope; it is not an OS security boundary.
- The [Desktop documentation](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/desktop.md) describes local, remote and SSH connections, a cross-gateway roster, and terminals tied to the selected host. Use this to choose execution location explicitly. Desktop, CLI and gateway can share a session on the same backend; a remote connection does not synchronize local files.
- The documented browser workspace can operate files and terminals with the agent account's privileges. It offers little benefit for the first pass on this LAN; leave it disabled. Keep authentication and credentials scoped to the chosen host. Do not copy one-time browser links or tokens into the session log.

## Performance acceptance

Start with laptop-local tools and Eddie inference. Compare the same short chat prompt and a small tool task after warm-up, then repeat a representative patch-and-test task. Track time to first response and end-to-end completion, plus Ollama's loaded model, GPU share, context size and any queuing. The historical 76-second response was a different prompt and is not a benchmark. Avoid concurrent requests until baseline is measured; increase context only if needed and check GPU residency. Compare output quality before substituting the local model for a cloud profile on complex edits.

Acceptance for a second, SSH-backed Desktop connection: a local session reads a laptop-only sentinel; a remote session reads an Eddie-only sentinel; a remote build continues through laptop disconnect; its output comes back as a patch without editing the laptop checkout. The shipped default profile is kept available but cloud inference requires separate configuration. Automatic quota-based fallback and cross-host file sync were not configured or tested.
