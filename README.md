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

## 起動方法

1. Docker Desktop を起動する
2. プロジェクトルートで以下を実行する

```bash
docker compose up --build
```

## 動作確認

- Backend health check: http://localhost:8000/health/
- Frontend: http://localhost:5173/

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

| Method | Path           | 説明                     |
| ------ | -------------- | ------------------------ |
| POST   | /auth/register | 家族アカウントの新規登録 |

### POST /auth/register

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

コンテナ内で実行（推奨）

```bash
docker compose exec backend pytest -v
```

ローカルで実行（Docker起動中に限る）

```bash
cd backend
.\.venv\Scripts\Activate.ps1
$env:POSTGRES_HOST="localhost"; pytest -v
```
