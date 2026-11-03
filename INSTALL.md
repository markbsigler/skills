# Install the aha-feature skill

[aha-feature](aha-feature/SKILL.md) is an [Agent Skill](https://agentskills.io/): a folder with a `SKILL.md` file, reference docs, and helper scripts. GitHub Copilot and Cursor load it from a skills folder, and the skill reads and writes Aha! records through the Aha! MCP server. These steps cover VS Code with GitHub Copilot, GitHub Copilot CLI, and Cursor on your computer.

1. [Check the prerequisites](#step-1-check-the-prerequisites)
2. [Install the skill files](#step-2-install-the-skill-files)
3. [Connect the Aha! MCP server](#step-3-connect-the-aha-mcp-server)
4. [Verify the installation](#step-4-verify-the-installation)

The same steps install the other skills in this repository: replace `aha-feature` with the skill's folder name, and skip step 3, which only aha-feature needs.

## Step 1: Check the prerequisites

- **An AI client:** VS Code with GitHub Copilot, GitHub Copilot CLI, or Cursor. Update to the latest version; older versions don't load Agent Skills.
- **Aha! access:** an account at `https://<your-company>.aha.io` with contributor permissions or higher. An Aha! account administrator turns on AI functionality and MCP server access under **Settings → Account → AI controls**. Read and write access are separate settings, and the skill needs both.
- **Python 3.11 or later** for the helper scripts. Check with `python3 --version` (Windows: `py --version`). Or install [uv](https://docs.astral.sh/uv/getting-started/installation/) (macOS: `brew install uv`), which downloads a matching Python when the skill runs a script.
- **A way to download the skill:** [GitHub CLI](https://cli.github.com/) 2.90 or later (`gh --version`), git, or a web browser.

Review a skill before you install it: a skill holds instructions and scripts that your agent runs. Read [aha-feature on GitHub](https://github.com/markbsigler/skills/tree/main/aha-feature), or run `gh skill preview markbsigler/skills aha-feature`. Its scripts use only the Python standard library and make no network calls. The skill reaches Aha! only through the MCP server, and it writes only after you approve the exact content.

## Step 2: Install the skill files

### Choose a location

Install the skill for yourself, in your home folder, or for everyone who works in a repository, in that repository.

| Client | Personal: all your projects | Project: one repository |
| --- | --- | --- |
| GitHub Copilot (VS Code and Copilot CLI) | `~/.copilot/skills/aha-feature/` | `.github/skills/aha-feature/` |
| Cursor | `~/.cursor/skills/aha-feature/` | `.cursor/skills/aha-feature/` |
| Both | Install in both folders above | `.agents/skills/aha-feature/` |

- Copy the whole folder, not only `SKILL.md`. The skill uses its `scripts/`, `references/`, and `assets/` folders.
- Keep the folder name `aha-feature`. It must match the `name` in `SKILL.md`, or the skill doesn't load.
- On Windows, `~` is your user profile folder (`%USERPROFILE%`).

Then use one of the following options.

### Option A: GitHub CLI (recommended)

`gh skill`, in public preview in GitHub CLI 2.90 and later, downloads the skill into the right folder and records its source, so one command updates it later.

```bash
# GitHub Copilot, for you: ~/.copilot/skills/aha-feature
gh skill install markbsigler/skills aha-feature --agent github-copilot --scope user

# Cursor, for you: ~/.cursor/skills/aha-feature
gh skill install markbsigler/skills aha-feature --agent cursor --scope user

# One repository, for Copilot and Cursor: .agents/skills/aha-feature
# Run it inside the repository, then commit the folder to share it.
gh skill install markbsigler/skills aha-feature --agent github-copilot --scope project
```

`gh skill` adds a `metadata` block with the source repository and version to the installed `SKILL.md`; `gh skill update` uses it.

### Option B: git

macOS or Linux:

```bash
git clone --depth 1 https://github.com/markbsigler/skills.git /tmp/markbsigler-skills

# GitHub Copilot
mkdir -p ~/.copilot/skills
cp -R /tmp/markbsigler-skills/aha-feature ~/.copilot/skills/

# Cursor
mkdir -p ~/.cursor/skills
cp -R /tmp/markbsigler-skills/aha-feature ~/.cursor/skills/

rm -rf /tmp/markbsigler-skills
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/markbsigler/skills.git "$env:TEMP\markbsigler-skills"

# GitHub Copilot
New-Item -ItemType Directory -Force "$HOME\.copilot\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\markbsigler-skills\aha-feature" "$HOME\.copilot\skills\"

# Cursor
New-Item -ItemType Directory -Force "$HOME\.cursor\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\markbsigler-skills\aha-feature" "$HOME\.cursor\skills\"

Remove-Item -Recurse -Force "$env:TEMP\markbsigler-skills"
```

### Option C: ZIP download

1. Download [the repository as a ZIP file](https://github.com/markbsigler/skills/archive/refs/heads/main.zip) and unzip it.
2. Find the `aha-feature` folder inside the `skills-main` folder.
3. Copy the `aha-feature` folder into a skills folder from the table, such as `~/.copilot/skills/` or `~/.cursor/skills/`. Create the skills folder if it doesn't exist. The macOS Finder hides folders whose names start with a dot; choose **Go → Go to Folder** and enter the path to open one.

Already manage your skills with [skillshare](https://github.com/runkids/skillshare)? Run `skillshare install markbsigler/skills/aha-feature`, then `skillshare sync`.

## Step 3: Connect the Aha! MCP server

The skill reads and writes Aha! through the Aha! remote MCP server. Add the server once in each client you use.

- **Server URL:** `https://<your-company>.aha.io/api/v1/mcp`, with the subdomain from your Aha! address.
- **Sign-in:** OAuth in your browser the first time the client connects. You don't need an API key. Don't create an OAuth application in Aha!: the client registers itself, and a manually created application can't authenticate an MCP connection.
- **Permissions:** the client acts as you, with your Aha! permissions. Its changes appear under your name in Aha! audit logs and activity.

### GitHub Copilot CLI

```bash
copilot mcp add --transport http aha https://<your-company>.aha.io/api/v1/mcp
```

The command saves the server in `~/.copilot/mcp-config.json`. Start `copilot`, and sign in to Aha! when your browser opens. If the server shows that it needs authentication, enter `/mcp`, select **aha**, and authenticate.

### VS Code

1. Open the Command Palette (**Cmd+Shift+P** on macOS, **Ctrl+Shift+P** on Windows and Linux) and run **MCP: Add Server**.
2. Choose **HTTP (HTTP or Server-Sent Events)**.
3. Paste `https://<your-company>.aha.io/api/v1/mcp`.
4. Enter `aha` as the server ID.
5. Choose **Global**, then **Copilot Global**. VS Code saves the server in `~/.copilot/mcp-config.json`, the file Copilot CLI uses, so one entry serves both. If **Copilot Global** isn't offered, choose your user profile configuration instead.
6. Accept the trust prompt, then sign in to Aha! when VS Code asks.

To edit the file instead, add the `aha` entry under `mcpServers` in `~/.copilot/mcp-config.json`, and keep any servers already there:

```json
{
  "mcpServers": {
    "aha": {
      "type": "http",
      "url": "https://<your-company>.aha.io/api/v1/mcp",
      "tools": ["*"]
    }
  }
}
```

### Cursor

1. Open `~/.cursor/mcp.json` to use the server in all your projects, or `.cursor/mcp.json` in a project to use it there only. Create the file if it doesn't exist.
2. Add the `aha` entry under `mcpServers`, and keep any servers already there:

   ```json
   {
     "mcpServers": {
       "aha": {
         "url": "https://<your-company>.aha.io/api/v1/mcp"
       }
     }
   }
   ```

3. Open **Customize** in the sidebar (in older versions, the MCP section of **Cursor Settings**). Check that **aha** is turned on, and sign in to Aha! in your browser when Cursor prompts you.

### If the client can't sign in to a remote server

Run [mcp-remote](https://www.npmjs.com/package/mcp-remote) as a local bridge; it handles the OAuth sign-in and needs Node.js. For Copilot CLI and VS Code, remove the HTTP entry first if you added it:

```bash
copilot mcp remove aha
copilot mcp add aha -- npx -y mcp-remote https://<your-company>.aha.io/api/v1/mcp
```

For Cursor, replace the `aha` entry in `mcp.json`:

```json
"aha": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://<your-company>.aha.io/api/v1/mcp"]
}
```

## Step 4: Verify the installation

1. **The skill loads.** Start a new chat or session, then:
   - VS Code: type `/` in the Chat view and look for **aha-feature**, or run **Chat: Open Customizations** and open **Skills**.
   - Copilot CLI: run `/skills list`. If the session was open when you installed the skill, run `/skills reload` first.
   - Cursor: type `/aha-feature` in Agent chat.
2. **The scripts run.** Use the folder where you installed the skill:

   ```bash
   uv run ~/.copilot/skills/aha-feature/scripts/aha_feature.py --help
   # or, without uv:
   python3 ~/.cursor/skills/aha-feature/scripts/aha_feature.py --help
   ```

   The help lists the subcommands `bundle`, `lint`, `render`, `matrix`, `fingerprint`, `verify`, and `export`.
3. **Aha! is connected.** Check that the **aha** server is running and lists its tools: run **MCP: List Servers** in VS Code, enter `/mcp` in Copilot CLI, or open **Customize** in Cursor.
4. **A read-only review works.** In agent mode, replace `APP-123` with one of your feature references and enter:

   ```text
   /aha-feature Review APP-123 against the elicitation matrix. Review only; don't change anything in Aha!.
   ```

   The agent reads the feature with Aha! tools such as `fields_metadata` and `read_records`, then reports its findings. It writes to Aha! only after you approve the exact content.

## Update or remove the skill

- **Update:** if you installed with `gh skill`, run `gh skill update aha-feature`. With skillshare, run `skillshare update aha-feature`, then `skillshare sync`. Otherwise, delete the `aha-feature` folder and repeat step 2.
- **Remove:** delete the `aha-feature` folder from each place you installed it, for example `rm -rf ~/.copilot/skills/aha-feature ~/.cursor/skills/aha-feature`. To disconnect Aha!, run `copilot mcp remove aha`, or delete the `aha` entry from `~/.copilot/mcp-config.json` or `~/.cursor/mcp.json`.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| The skill doesn't appear | `SKILL.md` must sit directly in a folder named `aha-feature`, such as `~/.copilot/skills/aha-feature/SKILL.md`, not a level deeper, such as `~/.copilot/skills/skills-main/aha-feature/SKILL.md`. Then start a new chat, run `/skills reload` in Copilot CLI, or restart the editor. |
| The agent doesn't pick the skill | Invoke it with `/aha-feature`, or name it in the prompt: "Use the aha-feature skill to review APP-123." |
| No Aha! tools, or sign-in fails | Check that the URL uses your company's subdomain and ends in `/api/v1/mcp`. Ask an Aha! administrator to confirm that AI functionality and MCP access are on under **Settings → Account → AI controls**, and that you have contributor permissions. |
| The agent reads Aha! but can't write | MCP read and write access are separate settings. Ask an Aha! administrator to turn on write access; until then, use the skill's Review mode. |
| Throttling or "Unknown tool" errors during long updates | Aha! allows 300 requests per minute per account and IP address. The skill paces its writes and retries; wait a minute, then ask the agent to continue. |
| `python3` isn't found | Install Python 3.11 or later, or uv. On Windows, the Python command is `py` or `python`. |
| Shell commands fail on Windows | The skill's helper commands use POSIX shell syntax. Use Git Bash or WSL as the agent's terminal, or ask the agent to use PowerShell equivalents. |
