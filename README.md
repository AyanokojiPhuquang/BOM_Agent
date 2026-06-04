# Starlinks BOM Assistant

Hệ thống tạo BOM (Bill of Materials) tự động cho thiết bị viễn thông, sử dụng AI chatbot để tư vấn và tạo báo giá.

## Stack

- **Backend** — Python 3.11, FastAPI, SQLAlchemy (async), PostgreSQL, LangChain/LangGraph
- **Frontend** — React 19, Vite, TypeScript, Tailwind CSS v4
- **Database** — PostgreSQL 16
- **AI** — OpenAI-compatible LLM (OpenRouter, Azure, v.v.)
- **Deploy** — Docker Compose (dev + prod)

## Kiến trúc hệ thống

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  Frontend   │────▶│   Backend    │────▶│  PostgreSQL │
│  React/Vite │     │   FastAPI    │     │            │
│  :5173      │     │   :8030      │     │   :5437    │
└─────────────┘     └──────┬───────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LLM (OpenAI │
                    │  /OpenRouter)│
                    └──────────────┘
```

## Chức năng chính

### 1. Chat AI tư vấn sản phẩm
- Chatbot bán hàng thông minh, hỗ trợ tiếng Việt
- Tìm kiếm sản phẩm từ catalog (datasheets đã upload)
- Tư vấn module quang, switch, media converter theo yêu cầu khách

### 2. Tạo BOM tự động
- Thu thập yêu cầu qua hội thoại → tự động tạo BOM
- Lấy thông số kỹ thuật trực tiếp từ database Products
- Xuất file Excel (.xlsx) có format chuyên nghiệp
- Gửi email BOM cho đội ngũ nội bộ

### 3. Quản lý Product Catalog (tab Products)
- Data table hiển thị tất cả sản phẩm đã trích xuất
- Inline editing — click vào cell để sửa trực tiếp
- Bulk save — lưu nhiều thay đổi cùng lúc
- Tìm kiếm, phân trang
- Nút "Sync từ Excel" — đồng bộ mô tả từ dữ liệu Excel Refs

### 4. Upload & Extract PDF Datasheets (tab Datasheets)
- Upload file PDF datasheet sản phẩm
- Tự động extract text bằng pdfplumber
- AI trích xuất mã sản phẩm + thông số kỹ thuật
- Lưu vào database Products cho BOM sử dụng

### 5. Excel Reference Files (tab Excel Refs)
- Upload file Excel chứa P/N + Description chuẩn
- Hiển thị bảng — cho phép inline edit
- Dữ liệu dùng để sync/ghi đè description ở tab Products

### 6. Tra cứu Datasheet
- Khách hàng hỏi "cho tôi datasheet mã XYZ" → bot trả link download PDF
- API lookup hỗ trợ truy vấn nhiều mã cùng lúc, deduplicate

### 7. Quản lý người dùng & Prompts
- CRUD users với role-based access (admin/user)
- Chỉnh sửa system prompts cho AI agent

## Quick Start (Docker)

### Yêu cầu
- Docker + Docker Compose v2

### Khởi chạy

```bash
# 1. Clone repo
git clone <repo-url> && cd starlinks

# 2. Tạo file env
cp backend/.env.example backend/.env.docker
# Chỉnh sửa backend/.env.docker — ít nhất cần OPENAI_API_KEY

# 3. Khởi chạy
docker compose -f docker-compose.dev.yml up --build

