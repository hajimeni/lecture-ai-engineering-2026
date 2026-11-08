# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
    - app.ask(素のLLM)では[01回目のanswer.md](/lectures/01/answer.md)にある通り「基礎・応用・発展」という一般論から回答していたが、app.agentでは[用語集](/workspaces/lecture-ai-engineering-2026/data/glossary.json)の `homework-levels` の内容を参照し正確に回答していた。また、最後に「第1回」と表示され `lecture` の値が示されていることも確認できた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    - `[tool call]   search_glossary({'query': 'LoRA'})`
    - `[tool call]   search_glossary({'query': 'QLoRA'})`
- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：
    - 追加したツール: `[make_quiz]`
    - docstring
        ```
        指定した回の用語から 1つを選び、
        確認問題と答えを返す。
        「第2回の確認問題を出して」のように、
        復習用の問題を求められたときに使う。
        ```
    - 引数: `{"lecture": {"type": "integer"}}`


## 宿題

- 取り組んだレベル：実装
- やったこと：
- 結果：
- 気づき・疑問：
