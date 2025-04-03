import subprocess
import os
from datetime import datetime


def run_tests():
    # 创建 reports 目录
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.html"

    # 运行 pytest 命令
    cmd = f"pytest tests/ -v --html={report_path} --self-contained-html"
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print(f"✅ 测试全部通过！报告位置: {report_path}")
    else:
        print(f"❗️ 测试有失败！请查看报告: {report_path}")

if __name__ == "__main__":
    run_tests()
