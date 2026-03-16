# How To Use the Splunk API Client
### A Step-by-Step Guide for Getting Up and Running

---

> **Before you start:** This guide is written for someone comfortable using a Mac
> but who hasn't coded before. Every step is explained in plain English.
> If something doesn't work, check the **Troubleshooting** section at the bottom.

---

## Table of Contents

1. [What This Tool Does](#1-what-this-tool-does)
2. [What You Need Before You Start](#2-what-you-need-before-you-start)
3. [Install Python](#3-install-python)
4. [Download the Project](#4-download-the-project)
5. [Set Up a Virtual Environment](#5-set-up-a-virtual-environment)
6. [Install the Dependencies](#6-install-the-dependencies)
7. [Configure Your Credentials](#7-configure-your-credentials)
8. [Get Your Splunk Token](#8-get-your-splunk-token)
9. [Run Your First Search](#9-run-your-first-search)
10. [Run a Search from an Excel File](#10-run-a-search-from-an-excel-file)
11. [Where to Find Your Results](#11-where-to-find-your-results)
12. [Usage Examples](#12-usage-examples)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. What This Tool Does

This tool lets you send search queries to Splunk Cloud from your Mac's Terminal
(the command-line app on your Mac). It's like having a search bar for your
Splunk data, but run from your computer.

**What it does for you:**
- Sends a search query to Splunk and waits for results
- Saves those results as a spreadsheet file (`.csv`) you can open in Excel
- Tells you in plain language if something goes wrong (wrong token, bad query, etc.)
- Can run a whole list of searches from an Excel file automatically

---

## 2. What You Need Before You Start

- A Mac (this guide is written for macOS)
- Internet access
- A Splunk Cloud account with permission to run searches
- The project files (given to you by your team)

---

## 3. Install Python

Python is the programming language this tool is written in. You need version 3.10 or higher.

### Check if Python is already installed

1. Open **Terminal**
   - Press `Cmd + Space`, type `Terminal`, press `Enter`

2. Type this and press `Enter`:
   ```
   python3 --version
   ```

3. If you see something like `Python 3.11.4`, you're good — skip to Step 4.
   If you see `command not found` or a version lower than `3.10`, continue below.

### Install Python (if needed)

1. Go to: **https://www.python.org/downloads/mac-osx/**
2. Click the big yellow **Download Python 3.x.x** button
3. Open the downloaded `.pkg` file and follow the installer steps (click Continue, Agree, Install)
4. When it's done, close and reopen Terminal, then type `python3 --version` again to confirm

---

## 4. Download the Project

Your team will give you the project either as a ZIP file or a Git repository link.

### Option A — ZIP file (simplest)

1. Find the ZIP file your team sent you (e.g. `splunk_client.zip`)
2. Double-click it to unzip — this creates a folder called `splunk_client`
3. Move this folder somewhere easy to find, like your Desktop or Documents

### Option B — From Git

1. In Terminal, navigate to where you want to put the project:
   ```
   cd ~/Documents
   ```
2. Clone the repository (your team will give you the URL):
   ```
   git clone https://github.com/your-org/splunk-client.git
   ```
3. This creates a `splunk-client` folder in your Documents

---

## 5. Set Up a Virtual Environment

A virtual environment is a clean, isolated space for this project's tools.
It keeps everything organised and prevents conflicts with other software on your Mac.

> Think of it like a separate toolbox just for this project.

1. In Terminal, navigate into the project folder.
   If you put it on your Desktop:
   ```
   cd ~/Desktop/splunk_client
   ```
   If you put it in Documents:
   ```
   cd ~/Documents/splunk_client
   ```

2. Create the virtual environment:
   ```
   python3 -m venv venv
   ```
   You'll see a new folder called `venv` appear inside the project folder.

3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
   You'll notice your Terminal prompt now shows `(venv)` at the start.
   This means the virtual environment is active. ✓

> **Important:** Every time you open a new Terminal window to use this tool,
> you need to navigate to the project folder and run `source venv/bin/activate` again.

---

## 6. Install the Dependencies

Dependencies are the extra tools and libraries that this project needs to run.

With your virtual environment active (you should see `(venv)` in your prompt), type:

```
pip install -r requirements.txt
```

You'll see a bunch of text scroll past — that's normal. It's downloading and
installing everything needed. When it's done, your prompt will appear again.

---

## 7. Configure Your Credentials

Your credentials live in a file called `settings.py` inside the `splunk_client` folder.
This is just a plain Python file — you open it like any text file and fill in two values.

1. Open `settings.py` in TextEdit:
   ```
   open -a TextEdit splunk_client/settings.py
   ```
   > If TextEdit opens it as a formatted document, go to **Format > Make Plain Text**

2. Find these two lines near the top:
   ```python
   SPLUNK_HOST  = "your-organisation.splunkcloud.com"  # <-- SET THIS
   SPLUNK_TOKEN = "paste-your-token-here"              # <-- SET THIS
   ```

3. Replace `your-organisation.splunkcloud.com` with your actual Splunk Cloud hostname.
   You can find this in your browser address bar when logged into Splunk.
   It looks like: `mycompany.splunkcloud.com`

4. Replace `paste-your-token-here` with your token (see Step 8 below)

5. Save the file (`Cmd + S`) and close TextEdit

> **Note:** You do NOT need to create or edit a `.env` file for basic use.
> The `.env` file is only needed if you want to change advanced options like
> SSL settings, timeouts, or switch between multiple Splunk hosts.

---

## 8. Get Your Splunk Token

A token is like a password that lets this tool talk to Splunk on your behalf.
You generate it inside Splunk Web.

1. Log in to your Splunk Cloud account in your web browser
2. Click on your username in the top-right corner
3. Go to **Settings** (top navigation bar) → **Tokens**
4. Click **New Token**
5. Fill in:
   - **Name:** Something descriptive, e.g. `api-client-token`
   - **Expiry:** Set a reasonable expiry (e.g. 90 days)
   - **Permissions:** Select search-only permissions if available
6. Click **Create**
7. **Copy the token now** — Splunk will only show it once
8. Paste it into your `.env` file next to `SPLUNK_TOKEN=`

> **Security tip:** Treat this token like a password. Don't share it, don't
> email it, and don't paste it into Slack or Teams messages.

---

## 9. Run Your First Search

Now let's test that everything is working.

1. Make sure your virtual environment is active (you see `(venv)` in your prompt).
   If not, navigate to the project folder and run:
   ```
   source venv/bin/activate
   ```

2. Run a simple test search:
   ```
   python main.py --query "search index=_internal | head 10"
   ```

3. You'll see output in the Terminal like:
   ```
   [2024-01-15 10:23:01] [INFO    ] Submitting search job...
   [2024-01-15 10:23:02] [INFO    ] Job submitted. SID: 1705312982.1234
   [2024-01-15 10:23:05] [INFO    ] Job status: RUNNING (45% complete)
   [2024-01-15 10:23:08] [INFO    ] Job completed successfully.
   [2024-01-15 10:23:09] [INFO    ] Total results fetched: 10
   [2024-01-15 10:23:09] [INFO    ] Results written to CSV: .../search_results/query_20240115_102309.csv

     Results saved to: /Users/yourname/Desktop/splunk_client/search_results/query_20240115_102309.csv
   ```

4. Find the CSV in the `search_results` folder inside the project directory.
   Double-click it to open in Excel or Numbers. ✓

---

## 10. Run a Search from an Excel File

You can run multiple searches automatically from an Excel file.

### Prepare your Excel file

Your Excel file needs exactly two column headers in row 1:

| rule name         | query                                          |
|-------------------|------------------------------------------------|
| Failed Logins     | search index=main sourcetype=auth failed       |
| High CPU Hosts    | search index=main sourcetype=metrics cpu>90    |
| Error Count       | search index=main log_level=ERROR \| stats count |

- The column headers must be exactly: `rule name` and `query` (lowercase is fine)
- Each row is one search
- Leave the first row as headers — don't put searches in row 1

### Run the rule file

```
python main.py --rules my_rules.xlsx
```

The tool will work through each rule one by one, printing its progress.
If one rule fails, it skips it and continues to the next.

At the end, you'll see a summary:
```
============================================================
  RULE RUNNER SUMMARY
============================================================
  Total rules : 3
  Passed      : 2
  Failed      : 1
  Skipped     : 0
============================================================
  ✓ [PASSED              ] Failed Logins
  ✗ [FAILED_VALIDATION   ] High CPU Hosts
      └─ Query contains the forbidden SPL command 'delete'
  ✓ [PASSED              ] Error Count
============================================================
```

Each passed rule creates its own CSV in `search_results/`.
A summary CSV is also saved there automatically.

---

## 11. Where to Find Your Results

All results are saved in the `search_results` folder inside the project directory.

To open it in Finder:
```
open search_results
```

Files are named automatically like:
- `Failed_Logins_20240115_102309.csv` — individual rule result
- `_summary_20240115_102315.csv` — run summary for Excel rule jobs

---

## 12. Usage Examples

### Basic search
```
python main.py --query "search index=main | head 20"
```

### Search with pipe and stats
```
python main.py --query "search index=main sourcetype=syslog | stats count by host"
```

### Run an Excel rules file
```
python main.py --rules detections.xlsx
```

### Turn on verbose output (useful for troubleshooting)
```
python main.py --query "search index=_internal | head 5" --debug
```

### Save results to a custom folder
```
python main.py --query "search index=main | head 10" --results ~/Desktop/my_results
```

---

## 13. Troubleshooting

### "command not found: python3"
Python is not installed. Go back to Step 3.

### "No module named 'requests'" or similar
Your virtual environment is not active, or dependencies weren't installed.
Run:
```
source venv/bin/activate
pip install -r requirements.txt
```

### "SPLUNK_HOST has not been set"
Open `splunk_client/settings.py` and set `SPLUNK_HOST` to your Splunk Cloud hostname. Go back to Step 7.

### "Authentication failed (HTTP 401)"
Your Splunk token is wrong, expired, or was copied incorrectly.
Go back to Step 8 to generate a new one, and update `splunk_client/settings.py`.

### "Cannot reach Splunk at..."
- Check that `SPLUNK_HOST` in your `.env` file is correct
- Check your internet connection
- Check with your team that your IP address is allowed to reach Splunk Cloud

### "Query contains the forbidden SPL command..."
Your query uses a command that is blocked for safety reasons.
Check the query in your Excel file and remove the flagged command.

### "Query does not start with a recognised SPL source command"
Your query must start with `search`, `index=`, `sourcetype=`, or a `|` pipe.
Example of a valid query: `search index=main | head 10`

### "Job did not complete within X seconds"
Your search is taking too long. Either simplify the query or add this line
to your `.env` file to give it more time:
```
SPLUNK_JOB_MAX_WAIT=300
```

### Still stuck?
Run the command again with `--debug` at the end for more detail:
```
python main.py --query "your query here" --debug
```
Share the full Terminal output with your team for help.
