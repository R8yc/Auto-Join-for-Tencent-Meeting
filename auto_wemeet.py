# -*- coding: utf-8 -*-
"""
Author: Ray Chen.

功能说明 / Description:
①从 meetings.txt 读取会议信息；
②为每个会议生成对应的 join_wemeet_{code}_{YYYYMMDD_HHMM}.bat；
③使用 XML 模式 调用 schtasks /Create 创建一次性计划任务；
④触发时间 = 会议时间 前 5 分钟；
⑤过期时间EndBoundary = 触发时间 + 5 分钟，任务 过期 60 秒后自动删除；
⑥.bat 文件在执行后会自动删除。

meetings.txt 每行格式（多行、多会议）： 
YYYY年MM月DD日HH:MM,会议号 
例： 
2025年06月30日09:00,123456789
2025年07月01日14:30,123456789
"""

import os
import re
import sys
import subprocess
from datetime import datetime, timedelta

# === 可调参数 ===
TASK_PREFIX = "AUTO_WEMEET"
AHEAD_MINUTES = 5          # 提前 N 分钟触发
DELETE_AFTER = "PT60S"     # 过期后自动删除时间（ISO8601 duration）
ENCODINGS_TRY = ("utf-8", "gb18030", "gbk")

# === 正则：YYYY年MM月DD日HH:MM,会议号 ===
LINE_RE = re.compile(
    r"^\s*(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}):(\d{2})\s*,\s*(\d{6,})\s*$"
)

def xml_escape(s: str) -> str:
    """最少量 XML 转义，保证路径/命令安全写入 XML。"""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))

def read_meetings(txt_path):
    raw = None
    for enc in ENCODINGS_TRY:
        try:
            with open(txt_path, "r", encoding=enc) as f:
                raw = f.read()
            break
        except Exception:
            continue
    if raw is None:
        raise RuntimeError(f"无法读取 Unable to read: {txt_path}（UTF-8/GBK/GB18030）")

    meetings = []
    for idx, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        m = LINE_RE.match(line)
        if not m:
            print(f"[WARN] 第 {idx} 行格式错误 Skipped (line {idx} format error)：{line}")
            continue
        y, mo, d, hh, mm, code = m.groups()
        try:
            mtime = datetime(int(y), int(mo), int(d), int(hh), int(mm), 0)
        except ValueError:
            print(f"[WARN] 第 {idx} 行日期非法 Skipped (line {idx} invalid date)：{line}")
            continue
        meetings.append((mtime, code))
    return meetings

def fmt_task_name(code, mtime):
    stamp = mtime.strftime("%Y_%m_%d_%H_%M")
    return f"{TASK_PREFIX}-{code}-{stamp}"

def fmt_bat_name(code, mtime):
    stamp = mtime.strftime("%Y%m%d_%H%M")
    return f"join_wemeet_{code}_{stamp}.bat"

def ensure_bat(bat_path, meeting_code):
    # 用 start 交给 URL 处理程序（Explorer）；两个引号 "" 是窗口标题占位不可省
    content = (
        f'start "" "wemeet://page/inmeeting?meeting_code={meeting_code}"\r\n'
        'del "%~f0"\r\n'
    )
    with open(bat_path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(content)

def run_cmd(cmd_list):
    p = subprocess.Popen(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    out, err = p.communicate()
    try:
        out = out.decode("utf-8", errors="ignore")
        err = err.decode("utf-8", errors="ignore")
    except Exception:
        pass
    return p.returncode, out, err

def delete_task_if_exists(task_name):
    # 存在就删；不存在忽略错误
    run_cmd(["schtasks", "/Delete", "/TN", task_name, "/F"])

def create_task_xml(task_name, bat_full, trig_time, working_dir):
    """
    生成任务 XML 并用 /XML 创建：
      - StartBoundary = trig_time
      - EndBoundary   = trig_time + 5 分钟
      - DeleteExpiredTaskAfter = PT60S
      - HighestAvailable + InteractiveToken（仅当用户登录时运行）
    """
    start_boundary = trig_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_boundary   = (trig_time + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")

    # XML 里对路径与命令做转义
    cmd_esc   = xml_escape(bat_full)
    work_esc  = xml_escape(working_dir)

    xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>auto_wemeet</Author>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <EndBoundary>{end_boundary}</EndBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <DeleteExpiredTaskAfter>{DELETE_AFTER}</DeleteExpiredTaskAfter>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd_esc}</Command>
      <WorkingDirectory>{work_esc}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""

    xml_path = bat_full + ".xml"
    # 任务计划程序 XML 需要 UTF-16
    with open(xml_path, "w", encoding="utf-16") as f:
        f.write(xml_content)

    rc, out, err = run_cmd([
        "schtasks", "/Create", "/TN", task_name, "/XML", xml_path, "/F"
    ])
    try:
        os.remove(xml_path)
    except Exception:
        pass
    return rc, out, err

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    txt_path = os.path.join(base_dir, "meetings.txt")
    if not os.path.exists(txt_path):
        print(f"[ERROR] 未找到 Not found: {txt_path}")
        sys.exit(1)

    print("[INFO] 读取会议清单 Reading meeting list…")
    meetings = read_meetings(txt_path)
    if not meetings:
        print("[WARN] 没有有效条目 No valid entries.")
        sys.exit(0)

    now = datetime.now()
    created = skipped = errors = 0

    for mtime, code in meetings:
        trig = mtime - timedelta(minutes=AHEAD_MINUTES)
        if trig <= now:
            print(f"[SKIP] 会议({code}) {mtime} 已过或不足 {AHEAD_MINUTES} 分钟 Skipped: expired or too close")
            skipped += 1
            continue

        task_name = fmt_task_name(code, mtime)
        bat_name  = fmt_bat_name(code, mtime)
        bat_full  = os.path.join(base_dir, bat_name)

        ensure_bat(bat_full, code)
        delete_task_if_exists(task_name)

        rc, out, err = create_task_xml(task_name, bat_full, trig, base_dir)
        if rc == 0:
            print(f"[OK] 已创建任务 Created task：{task_name} → {trig.strftime('%Y-%m-%d %H:%M')}")
            created += 1
        else:
            print(f"[ERR] 创建任务失败 Failed to create task：{task_name}")
            print(out.strip() or err.strip())
            errors += 1

    print("\n—— 汇总 Summary ——")
    print(f"创建 Created：{created}  跳过 Skipped：{skipped}  错误 Errors：{errors}")

if __name__ == "__main__":
    main()
