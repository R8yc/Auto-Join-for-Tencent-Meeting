# Auto-Join-for-Tencent-Meeting定時自動加入騰訊會議
This project provides a lightweight automation tool to schedule and auto-join Tencent Meeting (VooV Meeting) sessions without manual clicks.
<br><br>**作業系統  System**：Windows
<br>**執行環境  Environment**：Python
<br>**原理  Mechanism**：用xml模式創建Windows任務排程器（/任務計劃）來實現自動入會，不佔用資源。Uses XML mode to create Windows Task Scheduler tasks, enabling automatic meeting join with no background resource usage.
<br>**時間設定  Timing**：
<br>- 觸發時間 = 會議開始前 5 分鐘; Trigger time = 5 minutes before the meeting; 
<br>- 結束時間 = 觸發時間 + 5 分鐘; EndBoundary = trigger time + 5 minutes; 
<br>- 任務在過期 60 秒後自動刪除; Task is automatically deleted 60 seconds after expiration.


# 每次預設會議步驟  Steps for Scheduling Meetings

<br>①修改 `meetings.txt` 內的會議時間與會議號。Edit meeting times and codes in `meetings.txt`.
<br>②然後雙擊 `refresh.bat` 即可完成更新。Then double-click `refresh.bat` to refresh tasks.


# 詳細使用說明  User Guide

## 1、環境準備  Environment Setup
①下載並安裝 `Python`。Download and install `Python`. 在from `python.org`.
<br><img width="600" height="518" alt="image" src="https://github.com/user-attachments/assets/3a75e5b5-b9b3-43e4-827e-db239fe0978a" />

<br>②安裝時勾選 `Add Python to PATH`。During installation, check `Add Python to PATH`.
<br><img width="600" height="412" alt="image" src="https://github.com/user-attachments/assets/d4eca703-ccfe-4f3e-9b57-322dd722b9bf" />
<img width="600" height="412" alt="image" src="https://github.com/user-attachments/assets/d9e7248a-95c4-4464-90e8-a92dbfcf45d7" />

<br>③驗證：在 PowerShell 輸入:  Verify: in PowerShell, type: 
```powershell  
python --version
```
<br>應顯示 Python 版本。It should display the Python version.
<br><img width="600" height="716" alt="image" src="https://github.com/user-attachments/assets/d9106113-c34b-401f-8d0e-7df83045931c" />
<img width="600" height="264" alt="image" src="https://github.com/user-attachments/assets/47459eff-7c7b-4c7f-8f9a-b2a127296c1d" />

<br>④安裝 `騰訊會議 (Tencent Meeting)` 客戶端，並先手動登入一次。Install the `Tencent Meeting` application and log in manually once.
<br>測試：按 `Win + R`，輸入:  Test: press `Win + R`, then input:
```text
wemeet://page/inmeeting?meeting_code=123456789
```
<br>彈出騰訊會議，顯示`無效會議號`，代表協議已註冊成功。If Tencent Meeting launches with `invalid meeting code`, the protocol is successfully registered.
<br><img width="600" height="676" alt="image" src="https://github.com/user-attachments/assets/3ef080e9-5a26-4365-996c-3135d83e0f85" />


## 2. 部署腳本  Deploy the Script

①解壓 GitHub 下載的壓縮包,放到一個固定目錄,例如我放到python的安裝路徑下。Extract the GitHub package and place it in a fixed directory, for example under your Python installation path.
<br><br>②目前文件夾裡面共有5個文件。There are currently five files in the folder.
<br><img width="600" height="310" alt="image" src="https://github.com/user-attachments/assets/919a6c9a-c085-4549-bb81-7d077ceaa097" />
<br>③修改 `meeting.txt` 裡面的會議時間，每行一個會議：  Edit the meeting times in `meeting.txt`, one meeting per line:
```text
2025年06月30日09:00,123456789
2025年07月01日14:30,123456789
```
<br>日期時間格式必須是 `YYYY年MM月DD日HH:MM`（24 小時制），會議號用`半角逗號`分隔，冇空格。Date/time must follow `YYYY年MM月DD日HH:MM` (24-hour format), separated from the meeting code by a `comma` without `space`.


## 3. 執行腳本  Run the Script

①雙擊 `refresh.bat`，即可讀取 `meetings.txt` 並在任務排程器中自動建立任務。\simply double-click `refresh.bat` to read `meetings.txt` and automatically create tasks in Task Scheduler.
<br><br>②每次修改 `meetings.txt`，都要再次雙擊 `refresh.bat` 來刷新任務。\Each time you update `meetings.txt`, run `refresh.bat` again to refresh tasks.
<br><img width="600" height="301" alt="6dea24057531948896869f9d34b9c737" src="https://github.com/user-attachments/assets/4dd33b0b-9c89-4ceb-832d-6429e552396b" />

## 驗證效果  Verify the Result
①打開 `任務排程器/任務計劃程序 (win+R -> taskschd.msc)`。Open `Task Scheduler (win+R -> taskschd.msc)`.
<br><br>②你會在 `任務計劃程序庫`看到任務名稱類似： In `Task Scheduler Library`, You will see tasks named like:
```text
AUTO_WEMEET-932222232-2025_06_30_09_00
```
<br><img width="600" height="234" alt="f2fff8b51567418b43fc675c629fe61e" src="https://github.com/user-attachments/assets/0c337b1f-1ec8-442c-b60e-095b3dc40117" />

<br>③觸發時間 = 會議時間`前 5 分鐘`。 Trigger time = `5 minutes before` the meeting.
<br>④任務運行時會生成並運行的 `.bat`： When triggered, the task generated and runs the `.bat`:
<br>⑤打開騰訊會議  Launch Tencent Meeting
<br>⑥自動刪除 `.bat`  Auto-delete `.bat`
<br>⑦任務在運行後`5 分鐘過期`(Triggers-Edit)，過期後`1分鐘`自動從任務排程器`移除`(Settings)。The task `expires 5 minutes` after execution and is automatically `removed` from Task Scheduler `1 minute` after expiration.
