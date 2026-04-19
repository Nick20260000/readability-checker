"""CLI interface for readability checker"""

import sys
import click

from readability.analyzer import ReadabilityAnalyzer


def color_score(score: int) -> str:
    """Return color code for score"""
    if score >= 8:
        return "\033[92m"  # Green
    elif score >= 5:
        return "\033[93m"  # Yellow
    else:
        return "\033[91m"  # Red


def print_result(result: ReadabilityResult, use_color: bool = True):
    """Print readability result to console"""
    reset = "\033[0m" if use_color else ""
    color = color_score(result.score) if use_color else ""

    print()
    print(f"{color}{'='*60}{reset}")
    print(f"{color}📊 可读性评分: {result.score}/10{reset}")
    print(f"{color}   {result.level_label}{reset}")
    print(f"{color}{'='*60}{reset}")
    print()
    print(f"📝 {result.summary}")
    print()

    if result.complex_sentences:
        print(f"{'🔍 复杂句子:'}")
        for i, s in enumerate(result.complex_sentences, 1):
            print(f"  {i}. {s.original}")
            print(f"     问题: {s.issue}")
            print(f"     建议: {s.suggestion}")
            print()

    if result.complex_words:
        print(f"{'🔤 难词列表:'}")
        for i, w in enumerate(result.complex_words, 1):
            print(f"  {i}. {w.word}")
            print(f"     原因: {w.reason}")
            print(f"     替代: {w.alternative}")
            print()

    if result.suggestions:
        print(f"{'💡 改进建议:'}")
        for i, s in enumerate(result.suggestions, 1):
            print(f"  {i}. {s}")
        print()

    print(f"{color}{'='*60}{reset}")
    print()


@click.command()
@click.option("--text", "-t", help="要分析的文案（直接传入）")
@click.option("--file", "-f", type=click.Path(exists=True), help="从文件读取文案")
@click.option("--no-color", is_flag=True, help="不使用彩色输出")
def main(text: str, file: str, no_color: bool):
    """
    中文文案可读性测试工具

    用法示例:
      readability-cli -t "这是一段要测试的文案"
      readability-cli -f ./文案.txt
    """
    if not text and not file:
        click.echo("错误: 请提供文案内容 (--text) 或文案文件 (--file)", err=True)
        click.echo("使用 --help 查看帮助")
        sys.exit(1)

    if file:
        try:
            with open(file, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            click.echo(f"读取文件失败: {e}", err=True)
            sys.exit(1)

    try:
        click.echo("正在分析文案...")
        analyzer = ReadabilityAnalyzer()
        result = analyzer.analyze(text)
        print_result(result, use_color=not no_color)
    except Exception as e:
        click.echo(f"分析失败: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
