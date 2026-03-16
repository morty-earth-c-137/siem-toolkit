# Query Examples
### From simple one-liners to advanced multi-line detection rules

---

## How to Run a Query

### Single query from the command line

Wrap the query in quotes. For multi-line queries, use a shell here-string
or put the query in an Excel rules file (see the Excel section below).

```bash
# Simple one-liner
python main.py --query "search index=main | head 10"

# With debug output to see full job progress
python main.py --query "search index=main | head 10" --debug

# Save results to a specific folder
python main.py --query "search index=main | head 10" --results ~/Desktop/results
```

### Multi-line query from the command line (Mac/zsh)

Use `$'...'` quoting to preserve newlines in the shell:

```bash
python main.py --query $'
| tstats count
  from datamodel=Endpoint.Processes
  where Processes.process_name="cmd.exe"
  by Processes.dest Processes.user
| sort -count
'
```

### Multi-line query from an Excel rules file (recommended)

For long or complex queries, the Excel rules file is the cleanest approach.
Paste the full multi-line query into a single cell — Excel preserves newlines.

| rule name                        | query                          |
|----------------------------------|--------------------------------|
| Advanced IP Scanner Detection    | *(paste full query into cell)* |
| Failed Login Spike               | *(paste full query into cell)* |

```bash
python main.py --rules my_detections.xlsx
```

---

## Example Queries

---

### 1. Basic search with field filter

```
search index=main sourcetype=syslog severity=error | head 20
```

---

### 2. Count events by host

```
search index=main sourcetype=syslog
| stats count by host
| sort -count
```

---

### 3. Failed logins with threshold

```
search index=main sourcetype=WinEventLog EventCode=4625
| stats count by src_ip user
| where count > 10
| sort -count
```

---

### 4. Top processes by endpoint

```
search index=main sourcetype=sysmon EventCode=1
| stats count by Computer process_name
| sort -count
| head 20
```

---

### 5. tstats — fast datamodel search

```
| tstats count min(_time) as firstTime max(_time) as lastTime
  from datamodel=Endpoint.Processes
  where Processes.process_name="powershell.exe"
  by Processes.dest Processes.user Processes.process_name
| `drop_dm_object_name(Processes)`
| `security_content_ctime(firstTime)`
| `security_content_ctime(lastTime)`
```

---

### 6. Advanced multi-line detection — Advanced IP/Port Scanner Execution

This is a real-world Splunk security detection rule. Paste this directly
into a single cell in your Excel rules file.

```
| tstats `security_content_summariesonly`
  count min(_time) as firstTime
        max(_time) as lastTime

  from datamodel=Endpoint.Processes where
    Processes.process_name IN (
      "advanced_ip_scanner.exe",
      "advanced_ip_scanner_console.exe",
      "advanced_port_scanner.exe",
      "advanced_port_scanner_console.exe"
    )
    OR
    Processes.original_file_name IN (
      "advanced_ip_scanner.exe",
      "advanced_ip_scanner_console.exe",
      "advanced_port_scanner.exe",
      "advanced_port_scanner_console.exe"
    )
    OR (
      Processes.process = "* /portable *"
      Processes.process = "* /lng *"
    )

  by Processes.action Processes.dest Processes.original_file_name
     Processes.parent_process Processes.parent_process_exec
     Processes.parent_process_guid Processes.parent_process_id
     Processes.parent_process_name Processes.parent_process_path
     Processes.process Processes.process_exec Processes.process_guid
     Processes.process_hash Processes.process_id
     Processes.process_integrity_level Processes.process_name
     Processes.process_path Processes.user Processes.user_id
     Processes.vendor_product

| `drop_dm_object_name(Processes)`
| `security_content_ctime(firstTime)`
| `security_content_ctime(lastTime)`
| `advanced_ip_or_port_scanner_execution_filter`
```

---

### 7. Multi-condition network detection

```
| tstats `security_content_summariesonly`
  count min(_time) as firstTime max(_time) as lastTime
  from datamodel=Network_Traffic.All_Traffic
  where
    All_Traffic.dest_port IN (22, 23, 3389, 445, 1433, 3306)
    AND All_Traffic.action="allowed"
  by All_Traffic.src All_Traffic.dest All_Traffic.dest_port
     All_Traffic.protocol All_Traffic.action
| `drop_dm_object_name(All_Traffic)`
| `security_content_ctime(firstTime)`
| `security_content_ctime(lastTime)`
| where count > 100
| sort -count
```

---

### 8. Authentication anomaly with eval risk scoring

```
search index=main sourcetype=WinEventLog
  (EventCode=4624 OR EventCode=4625 OR EventCode=4648)
| stats
    count(eval(EventCode=4625)) as failed_logins
    count(eval(EventCode=4624)) as successful_logins
    values(src_ip) as src_ips
  by user dest
| eval risk_score = case(
    failed_logins > 50, "critical",
    failed_logins > 20, "high",
    failed_logins > 5,  "medium",
    true(),             "low"
  )
| where risk_score IN ("critical", "high")
| sort -failed_logins
```

---

### 9. Excel rules file — running multiple detections at once

Create a file called `detections.xlsx` with this structure:

| rule name                        | query                                                        |
|----------------------------------|--------------------------------------------------------------|
| Advanced IP Scanner              | `\| tstats ... \| \`drop_dm_object_name(Processes)\`` |
| Failed Login Spike               | `search index=main EventCode=4625 \| stats count by src_ip \| where count>10` |
| Suspicious PowerShell            | `search index=main process_name=powershell.exe \| stats count by dest user` |
| Lateral Movement - Network Scan  | `\| tstats count from datamodel=Network_Traffic ... \| where count>100` |

Then run all rules in one command:

```bash
python main.py --rules detections.xlsx
```

Each rule gets its own timestamped CSV. A summary is printed and saved automatically.

---

## Validator Rules — What Will Be Blocked

| Condition | Example | What happens |
|---|---|---|
| Empty query | `""` | Rejected — error shown |
| Forbidden command | `search index=main \| delete` | Rejected — error shown |
| Inline time range | `search index=main earliest=-7d` | Time range stripped, warning shown, query runs with `-30m` |
| Unbalanced bracket | `search index=main (host=web` | Rejected — position of unclosed bracket shown |
| Too short | `hi` | Rejected |
| Valid multi-line | any of the examples above | Passes — newlines and indentation preserved |
| Backtick macros | `` `security_content_summariesonly` `` | Passes — macros are not modified |

---

## Time Range Policy

All queries are hard-locked to the **past 30 minutes** regardless of what
is written in the query. If you include `earliest=` or `latest=` in your
query, they will be stripped and a warning will be printed:

```
[WARNING] Inline time modifier(s) found and removed: ['earliest', 'latest'].
          Enforced range: earliest=-30m latest=now
```

This is by design and cannot be overridden at runtime.