# 4. (Lần đầu) Chạy migration
docker compose -f docker-compose.dev.yml exec backend uv run alembic upgrade head
```

### Truy cập

| Service | URL | Ghi chú |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Giao diện chính |
| Backend API | http://localhost:8030 | Swagger docs tại `/docs` |
| PostgreSQL | localhost:5437 | user/pass/db: `starlink` |

### Tài khoản mặc định

```
Email:    demo@starlink.chat
Password: password
Role:     admin
```

## Cấu hình (Environment Variables)

Tất cả config nằm trong `backend/.env.docker`. Các biến quan trọng:

| Biến | Mô tả | Mặc định |
|------|--------|----------|
| `DATABASE__URL` | PostgreSQL connection string | `postgresql+asyncpg://starlink:starlink@postgres:5432/starlink` |
| `OPENAI_API_KEY` | API key cho LLM | (bắt buộc) |
| `OPENAI_API_BASE_URL` | Base URL cho LLM API | `https://api.openai.com/v1` |
| `AUTH__JWT_SECRET_KEY` | Secret key cho JWT | `change-me-in-production` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |
| `DATASHEETS_DIR` | Thư mục lưu datasheets | `data/datasheets` |
| `SMTP__SERVER` | SMTP server cho email | |
| `SMTP__USERNAME` | SMTP username | |
| `SMTP__PASSWORD` | SMTP password | |
| `BOM_RECIPIENT_EMAIL` | Email nhận BOM | |
| `ESCALATION_EMAIL` | Email nhận escalation | |
| `LANGFUSE_*` | Langfuse tracing (optional) | |

## Luồng dữ liệu

### Upload PDF → Products

```
PDF File
  │
  ▼ pdfplumber (text extraction)
Markdown (.md)
  │
  ▼ LLM (extract product codes + specs)
Database (products table)
  │
  ├── code, brand, data_rate, fiber_type, wavelength,
  │   max_distance, connector, main_device, category
  │
  └── pdf_url (link download PDF gốc)
```

### Tạo BOM

```
Customer yêu cầu qua chat
  │
  ▼ Agent thu thập: product_code, quantity, customer_name, phone
  │
  ▼ generate_bom tool
  │
  ├── 1. Tìm product trong DB (exact match by code)
  ├── 2. Lấy structured specs từ DB (user-edited = source of truth)
  ├── 3. Gửi specs cho LLM subagent → structured BOM output
  ├── 4. Render Excel (.xlsx)
  └── 5. Gửi email + trả response
```

### Sync Excel Refs → Products

```
Upload Excel (tab Excel Refs)
  │
  ▼ Parse cột P/N + Descriptions
  │
  ▼ Lưu vào bảng excel_product_refs
  │
  ▼ Nhấn "Sync từ Excel" (tab Products)
  │
  ▼ Match P/N với product.code → ghi đè description
```

## Database Schema

### products
| Column | Type | Mô tả |
|--------|------|--------|
| id | UUID | Primary key |
| code | VARCHAR | Mã sản phẩm (indexed) |
| name | VARCHAR | Tên đầy đủ |
| brand | VARCHAR | Nhà sản xuất |
| description | TEXT | Mô tả (có thể sync từ Excel) |
| data_rate | VARCHAR | Tốc độ (1G, 10G, 100G) |
| fiber_type | VARCHAR | single-mode / multi-mode / copper / N/A |
| wavelength | VARCHAR | Bước sóng (1310nm, 850nm, N/A) |
| max_distance | VARCHAR | Khoảng cách tối đa |
| connector | VARCHAR | Đầu nối (LC, SC, RJ-45, MPO) |
| main_device | VARCHAR | Thiết bị chính tương thích |
| category | VARCHAR | Loại SP (SFP, QSFP, Switch, ...) |
| datasheet_path | VARCHAR | Đường dẫn file markdown |
| pdf_url | VARCHAR | URL download PDF gốc |
| raw_specs | TEXT | Thông số bổ sung |

### excel_files
| Column | Type | Mô tả |
|--------|------|--------|
| id | UUID | Primary key |
| filename | VARCHAR | Tên file gốc |
| file_size | INT | Dung lượng (bytes) |
| total_rows | INT | Số dòng dữ liệu |

### excel_product_refs
| Column | Type | Mô tả |
|--------|------|--------|
| id | UUID | Primary key |
| excel_file_id | UUID | FK → excel_files |
| product_code | VARCHAR | Mã sản phẩm (P/N) |
| description | TEXT | Mô tả chuẩn |

## API Endpoints

### Auth
| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/api/auth/login` | Đăng nhập |
| POST | `/api/auth/logout` | Đăng xuất |
| GET | `/api/auth/me` | Thông tin user hiện tại |

### Chat
| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/api/chat/completions` | Gửi tin nhắn + streaming response |
| POST | `/api/chat/completions/{id}/stop` | Dừng generation |

