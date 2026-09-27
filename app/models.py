from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    role: str
    created_at: str
    last_login: Optional[str] = None


class Employee(BaseModel):
    id: int
    employee_id: str
    name: str
    department: str
    clearance_level: str
    status: str
    email: str


class Document(BaseModel):
    id: int
    slug: str
    title: str
    classification: str
    category: str
    content: str
    created_date: str
    author: str


class SystemService(BaseModel):
    id: int
    name: str
    status: str
    version: str
    last_check: str
    owner: str


class AuditLog(BaseModel):
    id: int
    timestamp: str
    event_type: str
    source_ip: str
    details: str


class SystemStatusResponse(BaseModel):
    node_id: str
    organization: str
    status: str
    location: str
    administrator: str
    system_age: str
    uptime_counter: str
    documentation: str
    services_online: int
    total_services: int
