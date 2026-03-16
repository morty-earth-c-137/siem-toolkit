# OpSec Guide — Local Terminal Testing (Mac)
### How to Run This Tool Safely From Your Mac

---

> **What is OpSec?**
> "OpSec" stands for Operational Security — it means the practical habits and
> steps you take to keep credentials, data, and access safe while you work.
> This guide explains what to do (and what NOT to do) when running this tool
> locally on your Mac.

---

## Table of Contents

1. [The Golden Rules](#1-the-golden-rules)
2. [Credential Safety — Your .env File](#2-credential-safety--your-env-file)
3. [Keeping Your Token Safe](#3-keeping-your-token-safe)
4. [Terminal History — The Hidden Risk](#4-terminal-history--the-hidden-risk)
5. [Protecting Your Results Files](#5-protecting-your-results-files)
6. [Network Safety](#6-network-safety)
7. [Shared Computers](#7-shared-computers)
8. [Quick Safety Checklist](#8-quick-safety-checklist)

---

## 1. The Golden Rules

Follow these every time you use this tool:

1. **Never put your token in a command** — always use the `.env` file
2. **Never commit `.env` to Git** — it is blocked by `.gitignore`, but double-check
3. **Never share your token** in Slack, email, Teams, or any messaging app
4. **Lock your Mac** when stepping away — press `Cmd + Ctrl + Q`
5. **Use the virtual environment** — don't install packages globally

---

## 2. Credential Safety — Your .env File

Your `.env` file holds your Splunk hostname and token. It lives in the project
folder and must stay there — it must never be uploaded, emailed, or shared.

### What the .env file looks like
```
SPLUNK_HOST=mycompany.splunkcloud.com
SPLUNK_TOKEN=eyJr...your_token_here
```

### How to keep it safe

**Confirm it is ignored by Git**
Run this from the project folder:
```
git status
```
You should NOT see `.env` listed. If you do see it, stop immediately and
ask your team — it means `.gitignore` may be misconfigured.

**Set restrictive file permissions**
This prevents other users on the same Mac from reading your token:
```
chmod 600 .env
```
This means only you (the file owner) can read or edit it.

**Confirm the permission is set:**
```
ls -la .env
```
You should see: `-rw-------` at the start of the line. ✓

**Never hardcode credentials in scripts**
If you ever write your own scripts that use this project, always load
credentials from environment variables — never paste them directly into code.

---

## 3. Keeping Your Token Safe

Your Splunk Bearer Token is the key to your Splunk data. Treat it like a password.

### Do
- Store it only in your `.env` file
- Set a token expiry date in Splunk (90 days is a reasonable default)
- Use a token scoped to search-only permissions where possible
- Revoke and regenerate the token if you ever suspect it was exposed

### Don't
- Don't paste it into Terminal commands directly
- Don't copy it into a notes app, Notion, or any cloud service
- Don't share it with colleagues — each person should have their own token
- Don't reuse tokens across different projects

### How to revoke a token (if compromised)
1. Log in to Splunk Web
2. Go to **Settings > Tokens**
3. Find the token by name and click **Disable** or **Delete**
4. Generate a new one and update your `.env` file

---

## 4. Terminal History — The Hidden Risk

Your Mac's Terminal saves a history of every command you type. This is a risk
if someone ever accesses your Terminal — they could scroll back and see
sensitive commands.

### Why this matters
If you ever accidentally typed your token directly in a command like:
```
SPLUNK_TOKEN=mytoken python main.py ...   ← WRONG — never do this
```
That token would be saved in your Terminal history.

### This project protects you by design
This tool always reads the token from your `.env` file. You should never need
to type a token in a command. But it's good practice to know how to protect
your history anyway.

### How to clear Terminal history if needed
```
history -c
```
Or to clear the saved history file permanently:
```
cat /dev/null > ~/.zsh_history
```
> Note: On modern Macs the default shell is `zsh`. If you use `bash`, the
> file is `~/.bash_history` instead.

### Hide sensitive output from Terminal
If you're on a video call or screen share, run searches in a separate
Terminal window that isn't shared, and be careful scrolling through logs
that may contain sensitive data values.

---

## 5. Protecting Your Results Files

The `search_results/` folder contains CSV files with real data pulled from Splunk.
Depending on what you searched for, this could include sensitive log data.

### Treat results like sensitive documents

- Don't leave result CSVs in a Downloads folder or on your Desktop where
  others can see them
- Don't upload results to Google Drive, Dropbox, or any cloud storage
  unless your team has explicitly approved it
- Delete results you no longer need:
  ```
  rm search_results/*.csv
  ```
  Or empty the whole folder:
  ```
  rm -rf search_results && mkdir search_results
  ```

### Confirm the results folder is not tracked by Git
```
git status
```
`search_results/` should not appear. It is excluded by `.gitignore`.

---

## 6. Network Safety

### Always use HTTPS (this tool enforces it)
This tool only connects to Splunk over HTTPS (encrypted). It does not allow
plain HTTP connections. The Splunk Cloud endpoint uses port 8089 by default.

### SSL verification
SSL verification is **enabled by default** and should stay that way.
The only case where you might disable it is a local test Splunk instance
with a self-signed certificate — never for Splunk Cloud.

If you see `SPLUNK_VERIFY_SSL=false` in your `.env` file and you're connecting
to Splunk Cloud, change it back to `true`.

### Use a trusted network
Avoid running searches from public Wi-Fi (cafes, airports, hotels).
If you must, use a VPN first. Your Splunk token travels over the network and
should not be exposed on untrusted connections, even over HTTPS.

---

## 7. Shared Computers

If you're using a Mac that other people also use (e.g. a shared work machine):

- Store the project in your user home directory (`~/Documents/`), not in
  a shared location like `/Users/Shared/`
- Set restrictive permissions on your project folder:
  ```
  chmod -R 700 ~/Documents/splunk_client
  ```
  This means only your user account can enter the folder at all.
- Lock your Mac whenever you step away (`Cmd + Ctrl + Q`)
- Consider using macOS FileVault (full-disk encryption) —
  go to **System Preferences > Privacy & Security > FileVault**

---

## 8. Quick Safety Checklist

Run through this before each session:

- [ ] Virtual environment is active — I see `(venv)` in my Terminal prompt
- [ ] `.env` file exists and has correct values (I haven't accidentally deleted it)
- [ ] I'm on a trusted network, or on VPN
- [ ] `git status` shows `.env` is NOT tracked
- [ ] My screen is not being shared while viewing sensitive results
- [ ] I'll lock my Mac when I step away (`Cmd + Ctrl + Q`)

---

*For CI/CD and repository-level OpSec (GitLab/GitHub), see `docs/OPSEC_CICD.md`.*