### Products
| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/api/products/` | List products (search, filter, paginate) |
| PATCH | `/api/products/{id}` | Update 1 product |
| DELETE | `/api/products/{id}` | Xóa product |
| POST | `/api/products/bulk-update` | Bulk update |
| POST | `/api/products/sync-excel` | Sync descriptions từ Excel Refs |
| POST | `/api/products/upload-excel` | Upload + parse Excel file |
| POST | `/api/products/datasheets-lookup` | Tra cứu PDF URL theo mã SP |

### Excel Files
| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/api/products/excel-files` | List file Excel đã upload |
| GET | `/api/products/excel-files/{id}` | Chi tiết file + mappings |
| PATCH | `/api/products/excel-files/{id}` | Cập nhật mappings |
| DELETE | `/api/products/excel-files/{id}` | Xóa file + mappings |

### Datasheets
| Method | Path | Mô tả |
|--------|------|--------|
| POST | `/api/datasheets/upload` | Upload folder datasheets |
| POST | `/api/datasheets/upload-pdf` | Upload PDF datasheets |
| GET | `/api/datasheets/` | List datasheets |
| DELETE | `/api/datasheets/` | Xóa tất cả |
| GET | `/api/datasheets/pdfs` | List PDF files |
| GET | `/api/datasheets/pdfs/{path}` | Download PDF |

### BOMs
| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/api/boms/` | List BOM files đã tạo |
| DELETE | `/api/boms/{filename}` | Xóa file BOM |

### Users (Admin only)
| Method | Path | Mô tả |
|--------|------|--------|
| GET | `/api/users` | List users |
| POST | `/api/users` | Tạo user |
| PUT | `/api/users/{id}` | Update user |
| DELETE | `/api/users/{id}` | Xóa user |

## Cấu trúc thư mục

```
starlinks/
├── backend/
│   ├── src/
│   │   ├── agents/          # LangGraph agent + tools
│   │   │   ├── tools/       # generate_bom, get_datasheet, escalate_to_human
│   │   │   └── ...
│   │   ├── app/             # FastAPI app
│   │   │   ├── routers/     # API endpoints
│   │   │   └── schemas/     # Request/response models
│   │   ├── db/              # Database models + repositories
│   │   ├── services/        # Business logic (pdf_converter, llms, email)
│   │   └── configs.py       # Settings from env
│   ├── configs/
│   │   └── prompts/         # AI agent prompts (editable)
│   ├── data/
│   │   ├── datasheets/      # Uploaded PDF + markdown files
│   │   └── generated_boms/  # Output Excel files
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── services/        # API client
│   │   └── components/      # Shared UI components
│   └── package.json
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── README.md
```

## Development

### Hot-reload

```bash
# Backend + Frontend tự reload khi code thay đổi
docker compose -f docker-compose.dev.yml watch
```

### Useful commands

```bash
# Logs
docker compose -f docker-compose.dev.yml logs -f backend

# Shell vào container
docker compose -f docker-compose.dev.yml exec backend bash

# Tạo migration mới
docker compose -f docker-compose.dev.yml exec backend \
  uv run alembic revision --autogenerate -m "message"

# Reset database
docker compose -f docker-compose.dev.yml down -v
```

### Production

```bash
cp backend/.env.example backend/.env.docker  # điền secrets thật
docker compose -f docker-compose.prod.yml up -d --build
```

## Ghi chú kỹ thuật

- **PDF Extraction**: Sử dụng `pdfplumber` (pdfminer engine) cho text — đọc được nhiều font type hơn PyMuPDF. PyMuPDF vẫn dùng cho image extraction.
- **BOM Source of Truth**: Khi tạo BOM, hệ thống lấy specs trực tiếp từ bảng `products` — đây là data đã qua user review/edit. Không đọc lại raw markdown.
- **Main Device**: Không tự động extract từ PDF. Mặc định = "N/A", người dùng tự chỉnh ở tab Products.
- **Excel Sync**: Chỉ sync cột `description`. Các field khác giữ nguyên từ PDF extraction hoặc user edit.
