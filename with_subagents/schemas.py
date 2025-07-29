# schemas.py (in the root folder)
from pydantic import BaseModel, Field
from typing import Dict, Any

class GCPServiceAccountKey(BaseModel):
    """
    Represents the structure of a Google Cloud Service Account Key.
    """
    type: str = Field(..., alias="type")
    project_id: str = Field(..., alias="project_id")
    private_key_id: str = Field(..., alias="private_key_id")
    private_key: str = Field(..., alias="private_key")
    client_email: str = Field(..., alias="client_email")
    client_id: str = Field(..., alias="client_id")
    auth_uri: str = Field(..., alias="auth_uri")
    token_uri: str = Field(..., alias="token_uri")
    auth_provider_x509_cert_url: str = Field(..., alias="auth_provider_x509_cert_url")
    client_x509_cert_url: str = Field(..., alias="client_x509_cert_url")
    universe_domain: str = Field(..., alias="universe_domain")

    class Config:
        extra = "allow"