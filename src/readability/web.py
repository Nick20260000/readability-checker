"""Streamlit web interface for readability checker"""

import streamlit as st
from readability.analyzer import ReadabilityAnalyzer


st.set_page_config(
    page_title="文案可读性测试",
    page_icon="📖",
    layout="centered",
)

st.title("📖 文案可读性测试工具")
st.markdown("输入文案，让AI帮你分析是否适合小学五年级学生理解")

text_input = st.text_area(
    "请输入要分析的文案：",
    height=200,
    placeholder="在这里粘贴或输入文案...",
)

analyze = st.button("🔍 开始分析", type="primary")

if analyze and text_input:
    if not text_input.strip():
        st.warning("请输入文案内容")
    else:
        with st.spinner("正在分析文案，请稍候..."):
            try:
                analyzer = ReadabilityAnalyzer()
                result = analyzer.analyze(text_input)

                # Score display
                score_color = "🟢" if result.score >= 8 else "🟡" if result.score >= 5 else "🔴"
                st.subheader(f"{score_color} 可读性评分: {result.score}/10")
                st.caption(result.level_label)

                # Summary
                st.markdown("### 📝 总体评价")
                st.info(result.summary)

                # Complex sentences
                if result.complex_sentences:
                    st.markdown("### 🔍 复杂句子")
                    for s in result.complex_sentences:
                        with st.expander(f"❌ {s.original[:50]}..."):
                            st.write(f"**问题**: {s.issue}")
                            st.write(f"**建议**: {s.suggestion}")

                # Complex words
                if result.complex_words:
                    st.markdown("### 🔤 难词")
                    for w in result.complex_words:
                        with st.expander(f"📖 {w.word}"):
                            st.write(f"**原因**: {w.reason}")
                            st.write(f"**简单替代**: {w.alternative}")

                # Suggestions
                if result.suggestions:
                    st.markdown("### 💡 改进建议")
                    for i, s in enumerate(result.suggestions, 1):
                        st.markdown(f"{i}. {s}")

            except Exception as e:
                st.error(f"分析失败: {e}")

elif analyze and not text_input:
    st.warning("请先输入文案内容")
