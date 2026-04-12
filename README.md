# family_todo_app

Django (backend) + Vue.js (frontend) を Docker Compose で動かす家族向けTodoアプリの開発用リポジトリです。

## 技術スタック

- Backend: Django 5
- Frontend: Vue 3 + Vite
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

## 停止方法

```bash
docker compose down
```
