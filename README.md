## 本番環境APIエンドポイント

### 本番環境APIエンドポイントの扱い

- フロントエンド（Vue/Vite）からバックエンド（Django）APIへのリクエストは、`import.meta.env.VITE_API_BASE_URL` でAPIのベースURLを切り替えています。
- 本番環境では `.env.production` で `VITE_API_BASE_URL` を本番バックエンドのURLに設定してください。
- 開発環境では `http://localhost:8000` などローカルAPIサーバーのURLを指定します。

---

## Azure App Service でのポート設定について

Azure App Service では外部公開ポートは 80 のみです。

**frontend（Vite）は `80:5173` のように、コンテナの 5173 番ポートを 80 にマッピングして公開するのが推奨です。**

backend（Django）は外部公開不要なら `8000` のままでOKです（frontend からのみアクセス）。

docker-compose.prod.yml の例:

```
services:
  frontend:
    image: familytodocontainer.azurecr.io/frontend:latest
    ports:
      - "80:5173"
  backend:
    image: familytodocontainer.azurecr.io/backend:latest
    ports:
      - "8000:8000"
```

この設定をしておくことで、Azure App Service での公開時にポートの問題でハマることを防げます。

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
- frontend/src/pages/TodoPage.vue: Todoメイン画面
- frontend/src/router/index.js: 画面ルーティング
- frontend/src/pages/LoginPage.test.js: ログイン画面のVitest
- frontend/src/pages/FamilyRegisterPage.test.js: 家族登録画面のVitest
- frontend/src/pages/TodoPage.test.js: Todo画面のVitest
- frontend/src/router/index.test.js: ルーター設定のVitest
- frontend/e2e/family-register.spec.js: 家族登録画面のPlaywright E2E
- frontend/e2e/login.spec.js: ログイン画面のPlaywright E2E
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
- /todo: Todoメイン画面
- /family/register: 家族登録画面
- /: /login にリダイレクト

### Todo画面のレイアウト

- 左サイドバー: ログイン中ユーザー表示、TODO一覧、カレンダー、ログアウト
- 右コンテンツ領域: 今後Todo一覧やカレンダー本体を表示する領域
- レイアウト方式: `grid-template-columns: 170px 1fr` による2カラム構成

### 現在のログアウト仕様

- サーバーセッションやトークンは未使用
- ログイン成功時に `localStorage` へ `loggedInFamilyName` を保存
- ログアウト時に `loggedInFamilyName` を削除し `/login` へ遷移

## DBの中身を確認する方法

### familyテーブルの中身を確認する

```bash
docker compose exec backend python manage.py dbshell
```

### テーブル一覧を確認する

```sql
\dt
```

または

```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

終了は `\q` です。

---

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

| Method | Path                          | 説明                     |
| ------ | ----------------------------- | ------------------------ |
| POST   | /auth/register/               | 家族アカウントの新規登録 |
| POST   | /auth/login/                  | ログイン                 |
| POST   | /auth/todos/                  | タスク新規登録           |
| PATCH  | /auth/todos/{id}/title/       | タスクのタイトル変更     |
| PATCH  | /auth/todos/{id}/assignee_id/ | タスクの担当者変更       |
| PATCH  | /auth/todos/{id}/due_date/    | タスクの期限変更         |
| PATCH  | /auth/todos/{id}/status/      | タスクの進行状況変更     |

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
  "name": "お母さん"
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

### POST /auth/login/

**Request Body (JSON)**

```json
{
  "name": "お母さん",
  "password": "パスワード"
}
```

**Response 200**

```json
{
  "id": 1,
  "name": "お母さん"
}
```

**Response 401（認証失敗）**

```json
{
  "error": "名前またはパスワードが違います。"
}
```

**Response 400（必須項目不足）**

```json
{
  "errors": {
    "name": "必須項目です。",
    "password": "必須項目です。"
  }
}
```

### 新規タスク登録API

#### エンドポイント

- POST `/auth/todos/`

#### 概要

新しいタスク（やること）を登録します。全項目必須です。

#### リクエスト例

```
POST /auth/todos/
Content-Type: application/json

{
  "title": "テストタスク",
  "creator_id": 1,
  "assignee_id": 2,
  "due_date": "2026-12-31T00:00:00",
  "status": "未対応"
}
```

- `title` : タスク名（文字列, 必須）
- `creator_id` : 作成者のfamily.id（整数, 必須）
- `assignee_id` : 担当者のfamily.id（整数, 必須）
- `due_date` : 期限（ISO8601形式の日時文字列, 必須）
- `status` : 進行状況（例: "未対応"、"完了" など, 必須)

#### レスポンス例（201 Created）

```
{
  "id": 1,
  "title": "テストタスク",
  "creator_id": 1,
  "assignee_id": 2,
  "due_date": "2026-12-31T00:00:00",
  "status": "未対応",
  "alarm_minutes": null
}
```

#### エラー例

- 必須項目不足

```
{
  "error": "titleは必須です"
}
```

- family_idが不正

```
{
  "error": "creator_idまたはassignee_idが不正です"
}
```

- due_dateの形式が不正

```
{
  "error": "due_dateの形式が不正です"
}
```

### タイトル変更API

#### エンドポイント

- PATCH `/auth/todos/{id}/title/`

#### 概要

指定したタスクのタイトルを変更します。

#### リクエスト例

```
PATCH /auth/todos/1/title/
Content-Type: application/json

