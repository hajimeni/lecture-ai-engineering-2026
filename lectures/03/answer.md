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
    - `app/tools.py` に `save_learning_log` を作成
    - `requires_approval=True` をつけて `agent.tool_plain` で登録
    - CLIで保存要否を確認、yの時だけ保存する処理を追加
    - `save_learning_log` の docstring で通常の質問の時だけ使用するように修正
    - `--trace` でツール呼び出しを確認
- 結果：
    ```
    $ uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"
    [model] gemini-3.5-flash-lite
    「LoRA とQLoRAの違いは？」に対する回答を記録しますか？ [y/N]: y
    LoRAとQLoRAの主な違いは、**ベースモデルの重みの保持方法（量子化）**にあります。

    * **LoRA（Low-Rank Adaptation）**
    事前学習済みの重みを固定したまま、重みの更新分を2つの小さな低ランク行列の積として表現し、その小さな行列だけを学習するPEFT手法です。学習パラメータや保存ファイルを少なく抑えられます。
    * **QLoRA（Quantized LoRA）**
    ベースモデルの重みを4ビットなどに**量子化**してメモリ消費を大幅に節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPU環境でも学習できるようになります。

    関係する回：第2回

    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
    [tool call]   save_learning_log({'question': 'LoRA とQLoRAの違いは？', 'answer': 'LoRAは事前学習済みの重みを固定したまま、重みの更新分を小さな低ランク行列のみで学習するPEFT手法です。一方、QLoRAは、ベースモデルの重みを4ビットなどに量子化してメモリを大幅に節約した上で、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPU環境でも効率よく扱えるようになります。\n関係する回：第2回'})
    [tool return] save_learning_log -> 保存しました: /workspaces/lecture-ai-engineering-2026/learning_log/20261108_150316_2e0786e6.md…
    [usage] RunUsage(cost=Decimal('0.0007623'), details={'text_prompt_tokens': 1216}, input_text_tokens=1216, input_tokens=1216, output_tokens=159, requests=1, tool_calls=1)
    ```
    ```
    $ ls -l learning_log/
    total 4
    -rw-rw-rw- 1 vscode vscode 508 Nov  8 15:03 20261108_150316_2e0786e6.md
    ```
    ```
     $ cat learning_log/20261108_150316_2e0786e6.md
    ## 質問

    LoRA とQLoRAの違いは？

    ## 回答

    LoRAは事前学習済みの重みを固定したまま、重みの更新分を小さな低ランク行列のみで学習するPEFT手法です。一方、QLoRAは、ベースモデルの重みを4ビットなどに量子化してメモリを大幅に節約した上で、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPU環境でも効率よく扱えるようになります。
    関係する回：第2回
    ```
- 気づき・疑問：
    - Agentの動作として確認を挟んでいる仕組みをコードで理解できた。
    - docstring の説明によって、モデルがツールを使う場面を制御できることを確認した。
    - 保存ログの内容とCLIに出力された結果が違う。run_syncの再呼び出しを行いつつ、両者を一致させる為の方法を調べたがわからなかった。直接保存関数を呼び出したり、deferred_tool_resultsを使わずに終了すれば一致するが、それではただのプログラムとなってしまう。
