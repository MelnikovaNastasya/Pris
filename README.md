## RetailGenie (prototype)

RetailGenie is a small FastAPI + SQLite prototype for retail analytics. It tracks customers, products, orders, and order items, and exposes analytics endpoints for:

- **Top selling products**: `GET /analytics/popular-products`
- **Total revenue**: `GET /analytics/revenue`
- **Most active customers**: `GET /analytics/customer-stats`

### Tech stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite (`retailgenie.db` in project root)
- **Dashboard**: Simple HTML/JS page at `GET /`

### Project structure

- `main.py` – FastAPI app entrypoint
- `database.py` – SQLAlchemy `engine`, `SessionLocal`, `Base`, and `init_db` with seed data
- `models.py` – ORM models: `Customer`, `Product`, `Order`, `OrderItem`
- `schemas.py` – Pydantic schemas for API input/output
- `routes/` – Routers for customers, products, orders, analytics, and dashboard
- `templates/index.html` – Minimal dashboard UI calling analytics APIs

### Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Running the server

From the `retailgenie` directory:

```bash
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/` in your browser to view the dashboard, or use the automatic docs at `http://127.0.0.1:8000/docs`.


# Pris