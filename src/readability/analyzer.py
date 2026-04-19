"""Core analyzer - calls LLM API for readability analysis"""

import json
import re
from openai import OpenAI

from readability.models import ReadabilityResult
from readability.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from readability.config import load_api_config


class ReadabilityAnalyzer:
    """Analyzer that calls LLM to assess text readability"""

    def __init__(self):
        config = load_api_config()
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
        )
        self.model = config["model"]

    def analyze(self, text: str, max_retries: int = 2) -> ReadabilityResult:
        """
        Analyze the readability of the given text.

        Args:
            text: The Chinese text to analyze
            max_retries: Number of retries on parse failure

        Returns:
            ReadabilityResult with score, issues, and suggestions
        """
        if not text or not text.strip():
            raise ValueError("输入文案不能为空")

        user_prompt = USER_PROMPT_TEMPLATE.format(text=text.strip())

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"},
                )

                content = response.choices[0].message.content
                data = json.loads(content)
                return ReadabilityResult(**data)

            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    # Try to extract JSON from response
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        try:
                            data = json.loads(json_match.group())
                            return ReadabilityResult(**data)
                        except Exception:
                            raise ValueError(f"LLM返回格式错误: {e}\n原始内容: {content[:500]}")
                    raise ValueError(f"LLM返回不是有效JSON: {e}\n原始内容: {content[:500]}")
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"API调用失败: {e}")
