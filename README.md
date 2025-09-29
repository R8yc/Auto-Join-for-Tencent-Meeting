# Auto-Join-for-Tencent-Meeting定時自動加入騰訊會議
This project provides a lightweight automation tool to schedule and auto-join Tencent Meeting (VooV Meeting) sessions without manual clicks.
<br>**作業系統  System**：Windows
<br>**執行環境  Environment**：Python
<br>**原理  Mechanism**：用xml模式創建Windows任務排程器（/任務計劃）來實現自動入會，不佔用資源。Uses XML mode to create Windows Task Scheduler tasks, enabling automatic meeting join with no background resource usage.
<br>**時間設定  Timing**：
<br>觸發時間 = 會議開始前 5 分鐘; Trigger time = 5 minutes before the meeting; 
<br>結束時間 = 觸發時間 + 5 分鐘; EndBoundary = trigger time + 5 minutes; 
<br>任務在過期 60 秒後自動刪除; Task is automatically deleted 60 seconds after expiration.
# 每次預設會議步驟  Usage
<br>①修改 `meetings.txt` 內的會議時間與會議號。Edit meeting times and codes in `meetings.txt`.
<br>②然後雙擊 `refresh.bat` 即可完成更新。Then double-click refresh.bat to `refresh tasks`.
# 詳細使用說明  User Guide
## 1、環境準備  Environment Setup
①安裝 Python 3（建議 3.9+）。Install Python 3 (recommended 3.9+).
<br>②安裝時勾選 `Add Python to PATH`。During installation, check `Add Python to PATH`.
<br>③驗證：在 PowerShell 輸入:  Verify: in PowerShell, type: 
```powershell  
python --version
```
<br>應顯示 Python 版本。It should display the Python version.
<br>④安裝 `騰訊會議 (Tencent Meeting)` 客戶端，並先手動登入一次。Install the `Tencent Meeting` application and log in manually once.
<br>測試：按 `Win + R`，輸入:  Test: press `Win + R`, then input:
```text
wemeet://page/inmeeting?meeting_code=123456789
```
<br>彈出騰訊會議,顯示無效會議號，代表協議已註冊成功。/If Tencent Meeting launches with “invalid meeting code”, the protocol is successfully registered.
## 2. 部署腳本 / Deploy the Script
①解壓 GitHub 下載的壓縮包,放到一個固定目錄,例如我放到python的安裝路徑下。/Extract the GitHub package and place it in a fixed directory, for example under your Python installation path.
<br>②目前文件夾裡面共有5個文件/There are currently five files in the folder.
<br>③修改 `meeting.txt` 裡面的會議時間，每行一個會議：  Edit the meeting times in `meeting.txt`, one meeting per line:
```text
2025年06月30日09:00,123456789
2025年07月01日14:30,123456789
```
<br>日期時間格式必須是 `YYYY年MM月DD日HH:MM`（24 小時制），會議號用`半角逗號`分隔，冇空格。Date/time must follow `YYYY年MM月DD日HH:MM` (24-hour format), separated from the meeting code by a `comma` without `space`.
## 3. 執行腳本 / Run the Script
①雙擊 `refresh.bat`，即可讀取 `meetings.txt` 並在任務排程器中自動建立任務。\simply double-click `refresh.bat` to read `meetings.txt` and automatically create tasks in Task Scheduler.
<br>②每次修改 `meetings.txt`，都要再次雙擊 `refresh.bat` 來刷新任務。\Each time you update `meetings.txt`, run `refresh.bat` again to refresh tasks.
## 驗證效果 / Verify the Result
①打開 `任務排程器/任務計劃程序 (win+R -> taskschd.msc)`。Open `Task Scheduler (win+R -> taskschd.msc)`.
<br>②你會在 `任務計劃程序庫`看到任務名稱類似：\In `Task Scheduler Library`, You will see tasks named like:
```text
AUTO_WEMEET-932222232-2025_06_30_09_00
```
<br>③<br>觸發時間 = 會議時間`前 5 分鐘`。\Trigger time = `5 minutes before` the meeting.
<br>④任務運行時會生成並運行的 `.bat`：\When triggered, the task generated and runs the `.bat`:
<br>⑤打開騰訊會議\Launch Tencent Meeting
<br>⑥自動刪除 `.bat` \ Auto-delete `.bat`
<br>⑦任務在運行後`5 分鐘過期`(Triggers-Edit)，過期後`1分鐘`自動從任務排程器`移除`(Settings)。\The task `expires 5 minutes` after execution and is automatically `removed` from Task Scheduler `1 minute` after expiration.
