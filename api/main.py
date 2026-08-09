from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from api.routes import predictions, dashboard

app = FastAPI(
    title="Churn Prediction ML API",
    description="Production-grade API with Guardrails for Customer Churn Prediction.",
    version="1.0.0"
)

# CORS Middleware for modern browser UX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(predictions.router)
app.include_router(dashboard.router)

# Mount Frontend (HTML/CSS/JS)
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Server Root - Render Dashboard UI"""
    with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return html_content

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the model training first!
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
