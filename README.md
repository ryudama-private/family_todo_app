# family_todo_app

Django (backend) + Vue.js (frontend) を Docker Compose で動かす家族向けTodoアプリの開発用リポジトリです。

## 技術スタック

- Backend: Django 5
- Frontend: Vue 3 + Vite
- Database: PostgreSQL 16
- Container: Docker / Docker Compose

## ディレクトリ構成

- backend: Djangoアプリ
- frontend: Vueアプリ
- docker-compose.yml: 開発用コンテナ定義

### フロントエンドの主な構成

- frontend/src/pages/LoginPage.vue: ログイン画面
- frontend/src/pages/FamilyRegisterPage.vue: 家族登録画面
- frontend/src/router/index.js: 画面ルーティング
- frontend/src/pages/LoginPage.test.js: ログイン画面のVitest
- frontend/src/pages/FamilyRegisterPage.test.js: 家族登録画面のVitest
- frontend/src/router/index.test.js: ルーター設定のVitest
- frontend/e2e/family-register.spec.js: 家族登録画面のPlaywright E2E
- frontend/playwright.config.js: Playwright設定

## 起動方法

1. Docker Desktop を起動する
2. プロジェクトルートで以下を実行する

```bash
docker compose up --build
```

## 動作確認

- Backend health check: http://localhost:8000/health/
- Frontend: http://localhost:5173/

## 画面構成

- /login: ログイン画面
- /family/register: 家族登録画面
- /: /login にリダイレクト

## PostgreSQL 接続情報

- Host: localhost
- Port: 5432
- Database: family_todo
- User: family_todo_user
- Password: family_todo_password

## 停止方法

```bash
docker compose down
```

## API エンドポイント

| Method | Path            | 説明                     |
| ------ | --------------- | ------------------------ |
| POST   | /auth/register/ | 家族アカウントの新規登録 |

### POST /auth/register/

**Request Body (JSON)**

```json
{
  "name": "お母さん",
  "password": "パスワード",
  "secret_question": "好きな食べ物は？",
  "secret_answer": "カレー"
}
```

**Response 201**

```json
{
  "id": 1,
  "name": "お母さん",
  "created_at": "2026-04-14T00:00:00+09:00",
  "updated_at": "2026-04-14T00:00:00+09:00"
}
```

**Response 400（必須項目不足）**

```json
{
  "errors": {
    "name": "必須項目です。",
    "password": "必須項目です。",
    "secret_question": "必須項目です。",
    "secret_answer": "必須項目です。"
  }
}
```

## テスト

### Backendテスト

コンテナ内で実行（推奨）

```bash
docker compose exec backend sh -c "pip install -r requirements-dev.txt && pytest -v"
```

ローカルで実行（Docker起動中に限る）

```bash
cd backend
.\.venv\Scripts\Activate.ps1
$env:POSTGRES_HOST="localhost"; pytest -v
```

### Frontendテスト

Vitestで画面コンポーネントとルーターをテストできます。

一括実行:

```bash
docker compose exec frontend sh -c "npm run test"
```

ウォッチモード:

```bash
docker compose exec frontend sh -c "npm run test:watch"
```

### E2Eテスト

Playwright で家族登録画面の総合テストを実行できます。

現在の E2E は、登録成功後に作成した family レコードの id を使って cleanup を行うため、テストが追加したデータだけを終了時に自動削除します。

cleanup API は次のガードが有効です。

- 開発環境（DEBUG=True）であること
- 環境変数 `E2E_CLEANUP_ENABLED=true` で明示的に有効化されていること
- リクエストヘッダ `X-E2E-Cleanup-Token` が `E2E_CLEANUP_TOKEN` と一致すること

このリポジトリではルートの `.env` に以下を固定しているため、通常は毎回設定不要です。

- `E2E_CLEANUP_ENABLED=true`
- `E2E_CLEANUP_TOKEN=local-test-token`

Docker Compose で実行（推奨）:

```bash
docker compose up -d db backend frontend
docker compose run --rm e2e
```

ローカルのブラウザを開いて実行:

```bash
docker compose up -d db backend frontend
cd frontend
npm install
npx playwright install chromium
PW_BASE_URL=http://localhost:5173 npx playwright test --headed
```

UIモードでテストを選択して実行:

```bash
docker compose up -d db backend frontend
cd frontend
# bash / zsh の場合
PW_BASE_URL=http://localhost:5173 npx playwright test --ui
```

Windows PowerShell では書き方が異なります。

```powershell
docker compose up -d db backend frontend
cd frontend
$env:PW_BASE_URL="http://localhost:5173"
npx playwright test --ui
```

### 現在のテスト対象

- LoginPageのタイトル、入力欄、ログインボタン、家族追加リンク
- FamilyRegisterPageのタイトル、入力欄、登録ボタン
- 各フォームへの入力と送信ボタン押下
- ルーターの画面遷移設定と / から /login へのリダイレクト
- 家族登録画面で入力して登録完了メッセージが表示されるE2E
