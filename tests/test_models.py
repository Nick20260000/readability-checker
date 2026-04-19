"""Tests for data models"""

import pytest
from readability.models import ReadabilityResult, SentenceIssue, WordIssue


def test_sentence_issue():
    issue = SentenceIssue(
        original="这是一个复杂的句子，包含了许多专业术语和嵌套从句。",
        issue="句子过长，包含多个修饰成分",
        suggestion="拆分为短句会更清晰"
    )
    assert "复杂" in issue.original
    assert "拆分" in issue.suggestion


def test_word_issue():
    issue = WordIssue(
        word="模块化",
        reason="技术术语",
        alternative="把产品分成几个独立部分"
    )
    assert issue.word == "模块化"
    assert issue.alternative != issue.word


def test_readability_result():
    result = ReadabilityResult(
        score=7,
        level_label="7分：五年级学生基本能看懂",
        summary="文案整体清晰",
        complex_sentences=[
            SentenceIssue(
                original="测试句子",
                issue="问题",
                suggestion="建议"
            )
        ],
        complex_words=[],
        suggestions=["建议1", "建议2"]
    )
    assert result.score == 7
    assert len(result.complex_sentences) == 1
    assert len(result.suggestions) == 2


def test_score_validation():
    """Score should be between 1 and 10"""
    result = ReadabilityResult(
        score=10,
        level_label="满分",
        summary="完美",
        complex_sentences=[],
        complex_words=[],
        suggestions=[]
    )
    assert result.score == 10

    result.score = 1
    assert result.score == 1
