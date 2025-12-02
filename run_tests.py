"""
测试运行入口脚本
提供便捷的测试执行方式
"""
import os
import sys
import argparse
import subprocess


def run_tests(args):
    """
    运行测试
    :param args: 命令行参数
    """
    # 构建pytest命令
    cmd = ["pytest"]

    # 添加基本参数
    cmd.extend(["-v", "-s"])

    # 环境参数
    if args.env:
        cmd.append(f"--env={args.env}")

    # 标记参数
    if args.markers:
        cmd.extend(["-m", args.markers])

    # 测试路径
    if args.path:
        cmd.append(args.path)

    # 并发运行
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])

    # 失败重试
    if args.reruns:
        cmd.extend(["--reruns", str(args.reruns)])

    # 生成Allure报告
    if args.allure:
        cmd.extend([
            "--alluredir=./reports/allure-results",
            "--clean-alluredir"
        ])

    # HTML报告
    if args.html:
        cmd.extend([
            "--html=./reports/report.html",
            "--self-contained-html"
        ])

    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 80)

    # 执行测试
    result = subprocess.run(cmd)

    # 生成Allure报告
    if args.allure and result.returncode == 0:
        print("\n" + "=" * 80)
        print("生成Allure报告...")
        subprocess.run([
            "allure", "generate",
            "./reports/allure-results",
            "-o", "./reports/allure-report",
            "--clean"
        ])
        print("Allure报告生成完成: ./reports/allure-report/index.html")

        if args.serve:
            print("启动Allure服务...")
            subprocess.run(["allure", "serve", "./reports/allure-results"])

    return result.returncode


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="API自动化测试运行脚本")

    parser.add_argument(
        "--env",
        choices=["test", "staging", "prod"],
        help="运行环境"
    )

    parser.add_argument(
        "-m", "--markers",
        help="运行指定标记的用例，如: smoke, regression"
    )

    parser.add_argument(
        "-p", "--path",
        help="测试路径，如: testcases/api/test_user.py"
    )

    parser.add_argument(
        "-n", "--parallel",
        type=int,
        help="并发运行的进程数"
    )

    parser.add_argument(
        "--reruns",
        type=int,
        default=0,
        help="失败重试次数"
    )

    parser.add_argument(
        "--allure",
        action="store_true",
        help="生成Allure报告"
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="生成HTML报告"
    )

    parser.add_argument(
        "--serve",
        action="store_true",
        help="生成报告后启动Allure服务"
    )

    args = parser.parse_args()

    # 运行测试
    sys.exit(run_tests(args))


if __name__ == "__main__":
    main()
