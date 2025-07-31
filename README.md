# DeepL CLI

[![PyPI version](https://badge.fury.io/py/deepl-cli.svg)](https://badge.fury.io/py/deepl-cli)
[![Python Version](https://img.shields.io/pypi/pyversions/deepl-cli.svg)](https://pypi.org/project/deepl-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/YOUR_USERNAME/deepl-cli/workflows/Tests/badge.svg)](https://github.com/YOUR_USERNAME/deepl-cli/actions)
[![Coverage](https://codecov.io/gh/YOUR_USERNAME/deepl-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/deepl-cli)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

高性能で使いやすい [DeepL Translator API](https://www.deepl.com/api) のコマンドラインインターフェース

## ✨ 機能

- 🌍 **多言語対応**: 30+ の言語間での高品質翻訳
- 📋 **クリップボード統合**: ワンクリックでコピー＆ペースト
- 📄 **柔軟な入出力**: ファイル、標準入力、直接テキスト入力に対応
- 🔧 **Unix パイプライン対応**: `echo "text" | deepl-cli JA` 形式をサポート
- ⚡ **高速処理**: 大量テキストの効率的な処理
- 🔐 **セキュアな設定管理**: API キーの安全な保存
- 📊 **使用量監視**: API クォータの確認と警告
- 🎯 **スマート言語検出**: ソース言語の自動判定
- 🔄 **バッチ処理**: 複数ファイルの一括翻訳
- 🛠️ **豊富な設定オプション**: カスタマイズ可能な動作設定

## 📦 インストール

### PyPI から（推奨）

```bash
# 基本インストール
pip install deepl-cli

# クリップボード機能付き
pip install deepl-cli[clipboard]

# 全機能付き（開発者向け）
pip install deepl-cli[all]
```

### ソースから

```bash
git clone https://github.com/YOUR_USERNAME/deepl-cli.git
cd deepl-cli
pip install -e .

# 開発モード（テスト・リント機能付き）
pip install -e .[dev]
```

### システム要件

- Python 3.8 以上
- インターネット接続（DeepL API アクセス用）
- DeepL API キー

## 🔑 セットアップ

### 1. DeepL API キーの取得

[DeepL Pro](https://www.deepl.com/pro-api) からAPI キーを取得してください。

### 2. API キーの設定

#### 方法 1: 設定ファイル（推奨）

```bash
# 安全な設定ファイル作成
mkdir -p ~/.token/deepl-cli
echo "YOUR_API_KEY" > ~/.token/deepl-cli/api_key
chmod 600 ~/.token/deepl-cli/api_key
```

#### 方法 2: 環境変数

```bash
# ~/.bashrc または ~/.zshrc に追加
export DEEPL_API_KEY="YOUR_API_KEY"

# 一時的な設定
export DEEPL_API_KEY="YOUR_API_KEY"
```

#### 設定ファイルの優先順位

1. `--api-key` コマンドライン引数
2. `DEEPL_API_KEY` 環境変数
3. `~/.token/deepl-cli/api_key` **（最も安全）**
4. `~/.config/deepl-cli/api_key`
5. `~/.config/.deepl_apikey`
6. `~/.deepl_apikey`

## 🚀 基本的な使用方法

### 直接テキスト翻訳

```bash
# 日本語に翻訳
deepl-cli JA "Hello, world!"

# 英語（US）に翻訳
deepl-cli EN-US "こんにちは、世界！"

# ソース言語を指定
deepl-cli EN -s JA "こんにちは"
```

### ファイル翻訳

```bash
# ファイルを翻訳（結果は標準出力）
deepl-cli JA document.txt

# ファイルから別ファイルに翻訳
deepl-cli JA input.txt -o output.txt

# 出力ディレクトリを自動作成
deepl-cli JA document.txt -o translations/document_ja.txt
```

### 標準入力（Stdin）での翻訳

#### パイプライン（自動検出）

```bash
# 最もシンプルな方法
echo "Hello, world!" | deepl-cli JA

# ファイルをパイプで送信
cat document.txt | deepl-cli JA

# 複数コマンドの連鎖
curl -s https://api.example.com/text | jq -r '.content' | deepl-cli JA
```

#### 明示的な標準入力指定

```bash
# --stdin フラグを使用（推奨）
echo "Hello, world!" | deepl-cli JA --stdin

# リダイレクトと組み合わせ
deepl-cli JA --stdin < input.txt

# 対話的入力
deepl-cli JA --stdin
# プロンプトに従ってテキストを入力し、Ctrl+D（Unix）または Ctrl+Z（Windows）で終了
```

#### Unix 慣例のダッシュ（-）

```bash
# ダッシュを使用した標準入力
echo "Hello, world!" | deepl-cli JA -

# ファイルリダイレクト
deepl-cli JA - < input.txt
```

### クリップボード操作

```bash
# クリップボードの内容を翻訳（結果も自動的にクリップボードにコピー）
deepl-cli JA --clipboard

# 標準入力から翻訳してクリップボードに保存
echo "Hello" | deepl-cli JA --stdin --clipboard

# ファイルから翻訳してクリップボードに保存
deepl-cli JA document.txt --clipboard
```

### 情報確認コマンド

```bash
# サポートされている言語の一覧
deepl-cli --list-languages

# API 使用量の確認
deepl-cli --usage

# バージョン情報
deepl-cli --version

# ヘルプの表示
deepl-cli --help
```

## 🔧 高度な使用方法

### ログファイルの分析と翻訳

```bash
# エラーログを日本語に翻訳
tail -f /var/log/application.log | grep "ERROR" | deepl-cli JA --stdin

# JSONログから特定のメッセージを翻訳
cat logs.json | jq -r '.[] | select(.level=="ERROR") | .message' | deepl-cli JA

# 複数ログファイルの処理
find /var/log -name "*.log" -exec cat {} \; | deepl-cli JA --stdin
```

### Web スクレイピングと翻訳

```bash
# ウェブページの内容を翻訳
curl -s https://example.com/article | html2text | deepl-cli JA --stdin

# GitHub の README を翻訳
curl -s https://raw.githubusercontent.com/user/repo/main/README.md | deepl-cli JA - > README_ja.md

# RSS フィードの翻訳
curl -s https://example.com/feed.xml | xmllint --xpath "//description/text()" - | deepl-cli JA -
```

### バッチ処理

#### 複数ファイルの一括翻訳

```bash
#!/bin/bash
# translate_batch.sh

TARGET_LANG="JA"
INPUT_DIR="./documents"
OUTPUT_DIR="./translated"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.txt; do
    filename=$(basename "$file")
    echo "翻訳中: $filename"
    
    cat "$file" | deepl-cli "$TARGET_LANG" --stdin \
        -o "$OUTPUT_DIR/$(basename "$filename" .txt)_${TARGET_LANG}.txt"
    
    # API制限を考慮した待機
    sleep 1
    echo "完了: $filename"
done

echo "✅ 全てのファイルの翻訳が完了しました！"
```

#### プログレス表示付きバッチ処理

```bash
#!/bin/bash
# プログレス表示付き翻訳

files=(*.txt)
total=${#files[@]}

for i in "${!files[@]}"; do
    file="${files[$i]}"
    progress=$((i + 1))
    
    echo "[$progress/$total] 処理中: $file"
    
    # 進捗バー
    completed=$((progress * 50 / total))
    remaining=$((50 - completed))
    printf "["
    printf "%*s" $completed | tr ' ' '█'
    printf "%*s" $remaining | tr ' ' '░'
    printf "] %d%%\n" $((progress * 100 / total))
    
    cat "$file" | deepl-cli JA --stdin -o "ja_$(basename "$file")" || {
        echo "❌ エラー: $file の翻訳に失敗"
        continue
    }
    
    # API制限を考慮
    sleep 1
done

echo ""
echo "🎉 バッチ翻訳完了！"
```

### 字幕ファイル（SRT）の翻訳

```bash
# 字幕ファイルの翻訳（タイムスタンプ保持）
# 注意: これは基本的な例です。実際の字幕翻訳にはより高度な処理が必要です

# SRTファイルのテキスト部分のみを抽出して翻訳
grep -v "^[0-9]*$" movie.srt | grep -v "^[0-9][0-9]:" | grep -v "^$" | \
deepl-cli JA --stdin > translated_text.txt
```

### 大きなファイルの処理

```bash
# 大きなファイルを分割して処理
split -l 100 large_document.txt part_
for part in part_*; do
    echo "処理中: $part"
    cat "$part" | deepl-cli JA --stdin > "ja_${part}"
done

# 分割ファイルを結合
cat ja_part_* > large_document_ja.txt
rm part_* ja_part_*

# 進捗表示付きで大きなファイルを処理
pv large_document.txt | deepl-cli JA --stdin -o translated_document.txt
```

## ⚙️ 設定とカスタマイズ

### 設定ファイル

`~/.config/deepl-cli/config.json` で動作をカスタマイズできます：

```json
{
  "default_target_lang": "JA",
  "default_source_lang": null,
  "preserve_formatting": true,
  "batch_max_workers": 3,
  "batch_delay_seconds": 0.5,
  "segment_size": 5000,
  "output_suffix_format": "_{lang}",
  "create_backup": false,
  "show_progress": true,
  "verbose": false,
  "retry_attempts": 3,
  "retry_delay": 1.0,
  "timeout_seconds": 30
}
```

### 言語ショートカット

`~/.config/deepl-cli/languages.json` で言語ショートカットを設定：

```json
{
  "shortcuts": {
    "en": "EN-US",
    "jp": "JA", 
    "english": "EN-US",
    "japanese": "JA",
    "german": "DE",
    "french": "FR"
  },
  "recent": ["JA", "EN-US", "DE"],
  "favorites": ["JA", "EN-US"]
}
```

### 環境変数での設定

```bash
# デフォルト設定
export DEEPL_DEFAULT_TARGET_LANG="JA"
export DEEPL_DEFAULT_SOURCE_LANG="EN"
export DEEPL_SHOW_PROGRESS="true"
export DEEPL_VERBOSE="false"
```

## 🌍 サポートされている言語

DeepL CLI は以下の言語をサポートしています：

| コード | 言語 | コード | 言語 |
|--------|------|--------|------|
| **BG** | ブルガリア語 | **NB** | ノルウェー語（ブークモール） |
| **CS** | チェコ語 | **NL** | オランダ語 |
| **DA** | デンマーク語 | **PL** | ポーランド語 |
| **DE** | ドイツ語 | **PT** | ポルトガル語 |
| **EL** | ギリシャ語 | **PT-BR** | ポルトガル語（ブラジル） |
| **EN** | 英語 | **PT-PT** | ポルトガル語（ポルトガル） |
| **EN-GB** | 英語（イギリス） | **RO** | ルーマニア語 |
| **EN-US** | 英語（アメリカ） | **RU** | ロシア語 |
| **ES** | スペイン語 | **SK** | スロバキア語 |
| **ET** | エストニア語 | **SL** | スロベニア語 |
| **FI** | フィンランド語 | **SV** | スウェーデン語 |
| **FR** | フランス語 | **TR** | トルコ語 |
| **HU** | ハンガリー語 | **UK** | ウクライナ語 |
| **ID** | インドネシア語 | **ZH** | 中国語 |
| **IT** | イタリア語 | **JA** | 日本語 |
| **KO** | 韓国語 | **LT** | リトアニア語 |
| **LV** | ラトビア語 | | |

### 言語の指定方法

```bash
# 基本的な言語コード
deepl-cli JA "Hello"      # 日本語
deepl-cli EN "こんにちは"  # 英語（自動選択）
deepl-cli DE "Hello"      # ドイツ語

# 地域指定
deepl-cli EN-US "Hello"   # アメリカ英語
deepl-cli EN-GB "Hello"   # イギリス英語
deepl-cli PT-BR "Hello"   # ブラジルポルトガル語
deepl-cli PT-PT "Hello"   # ポルトガルポルトガル語

# ソース言語の指定
deepl-cli EN -s JA "こんにちは"  # 日本語から英語
deepl-cli FR -s EN "Hello"      # 英語からフランス語
```

## 🛠️ 開発者向け情報

### プロジェクト構造

```
deepl-cli/
├── src/deepl_cli/          # メインソースコード
│   ├── __init__.py         # パッケージ初期化
│   ├── cli.py              # CLI実装
│   ├── translator.py       # DeepL API ラッパー
│   ├── clipboard.py        # クリップボード機能
│   ├── config.py           # 設定管理
│   └── utils.py            # ユーティリティ関数
├── tests/                  # テストコード
├── examples/               # 使用例
├── docs/                   # ドキュメント
└── scripts/                # スクリプト
```

### 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/deepl-cli.git
cd deepl-cli

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 開発モードでインストール
pip install -e .[dev]

# pre-commit フックをセットアップ
pre-commit install
```

### テストの実行

```bash
# 全テストの実行
pytest

# カバレッジ付きでテスト
pytest --cov

# 特定のテストファイル
pytest tests/test_cli.py

# 詳細出力
pytest -v -s
```

### コード品質チェック

```bash
# コードフォーマット
black src tests

# リント
flake8 src tests

# 型チェック
mypy src

# セキュリティチェック
bandit -r src

# 全チェックを実行
make all
```

### 利用可能な Make コマンド

```bash
make help          # ヘルプを表示
make install-dev   # 開発環境をセットアップ
make test          # テストを実行
make test-cov      # カバレッジ付きテスト
make lint          # リント実行
make format        # コードフォーマット
make type-check    # 型チェック
make security      # セキュリティチェック
make clean         # ビルドアーティファクトを削除
make build         # パッケージをビルド
make all           # 全チェックを実行
```

### Python ライブラリとしての使用

```python
from deepl_cli import DeepLTranslator, BatchTranslator, TextProcessor

# 基本的な翻訳
translator = DeepLTranslator(api_key="your_api_key")
result = translator.translate("Hello, world!", "JA")
print(result)  # こんにちは、世界！

# バッチ翻訳
batch = BatchTranslator(translator)
files = [Path("doc1.txt"), Path("doc2.txt")]
results = batch.translate_files(files, "JA", output_dir=Path("translated/"))

# テキスト処理（プレースホルダーの保護など）
processor = TextProcessor()
processed, placeholders = processor.preserve_placeholders(
    "Hello {name}, welcome to {place}!"
)
translated = translator.translate(processed, "JA")
final = processor.restore_placeholders(translated, placeholders)

# 使用量の確認
usage = translator.get_usage()
print(f"使用量: {usage['character_count']:,} / {usage['character_limit']:,}")
print(f"使用率: {usage['usage_percentage']:.1f}%")
```

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. API キーエラー

```bash
# エラー: "API key not found"
# 解決方法:
echo "YOUR_API_KEY" > ~/.token/deepl-cli/api_key
chmod 600 ~/.token/deepl-cli/api_key

# または環境変数で設定
export DEEPL_API_KEY="YOUR_API_KEY"
```

#### 2. クリップボードエラー

```bash
# エラー: "Clipboard support not available"
# 解決方法:
pip install deepl-cli[clipboard]

# Linux の場合、追加でインストールが必要な場合があります
sudo apt-get install xclip  # Ubuntu/Debian
# または
sudo yum install xclip      # RHEL/CentOS
```

#### 3. 標準入力エラー

```bash
# エラー: "No input provided"
# 原因: 入力方法が明確でない

# 悪い例:
deepl-cli JA

# 良い例:
echo "Hello" | deepl-cli JA           # パイプ
deepl-cli JA "Hello"                  # 直接テキスト
deepl-cli JA --stdin < input.txt      # リダイレクト
deepl-cli JA input.txt                # ファイル指定
```

#### 4. ファイルエンコーディングエラー

```bash
# エラー: "Unable to decode file as UTF-8"
# 解決方法: ファイルをUTF-8に変換
iconv -f SHIFT_JIS -t UTF-8 input.txt > input_utf8.txt

# エンコーディングを確認
file -i input.txt
```

#### 5. 権限エラー

```bash
# エラー: "Permission denied"
# 解決方法:
chmod 644 input.txt              # 読み取り権限
chmod 755 output_directory       # ディレクトリ権限
chmod 600 ~/.token/deepl-cli/api_key  # API キーファイル権限
```

#### 6. API クォータエラー

```bash
# エラー: "DeepL API quota exceeded"
# 解決方法:
deepl-cli --usage               # 使用量を確認
# DeepL アカウントでクォータを確認: https://www.deepl.com/account/usage

# 大きなファイルは分割して処理
split -l 100 large_file.txt part_
for part in part_*; do
    cat "$part" | deepl-cli JA --stdin > "ja_${part}"
    sleep 2  # レート制限を考慮
done
```

#### 7. ネットワークエラー

```bash
# エラー: "Failed to connect"
# 解決方法:
# 1. インターネット接続を確認
ping google.com

# 2. プロキシ設定が必要な場合
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 3. タイムアウト設定を調整
deepl-cli JA "Hello" --timeout 60
```

### デバッグモード

詳細な実行情報を確認するには `-v` オプションを使用：

```bash
deepl-cli JA "Hello" -v
```

出力例：
```
DEBUG: Read 5 characters from stdin
DEBUG: Loaded API key from ~/.token/deepl-cli/api_key
INFO: DeepL translator initialized successfully
DEBUG: Translating 5 characters to JA
INFO: Translation completed: EN → JA
こんにちは
```

### パフォーマンス最適化

#### 大量テキストの処理

```bash
# セグメント化して処理（デフォルト: 5000文字ごと）
cat large_file.txt | deepl-cli JA --stdin

# 並列処理（注意: API制限に注意）
split -l 100 input.txt part_
ls part_* | xargs -P 3 -I {} sh -c 'cat {} | deepl-cli JA --stdin > "ja_{}"'

# バッチサイズの調整
deepl-cli JA large_file.txt --segment-size 3000
```

#### API制限の最適化

```bash
# レート制限を考慮したバッチ処理
for file in *.txt; do
    cat "$file" | deepl-cli JA --stdin -o "ja_${file}"
    sleep 1  # 1秒待機
done

# 使用量を定期的にチェック
while IFS= read -r line; do
    echo "$line" | deepl-cli JA --stdin
    if (( $(deepl-cli --usage | grep -o '[0-9.]*%' | sed 's/%//') > 90 )); then
        echo "Warning: API usage is high, taking a break..."
        sleep 10
    fi
done < input.txt
```

## 🤝 貢献方法

DeepL CLI プロジェクトへの貢献を歓迎します！

### 貢献の種類

- 🐛 バグレポート
- 💡 機能提案
- 📝 ドキュメント改善
- 🔧 コード貢献
- 🧪 テスト追加
- 🌍 翻訳・国際化

### 貢献手順

1. **Issues を確認**
   - [既存の Issues](https://github.com/YOUR_USERNAME/deepl-cli/issues) を確認
   - 重複していないことを確認

2. **フォークとクローン**
   ```bash
   # GitHub でリポジトリをフォーク
   git clone https://github.com/YOUR_USERNAME/deepl-cli.git
   cd deepl-cli
   ```

3. **開発環境のセットアップ**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .[dev]
   pre-commit install
   ```

4. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   # または
   git checkout -b fix/bug-description
   ```

5. **変更の実装**
   - コードの変更
   - テストの追加
   - ドキュメントの更新

6. **テストの実行**
   ```bash
   make all  # 全チェック実行
   pytest tests/  # テスト実行
   ```

7. **コミットとプッシュ**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

8. **プルリクエストの作成**
   - GitHub でプルリクエストを作成
   - 詳細な説明を記載
   - レビューを待つ

### コーディング規約

- **Python スタイル**: [PEP 8](https://pep8.org/) に準拠
- **フォーマッター**: [Black](https://black.readthedocs.io/)
- **リンター**: [flake8](https://flake8.pycqa.org/)
- **型ヒント**: [mypy](https://mypy.readthedocs.io/) を使用
- **テスト**: [pytest](https://pytest.org/) でテストを記述

### コミットメッセージ

```bash
# 良い例
git commit -m "Add: stdin support for CLI interface"
git commit -m "Fix: clipboard error handling on Windows"
git commit -m "Update: documentation for new features"

# 悪い例
git commit -m "update"
git commit -m "fix bug"
```

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 謝辞

- [DeepL](https://www.deepl.com) - 優秀な翻訳APIの提供
- [pyperclip](https://github.com/asweigart/pyperclip) - クリップボード機能
- [Click](https://click.palletsprojects.com/) - CLI フレームワークのインスピレーション
- すべての[貢献者](https://github.com/YOUR_USERNAME/deepl-cli/contributors)

## 🔗 関連リンク

- [DeepL API ドキュメント](https://www.deepl.com/docs-api)
- [PyPI パッケージ](https://pypi.org/project/deepl-cli/)
- [GitHub リポジトリ](https://github.com/YOUR_USERNAME/deepl-cli)
- [Issue トラッカー](https://github.com/YOUR_USERNAME/deepl-cli/issues)
- [変更履歴](CHANGELOG.md)
- [貢献ガイド](CONTRIBUTING.md)

## 📈 統計情報

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/deepl-cli.svg?style=social&label=Star)](https://github.com/YOUR_USERNAME/deepl-cli)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/deepl-cli.svg?style=social&label=Fork)](https://github.com/YOUR_USERNAME/deepl-cli/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/deepl-cli.svg?style=social&label=Watch)](https://github.com/YOUR_USERNAME/deepl-cli)

## 💬 サポート

質問や問題がある場合は、以下の方法でサポートを受けられます：

1. **GitHub Issues**: [新しい Issue を作成](https://github.com/YOUR_USERNAME/deepl-cli/issues/new)
2. **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/deepl-cli/discussions)
3. **Email**: support@example.com

---

**注意**: これは DeepL SE の公式ツールではありません。DeepL API の非公式クライアントです。

⭐ このツールが役に立った場合は、GitHub でスターを付けていただけると嬉しいです！

## 📱 クイックスタート

初めてのユーザー向けの5分間クイックスタート：

```bash
# 1. インストール
pip install deepl-cli[clipboard]

# 2. API キー設定
mkdir -p ~/.token/deepl-cli
echo "YOUR_API_KEY" > ~/.token/deepl-cli/api_key

# 3. 基本的な翻訳
deepl-cli JA "Hello, world!"

# 4. ファイル翻訳
echo "Hello from file" > test.txt
deepl-cli JA test.txt

# 5. パイプライン使用
echo "Hello from pipe" | deepl-cli JA

# 6. 使用量確認
deepl-cli --usage
```

これで DeepL CLI の基本的な使用方法をマスターできます！