class Main:
    def __init__(self):
        pass

    def run(self):
        import subprocess
        import os

        def kill_python_processes():
            # 执行 PowerShell 命令获取 Python 进程信息
            powershell_cmd = 'Get-Process | Where-Object { $_.ProcessName -eq "python" } | Format-Table -Property Id, ProcessName, StartTime'
            result = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)

            # 解析输出获取 Python 进程的 PID
            lines = result.stdout.split('\n')
            for line in lines[3:-2]:  # 从第四行开始解析，忽略头尾
                parts = line.split()
                if parts:
                    pid = int(parts[0])
                    print("PID:", pid)
                    # 结束进程
                    os.system(f'Taskkill /F /PID {pid}')

        if __name__ == "__main__":
            kill_python_processes()


if __name__ == "__main__":
    main = Main()
    main.run()
