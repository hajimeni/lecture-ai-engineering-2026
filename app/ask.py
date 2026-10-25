"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    start = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
    )
    elapsed = time.perf_counter() - start
    
    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）
    usage = response.usage_metadata

    if usage is not None:
        print(f"[入力] {usage.prompt_token_count} tokens")
        print(f"[出力] {usage.candidates_token_count} tokens")
        print(f"[合計] {usage.total_token_count} tokens")

    print(f"[応答時間] {elapsed:.3f} 秒")
    return response.text


def chat_loop() -> None:
    """同じチャットセッションを使い、会話履歴を保つ。"""
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)
    print("[会話モード] /exit で終了します")

    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if question == "/exit":
            break
        if not question:
            continue

        try:
            response = chat.send_message(question)
            print(f"AI> {response.text or ''}\n")
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))

def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--chat", action="store_true", help="会話履歴を保って対話する")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    
    if args.chat:
        chat_loop()
    else:
        try:
            print(ask(args.question))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
