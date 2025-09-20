"""
NASA Urban Planning API - FastAPI Backend
Simplified version for Vercel deployment
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="NASA Urban Planning API",
    description="Climate-Resilient Urban Intelligence Platform - NASA Space Apps Challenge 2025",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str

class AnalysisRequest(BaseModel):
    coordinates: List[float]
    analysis_type: str = "comprehensive"

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "NASA Urban Planning API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "environment": "vercel"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Test endpoints
@app.get("/api/test")
async def test_endpoint():
    return {
        "message": "API is working!",
        "timestamp": datetime.now().isoformat(),
        "environment": "vercel"
    }

# AI endpoints
@app.get("/api/ai/visualization-data")
async def get_visualization_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    analysis_type: str = Query("dashboard", description="Type of visualization")
):
    """Generate mock data for frontend visualizations"""
    mock_data = {
        "analysis_type": analysis_type,
        "coordinates": {"lat": lat, "lng": lng},
        "data": {
            "temperature": 25.5,
            "air_quality": "Good",
            "vegetation_index": 0.7,
            "population_density": 1500,
            "urban_heat_island": 2.3,
            "climate_risk": "Low",
            "sustainability_score": 8.2
        },
        "timestamp": datetime.now().isoformat(),
        "source": "mock_data_for_testing"
    }
    return JSONResponse(content=mock_data)

@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):
    """Mock AI chat endpoint"""
    response = {
        "response": f"Mock AI response to: {request.message}",
        "timestamp": datetime.now().isoformat(),
        "context": "This is a simplified version for Vercel deployment"
    }
    return JSONResponse(content=response)

@app.post("/api/ai/analyze-urban-data")
async def analyze_urban_data(request: AnalysisRequest):
    """Mock urban data analysis"""
    analysis_result = {
        "coordinates": request.coordinates,
        "analysis_type": request.analysis_type,
        "results": {
            "climate_risk": "Medium",
            "urban_heat_island": 2.1,
            "air_quality_index": 75,
            "vegetation_coverage": 0.6,
            "population_density": 1200,
            "recommendations": [
                "Increase green space coverage",
                "Implement cool roof technologies",
                "Improve public transportation"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }
    return JSONResponse(content=analysis_result)

# Data sources info
@app.get("/api/data-sources")
async def get_data_sources():
    """Get information about available data sources"""
    return JSONResponse(content={
        "message": "NASA Urban Planning API - Data Sources",
        "sources": [
            {
                "name": "Mock Data Source",
                "description": "This is a simplified version for Vercel deployment",
                "status": "active",
                "endpoints": [
                    "/api/ai/visualization-data",
                    "/api/ai/chat",
                    "/api/ai/analyze-urban-data"
                ]
            }
        ],
        "note": "This is a simplified version. Full functionality requires additional setup."
    })

# This is what Vercel will use
handler = app
