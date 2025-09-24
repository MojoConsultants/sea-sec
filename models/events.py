from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict
from datetime import datetime

class SecurityEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    page_url: HttpUrl
    https: bool
    num_links: int
    num_forms: int
    has_login_form: bool
    headers: Dict[str, str] = {}d
    note: Optional[str] = None

class TrainResult(BaseModel):
    trained_on: int
    model_path: str

class ReportSummary(BaseModel):
    total_events: int
    anomalies: int
    report_html_path: str
    report_csv_path: str
    report_json_path: str