{
  "title": "新しいタイトル"
}
```

- `title` : 新しいタイトル（文字列, 必須, 空文字不可）

#### レスポンス例（200 OK）

```json
{
  "title": "新しいタイトル"
}
```

#### エラー例

- titleが空または未指定

```json
{
  "error": "titleは必須です"
}
```

- 指定したIDのタスクが存在しない

```json
{
  "error": "指定されたタスクが存在しません"
}
```

### 担当者変更API

#### エンドポイント

- PATCH `/auth/todos/{id}/assignee_id/`

#### 概要

指定したタスクの担当者を変更します。

#### リクエスト例

```
PATCH /auth/todos/1/assignee_id/
Content-Type: application/json

{
  "assignee_id": 3
}
```

- `assignee_id` : 新しい担当者のfamily.id（整数, 必須）

#### レスポンス例（200 OK）

```json
{
  "assignee_id": 3
}
```

#### エラー例

- assignee_idが未指定

```json
{
  "error": "assignee_idは必須です"
}
```

- 指定したassignee_idのfamilyが存在しない

```json
{
  "error": "指定された担当者が存在しません"
}
```

- 指定したIDのタスクが存在しない

```json
{
  "error": "指定されたタスクが存在しません"
}
```

### 進行状況変更API

#### エンドポイント

- PATCH `/auth/todos/{id}/status/`

#### 概要

指定したタスクの進行状況を変更します。

#### リクエスト例

```
PATCH /auth/todos/1/status/
Content-Type: application/json

{
  "status": "進行中"
}
```

- `status` : 新しい進行状況（文字列, 必須, 空文字不可）

#### レスポンス例（200 OK）

```json
{
  "status": "進行中"
}
```

#### エラー例

- statusが空または未指定

```json
{
  "error": "statusは必須です"
}
```

- 指定したIDのタスクが存在しない

```json
{
  "error": "指定されたタスクが存在しません"
}
```

### 期限変更API

#### エンドポイント

- PATCH `/auth/todos/{id}/due_date/`

#### 概要

指定したタスクの期限を変更します。

#### リクエスト例

```
PATCH /auth/todos/1/due_date/
Content-Type: application/json

{
  "due_date": "2027-01-15T09:30:00Z"
}
```

- `due_date` : 新しい期限（ISO8601形式の日時文字列, 必須, 空文字不可）

#### レスポンス例（200 OK）

```json
{
  "due_date": "2027-01-15T09:30:00Z"
}
```

#### エラー例

- due_dateが空または未指定

```json
{
  "error": "due_dateは必須です"
}
```

- due_dateの形式が不正

```json
{
  "error": "due_dateの形式が不正です"
}
```

- 指定したIDのタスクが存在しない

```json
{
  "error": "指定されたタスクが存在しません"
}
```

---

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

Playwright で家族登録画面とログイン画面の総合テストを実行できます。

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

ローカルのブラウザを開いてE2Eテストを実行:

- bash/zsh（Mac/WSL等）

  ```bash
  docker compose up -d db backend frontend
  cd frontend
  npm install
  npx playwright install chromium
  PW_BASE_URL=http://localhost:5173 npx playwright test --headed
  # UIモード
  PW_BASE_URL=http://localhost:5173 npx playwright test --ui
  ```

- Windows PowerShell
  ```powershell
  docker compose up -d db backend frontend
  cd frontend
  npm install
  npx playwright install chromium
  $env:PW_BASE_URL="http://localhost:5173"
  npx playwright test --headed
  # UIモード
  npx playwright test --ui
  ```

### 現在のテスト対象

- LoginPageのタイトル、入力欄、ログインボタン、家族追加リンク
- FamilyRegisterPageのタイトル、入力欄、登録ボタン
- TodoPageのサイドバー表示、メニュー表示、ログアウトボタン表示
- 各フォームへの入力と送信ボタン押下
- ルーターの画面遷移設定（/login, /todo, /family/register）と / から /login へのリダイレクト
- 家族登録画面で入力して登録完了メッセージが表示されるE2E
- 正しい認証情報でログイン後に /todo へ遷移するE2E
- 誤ったパスワードでログイン失敗メッセージが表示されるE2E
- ログイン後に Todo画面でログイン中ユーザー名が表示されるE2E
- Todo画面でログアウトすると /login に戻り、保持していた name が削除されるE2E
- タスク新規登録APIのテスト（正常系・バリデーション・エラー系）
- タスクタイトル変更APIのテスト（正常系・空文字エラー・存在しないIDの404）
- タスク担当者変更APIのテスト（正常系・キーなしエラー・存在しないassignee_idエラー・存在しないタスクIDの404）
- タスク期限変更APIのテスト（正常系・空文字エラー・キーなしエラー・形式不正エラー・存在しないタスクIDの404）
- タスク進行状況変更APIのテスト（正常系・空文字エラー・キーなしエラー・存在しないタスクIDの404）
