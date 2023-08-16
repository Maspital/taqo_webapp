## Dataset simulation_1

Summary of triggered alerts and how often they occurred, grouped by their alert source. 
Note that you can find the log files this is based on in `./replication/simulation_datasets`.

### Sigma
    
| Rule Name                                                       | # TPs  | # FPs   |
|-----------------------------------------------------------------|--------|---------|
| Alternate PowerShell Hosts                                      | 1      | 12      |
| Cleartext Protocol Usage                                        | 8      | 2       |
| Conhost Parent Process Executions                               | 3      | -       |
| Creation of an Executable by an Executable                      | 2      | 62      |
| Direct Autorun Keys Modification                                | 1      | -       |
| Encoded PowerShell Command Line Usage of ConvertTo-SecureString | -      | 3       |
| Meterpreter or Cobalt Strike Getsystem Service Installation     | 1      | -       |
| Meterpreter or Cobalt Strike Getsystem Service Start            | 1      | -       |
| Non Interactive PowerShell                                      | 1      | 15      |
| NTLMv1 Logon Between Client and Server                          | -      | 2       |
| PowerShell DownloadFile                                         | 3      | -       |
| PowerShell Web Download                                         | 3      | -       |
| Process Start From Suspicious Folder                            | 1      | -       |
| Rare Service Installations                                      | 1      | -       |
| Redirect Output in CommandLine                                  | 1      | -       |
| Reg Add RUN Key                                                 | 2      | -       |
| Scheduled Task Creation                                         | 1      | -       |
| Startup Folder File Write                                       | -      | 12      |
| Suspicious Network Command                                      | -      | 18      |
| Suspicious PowerShell Download                                  | 2      | -       |
| Verclsid.exe Runs COM Object                                    | -      | 6       |
| Windows PowerShell Web Request                                  | 1      | -       |
| Windows Suspicious Use Of Web Request in CommandLine            | 3      | -       |
| Winlogon Helper DLL                                             | -      | 3       |
| Wlrmdr Lolbin Use as Launcher                                   | -      | 1       |
| **Total**                                                       | **36** | **136** |


### Suricata

| Rule Name                                                                                | # TPs   | # FPs  |
|------------------------------------------------------------------------------------------|---------|--------|
| ET INFO EXE IsDebuggerPresent (Used in Malware Anti-Debugging)                           | 1       | -      |
| ET INFO Executable Download from dotted-quad Host                                        | 1       | -      |
| ET INFO Executable Retrieved With Minimal HTTP Headers - Potential Second Stage Download | 2       | -      |
| ET INFO SUSPICIOUS Dotted Quad Host MZ Response                                          | 2       | -      |
| ET INFO SUSPICIOUS SMTP EXE - EXE SMTP Attachment                                        | 2       | -      |
| ET INFO Windows OS Submitting USB Metadata to Microsoft                                  | -       | 4      |
| ET POLICY PE EXE or DLL Windows file download HTTP                                       | 2       | -      |
| ET SCAN Sqlmap SQL Injection Scan                                                        | 2       | -      |
| ET TROJAN Possible Metasploit Payload Common Construct Bind_API (from server)            | 2       | -      |
| ET USER_AGENTS Go HTTP Client User-Agent                                                 | -       | 20     |
| ET WEB_SERVER ATTACKER SQLi - SELECT and Schema Columns                                  | 8       | -      |
| ET WEB_SERVER Attempt To Access MSSQL xp_cmdshell Stored Procedure Via URI               | 1       | -      |
| ET WEB_SERVER MYSQL Benchmark Command in URI to Consume Server Resources                 | 2       | -      |
| ET WEB_SERVER MYSQL SELECT CONCAT SQL Injection Attempt                                  | 22      | -      |
| ET WEB_SERVER Possible Attempt to Get SQL Server Version in URI using SELECT VERSION     | 6       | -      |
| ET WEB_SERVER Possible MySQL SQLi Attempt Information Schema Access                      | 4       | -      |
| ET WEB_SERVER Possible SQL Injection Attempt SELECT FROM                                 | 16      | -      |
| ET WEB_SERVER Possible SQL Injection Attempt UNION SELECT                                | 19      | -      |
| ET WEB_SERVER Possible attempt to enumerate MS SQL Server version                        | 2       | -      |
| ET WEB_SERVER SQL Errors in HTTP 200 Response (error in your SQL syntax)                 | 36      | -      |
| ET WEB_SERVER SQL Injection Select Sleep Time Delay                                      | 7       | -      |
| ET WEB_SERVER Script tag in URI Possible Cross Site Scripting Attempt                    | 1       | -      |
| **Total**                                                                                | **138** | **24** |
