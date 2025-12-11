# 企業知識庫 RAG 系統 V1 – 系統規格書（Specification Document）

## 一、系統簡介
企業知識庫 RAG 系統旨在提供企業級的文件檢索與智能問答服務，採用 Google Gemini File Search、n8n Workflow Orchestration 與 LangChain Agent 實現。

## 二、系統架構概觀
- Web UI（Streamlit）
- Python Backend
- n8n Workflow Pipeline
- Google Gemini API
- Google FileSearchStore

## 三、功能需求（FR）
1. 文件上傳
2. 基於 File Search 的 RAG 問答
3. Store / Document 管理
4. Workflow Logging

## 四、非功能需求（NFR）
- 延遲 < 5 秒
- API Key 安全管理
- Workflow 可維護性

## 五、API Specification
### POST /upload
- multipart/form-data
### POST /chat
- body: {"question": "..."}

## 六、n8n Workflow V1 設計
- 建立 Store
- 上傳文件
- 問答
- 管理工具

## 七、資料流
User → Web UI → n8n → Gemini → File Search → 回應

## 八、版本規劃
V1、V2、V3 漸進式強化企業級能力

