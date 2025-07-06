# 🚀 GitHub 完全初心者ガイド

## 📚 GitHubとは？

**GitHub**は、世界最大のプログラムコード保存・共有サービスです。

### 🎯 簡単に言うと
- **「プログラムのDropbox」** - コードをオンラインで安全に保存
- **「プログラマーのSNS」** - 世界中の開発者と交流
- **「無料のバックアップサービス」** - 大切なコードを失わない

### 🌟 なぜGitHubを使うのか？
1. **永続的保存**: コードが失われる心配なし
2. **どこからでもアクセス**: 家でも職場でも同じコードを使える
3. **バージョン管理**: 過去の変更履歴を全て保存
4. **共有**: 他の人とコードを共有できる
5. **無料**: 基本機能は完全無料

## 🎬 STEP 1: GitHubアカウント作成

### 1-1. GitHubサイトにアクセス
```
https://github.com
```
ブラウザでこのURLを開いてください。

### 1-2. アカウント作成
1. **「Sign up」ボタンをクリック**
2. **必要情報を入力**:
   - **Username**: あなたの好きなユーザー名（例: tennis-analyzer-dev）
   - **Email**: あなたのメールアドレス
   - **Password**: 強力なパスワード

### 1-3. プラン選択
- **「Free」プラン**を選択（無料で十分です）
- パブリックリポジトリ（誰でも見れる）は無制限
- プライベートリポジトリ（自分だけ）も無制限

### 1-4. メール認証
- 登録したメールアドレスに認証メールが届きます
- メール内のリンクをクリックして認証完了

## 🏗️ STEP 2: 新しいリポジトリ作成

### 2-1. リポジトリ作成開始
1. GitHubにログイン
2. 右上の **「+」ボタン** をクリック
3. **「New repository」** を選択

### 2-2. リポジトリ設定
```
Repository name: tennis-serve-analyzer
Description: AI-powered tennis serve motion analysis system
```

### 2-3. 設定オプション
- ✅ **Public**: 誰でも見ることができる（推奨）
- ❌ **Private**: 自分だけが見ることができる
- ❌ **Add a README file**: チェックしない（既にあるため）
- ❌ **Add .gitignore**: チェックしない（既にあるため）
- ❌ **Choose a license**: 今は選択しない

### 2-4. 作成完了
**「Create repository」ボタンをクリック**

## 🔗 STEP 3: ローカルリポジトリとGitHubを接続

### 3-1. GitHubリポジトリのURL取得
作成されたリポジトリページで：
1. **緑色の「Code」ボタン**をクリック
2. **「HTTPS」タブ**を選択
3. **URLをコピー**（例: https://github.com/username/tennis-serve-analyzer.git）

### 3-2. Manusサンドボックスでの接続設定
```bash
# リモートリポジトリを追加
git remote add origin https://github.com/あなたのユーザー名/tennis-serve-analyzer.git

# 接続確認
git remote -v
```

### 3-3. 初回プッシュ（アップロード）
```bash
# メインブランチをプッシュ
git push -u origin master

# タグもプッシュ
git push origin v1.0.0
```

## 🎯 STEP 4: 認証設定

### 4-1. Personal Access Token作成
GitHubでパスワード認証は廃止されているため、トークンが必要です。

1. **GitHubの右上のプロフィール画像**をクリック
2. **「Settings」**を選択
3. 左メニューの**「Developer settings」**をクリック
4. **「Personal access tokens」** → **「Tokens (classic)」**
5. **「Generate new token」** → **「Generate new token (classic)」**

### 4-2. トークン設定
```
Note: Tennis Analyzer Development
Expiration: 90 days（または好きな期間）
Scopes: 
✅ repo（リポジトリへの完全アクセス）
```

### 4-3. トークンの使用
- **生成されたトークンをコピー**（一度しか表示されません！）
- **パスワードの代わりに使用**

## 📱 STEP 5: GitHubの基本的な使い方

### 5-1. リポジトリページの見方
```
📁 Code タブ: ファイル一覧とコード表示
📊 Issues タブ: バグ報告や要望管理
🔀 Pull requests タブ: コード変更の提案
⚙️ Settings タブ: リポジトリ設定
```

### 5-2. ファイルの確認
- **ファイル名をクリック**: ファイル内容を表示
- **履歴確認**: 「History」ボタンで変更履歴
- **ダウンロード**: 「Download」でファイル取得

### 5-3. リリース管理
1. **「Releases」**をクリック
2. **「Create a new release」**
3. **タグ選択**: v1.0.0を選択
4. **リリースノート**を記入
5. **「Publish release」**

## 🔄 STEP 6: 日常的な使い方

### 6-1. 新しい変更をプッシュ
```bash
# ローカルで変更作業
# ファイルを編集...

# 変更をコミット
git add .
git commit -m "✨ 新機能: リアルタイム解析を追加"

# GitHubにプッシュ
git push origin master

# 新バージョンのタグ
git tag -a v1.1.0 -m "v1.1.0: リアルタイム解析機能"
git push origin v1.1.0
```

### 6-2. GitHubでの確認
1. **リポジトリページを更新**
2. **新しいコミットが表示される**
3. **ファイルの変更内容を確認**

## 🛡️ STEP 7: セキュリティとベストプラクティス

### 7-1. 注意事項
- ❌ **APIキーを公開しない**: .envファイルは.gitignoreに追加
- ❌ **パスワードを含めない**: 設定ファイルに注意
- ❌ **大きなファイルを避ける**: 動画ファイルなどは除外

### 7-2. プライベート情報の管理
```bash
# .envファイルの例
OPENAI_API_KEY=your_secret_key_here
DATABASE_PASSWORD=your_password_here
```

## 📋 STEP 8: 便利な機能

### 8-1. README.mdの活用
- **プロジェクトの説明**
- **インストール方法**
- **使用方法**
- **ライセンス情報**

### 8-2. Issues（課題管理）
- **バグ報告**
- **新機能の要望**
- **TODO管理**

### 8-3. Wiki（ドキュメント）
- **詳細な説明書**
- **API仕様書**
- **開発ガイド**

## 🎯 実際の手順（テニス解析システム用）

### 今すぐやること
1. **GitHub.comにアクセス**
2. **アカウント作成**（5分）
3. **新リポジトリ作成**（2分）
   - 名前: `tennis-serve-analyzer`
   - 説明: `AI-powered tennis serve motion analysis system`
4. **Personal Access Token作成**（3分）
5. **Manusサンドボックスで接続**（2分）

### コマンド例
```bash
# リモート追加
git remote add origin https://github.com/あなたのユーザー名/tennis-serve-analyzer.git

# プッシュ
git push -u origin master
git push origin v1.0.0
```

## 🆘 トラブルシューティング

### よくあるエラー
1. **認証エラー**: Personal Access Tokenを使用
2. **プッシュエラー**: git pullで最新を取得
3. **ファイルサイズエラー**: .gitignoreで大きなファイルを除外

### 解決方法
```bash
# 認証情報をクリア
git config --global --unset user.password

# 強制プッシュ（注意して使用）
git push --force origin master
```

## 🎉 完了後の確認

### GitHubで確認すべきこと
- ✅ 全ファイルがアップロードされている
- ✅ README.mdが正しく表示されている
- ✅ v1.0.0タグが作成されている
- ✅ コミット履歴が表示されている

**🎾 これでテニス解析システムが世界中からアクセス可能になります！**

