"""Data models for readability analysis results"""

from pydantic import BaseModel, Field
from typing import List, Optional


class SentenceIssue(BaseModel):
    """A sentence that is too complex for 5th graders"""
    original: str = Field(description="原文")
    issue: str = Field(description="问题说明")
    suggestion: str = Field(description="改写建议")


class WordIssue(BaseModel):
    """A word/phrase that is too difficult"""
    word: str = Field(description="生词或难词")
    reason: str = Field(description="为什么难")
    alternative: str = Field(description="简单替代词")


class ReadabilityResult(BaseModel):
    """Complete readability analysis result"""
    score: int = Field(ge=1, le=10, description="可读性评分 1-10")
    level_label: str = Field(description="等级标签")
    summary: str = Field(description="总体评价")
    complex_sentences: List[SentenceIssue] = Field(default_factory=list, description="复杂句子列表")
    complex_words: List[WordIssue] = Field(default_factory=list, description="难词列表")
    suggestions: List[str] = Field(default_factory=list, description="改进建议列表")
