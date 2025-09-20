"""
NASA Urban Planning Tool - FastAPI Backend
Climate-Resilient Urban Intelligence Platform
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our services
from services.nasa_service import NASAService
from services.gemini_service import GeminiService
from services.official_nasa_service import OfficialNASAService
from services.landsat_service import LandsatService
from services.worldpop_service import WorldPopService
from services.copernicus_service import CopernicusService
from services.nasa_library_service import NASALibraryService
from services.ai_analysis_service import AIAnalysisService

# Initialize FastAPI app
app = FastAPI(
    title="NASA Urban Planning API",
    description="Climate-Resilient Urban Intelligence Platform - NASA Space Apps Challenge 2025",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://space-apps-2025-urban-planner.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
nasa_service = NASAService()  # Basic NASA service
official_nasa_service = OfficialNASAService()  # Official NASA Space Apps resources
gemini_service = GeminiService()
landsat_service = LandsatService()  # Landsat STAC API service
worldpop_service = WorldPopService()  # WorldPop API service
copernicus_service = CopernicusService()  # EU Copernicus service
nasa_library_service = NASALibraryService()  # NASA Image Library service
ai_analysis_service = AIAnalysisService()  # AI analysis service

# Pydantic models for request/response
class CoordinateRequest(BaseModel):
    latitude: float
    longitude: float
    radius: Optional[float] = 1000  # meters

class AreaRequest(BaseModel):
    coordinates: List[List[float]]  # Polygon coordinates
    name: Optional[str] = "Custom Area"

class AnalysisRequest(BaseModel):
    coordinates: List[float]  # [lat, lng]
    analysis_type: str = "comprehensive"
    query: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "NASA Urban Planning API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# NASA Data Endpoints
@app.get("/api/nasa/temperature")
async def get_temperature_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get MODIS Land Surface Temperature data for coordinates"""
    try:
        data = await nasa_service.get_temperature_data(lat, lng, date)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/air-quality")
async def get_air_quality_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get Aura OMI air quality data for coordinates"""
    try:
        data = await nasa_service.get_air_quality_data(lat, lng, date)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/vegetation")
async def get_vegetation_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get Landsat NDVI vegetation data for coordinates"""
    try:
        data = await nasa_service.get_vegetation_data(lat, lng, date)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/precipitation")
async def get_precipitation_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get GPM precipitation data for coordinates"""
    try:
        data = await nasa_service.get_precipitation_data(lat, lng, date)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Comprehensive Analysis Endpoint
@app.post("/api/analyze")
async def analyze_climate_data(request: AnalysisRequest):
    """Comprehensive climate analysis for coordinates"""
    try:
        # Get all NASA data
        nasa_data = await nasa_service.get_comprehensive_data(
            request.coordinates[0], 
            request.coordinates[1]
        )
        
        # Get Gemini insights if query provided
        gemini_insights = None
        if request.query:
            gemini_insights = await gemini_service.analyze_with_context(
                request.query, nasa_data, {}, []
            )
        
        return JSONResponse(content={
            "coordinates": request.coordinates,
            "nasa_data": nasa_data,
            "gemini_insights": gemini_insights,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Gemini AI Chat
@app.post("/api/chat")
async def chat_with_gemini(request: ChatRequest):
    """Chat with Gemini AI about climate data"""
    try:
        response = await gemini_service.chat(request.message, request.context)
        return JSONResponse(content={
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Official NASA Space Apps Challenge 2025 Endpoints
@app.get("/api/official/earthdata-worldview")
async def get_earthdata_worldview_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    layer: str = Query("MODIS_Terra_Land_Surface_Temperature_Day", description="Data layer"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get data from NASA Earthdata Worldview - Primary satellite data visualization platform"""
    try:
        data = await official_nasa_service.get_earthdata_worldview_data(lat, lng, layer, date)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/sedac-demographic")
async def get_sedac_demographic_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    dataset: str = Query("gpw-v4-population-density", description="SEDAC dataset")
):
    """Get demographic and equity data from NASA SEDAC - Social and environmental dynamics (UN SDGs)"""
    try:
        data = await official_nasa_service.get_sedac_demographic_data(lat, lng, dataset)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/ghsl-urban")
async def get_ghsl_urban_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    dataset: str = Query("built-up-area", description="GHSL dataset")
):
    """Get urban settlement data from EU Copernicus GHSL - Global population and urban density"""
    try:
        data = await official_nasa_service.get_ghsl_urban_data(lat, lng, dataset)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/worldpop")
async def get_worldpop_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    year: int = Query(2020, description="Year for population data")
):
    """Get population data from WorldPop - Open source population data for urban change analysis"""
    try:
        data = await official_nasa_service.get_worldpop_data(lat, lng, year)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/copernicus-climate")
async def get_copernicus_climate_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    dataset: str = Query("land-use", description="Copernicus dataset")
):
    """Get climate and land use data from EU Copernicus - Comprehensive Earth observation datasets"""
    try:
        data = await official_nasa_service.get_copernicus_climate_data(lat, lng, dataset)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/wri-urban")
async def get_wri_urban_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    dataset: str = Query("urban-landscape", description="WRI dataset")
):
    """Get urban landscape data from World Resources Institute - Urban landscapes, ecosystems, climate, and economic data"""
    try:
        data = await official_nasa_service.get_wri_urban_data(lat, lng, dataset)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/official/comprehensive")
async def get_comprehensive_urban_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude")
):
    """Get comprehensive urban data from all official NASA Space Apps Challenge 2025 sources"""
    try:
        data = await official_nasa_service.get_comprehensive_urban_data(lat, lng)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Working APIs - Landsat STAC
@app.get("/api/landsat/satellite-imagery")
async def get_satellite_imagery(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers"),
    cloud_cover: int = Query(20, description="Maximum cloud cover percentage"),
    limit: int = Query(5, description="Maximum number of results")
):
    """Get Landsat satellite imagery for a specific location"""
    try:
        async with LandsatService() as service:
            data = await service.get_satellite_imagery(lat, lng, radius_km, cloud_cover, limit)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/landsat/vegetation-analysis")
async def get_vegetation_analysis(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(5.0, description="Search radius in kilometers")
):
    """Get vegetation analysis data (NDVI) for a location"""
    try:
        async with LandsatService() as service:
            data = await service.get_vegetation_analysis(lat, lng, radius_km)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/landsat/urban-heat-island")
async def get_urban_heat_island_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(10.0, description="Search radius in kilometers")
):
    """Get urban heat island analysis data"""
    try:
        async with LandsatService() as service:
            data = await service.get_urban_heat_island_data(lat, lng, radius_km)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Working APIs - WorldPop
@app.get("/api/worldpop/population-data")
async def get_worldpop_data(
    country_code: str = Query("USA", description="ISO3 country code"),
    year: int = Query(2020, description="Year for population data")
):
    """Get population data from WorldPop API"""
    try:
        async with WorldPopService() as service:
            data = await service.get_population_data(country_code, year)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/worldpop/urban-density")
async def get_urban_population_density(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    country_code: str = Query("USA", description="ISO3 country code"),
    year: int = Query(2020, description="Year for population data"),
    radius_km: float = Query(10.0, description="Search radius in kilometers")
):
    """Get urban population density for a specific location"""
    try:
        async with WorldPopService() as service:
            data = await service.get_urban_population_density(lat, lng, country_code, year, radius_km)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/worldpop/urban-growth-trends")
async def get_urban_growth_trends(
    country_code: str = Query("USA", description="ISO3 country code"),
    start_year: int = Query(2000, description="Starting year for trend analysis"),
    end_year: int = Query(2020, description="Ending year for trend analysis")
):
    """Get urban growth trends over time"""
    try:
        async with WorldPopService() as service:
            data = await service.get_urban_growth_trends(country_code, start_year, end_year)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Working APIs - EU Copernicus
@app.get("/api/copernicus/land-use")
async def get_land_use_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(10.0, description="Search radius in kilometers"),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    """Get land use and land cover data from EU Copernicus"""
    try:
        async with CopernicusService() as service:
            data = await service.get_land_use_data(lat, lng, radius_km, start_date, end_date)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/copernicus/climate-data")
async def get_copernicus_climate_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(10.0, description="Search radius in kilometers"),
    climate_type: str = Query("temperature", description="Type of climate data")
):
    """Get climate data from EU Copernicus"""
    try:
        async with CopernicusService() as service:
            data = await service.get_climate_data(lat, lng, radius_km, climate_type)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/copernicus/atmospheric-data")
async def get_atmospheric_data(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(10.0, description="Search radius in kilometers")
):
    """Get atmospheric data for air quality analysis"""
    try:
        async with CopernicusService() as service:
            data = await service.get_atmospheric_data(lat, lng, radius_km)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Working APIs - NASA Image Library
@app.get("/api/nasa-library/search")
async def search_nasa_imagery(
    query: str = Query("urban", description="Search query"),
    media_type: str = Query("image", description="Type of media"),
    year_start: Optional[int] = Query(None, description="Start year for search"),
    year_end: Optional[int] = Query(None, description="End year for search"),
    page: int = Query(1, description="Page number for pagination"),
    page_size: int = Query(20, description="Number of results per page")
):
    """Search NASA Image and Video Library"""
    try:
        async with NASALibraryService() as service:
            data = await service.search_urban_imagery(query, media_type, year_start, year_end, page, page_size)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa-library/historical-urban")
async def get_historical_urban_data(
    city_name: str = Query("New York", description="Name of the city"),
    decade: Optional[str] = Query(None, description="Specific decade"),
    media_type: str = Query("image", description="Type of media")
):
    """Get historical urban imagery for a specific city"""
    try:
        async with NASALibraryService() as service:
            data = await service.get_historical_urban_data(city_name, decade, media_type)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa-library/climate-visualization")
async def get_climate_change_visualization(
    location: str = Query("global", description="Location to search for"),
    time_period: str = Query("decade", description="Time period for comparison"),
    media_type: str = Query("image", description="Type of media")
):
    """Get climate change visualization imagery"""
    try:
        async with NASALibraryService() as service:
            data = await service.get_climate_change_visualization(location, time_period, media_type)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Analysis Endpoints
@app.post("/api/ai/analyze-urban-data")
async def analyze_urban_data(request: AnalysisRequest):
    """Comprehensive AI analysis of urban data from all sources"""
    try:
        data = await ai_analysis_service.analyze_urban_data(
            request.coordinates[0], 
            request.coordinates[1], 
            context=request.context
        )
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):
    """AI chat with urban planning context"""
    try:
        data = await ai_analysis_service.generate_ai_chat_response(
            request.message, 
            request.context or {}
        )
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/visualization-data")
async def get_visualization_data(
    analysis_type: str = Query("dashboard", description="Type of visualization"),
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude")
):
    """Generate data for frontend visualizations"""
    try:
        context = {"lat": lat, "lng": lng}
        data = await ai_analysis_service.generate_visualization_data(analysis_type, context)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Data Sources Info
@app.get("/api/data-sources")
async def get_data_sources():
    """Get information about available NASA data sources"""
    return JSONResponse(content={
        "official_nasa_space_apps_2025": {
            "description": "Official NASA Space Apps Challenge 2025 Resources for Data Pathways to Healthy Cities",
            "sources": [
                {
                    "name": "NASA Earthdata Worldview",
                    "description": "Primary satellite data visualization platform",
                    "endpoint": "/api/official/earthdata-worldview",
                    "purpose": "Real-time satellite imagery and climate data"
                },
                {
                    "name": "NASA SEDAC",
                    "description": "Socioeconomic Data and Applications Center - UN SDGs",
                    "endpoint": "/api/official/sedac-demographic",
                    "purpose": "Demographic and equity analysis"
                },
                {
                    "name": "EU Copernicus GHSL",
                    "description": "Global Human Settlement Layer",
                    "endpoint": "/api/official/ghsl-urban",
                    "purpose": "Urban population and settlement data"
                },
                {
                    "name": "WorldPop",
                    "description": "Open source population data",
                    "endpoint": "/api/official/worldpop",
                    "purpose": "Urban change and population density analysis"
                },
                {
                    "name": "EU Copernicus Services",
                    "description": "Comprehensive Earth observation datasets",
                    "endpoint": "/api/official/copernicus-climate",
                    "purpose": "Climate, land use, and atmospheric data"
                },
                {
                    "name": "World Resources Institute",
                    "description": "Urban landscapes and ecosystem data",
                    "endpoint": "/api/official/wri-urban",
                    "purpose": "Economic and ecosystem health metrics"
                }
            ]
        },
        "legacy_nasa_sources": {
            "description": "Traditional NASA data sources",
            "sources": [
                {
                    "name": "MODIS Land Surface Temperature",
                    "description": "Daily land surface temperature data",
                    "resolution": "1km",
                    "frequency": "Daily",
                    "latency": "24-48 hours"
                },
                {
                    "name": "Aura OMI Nitrogen Dioxide",
                    "description": "Air quality and pollution monitoring",
                    "resolution": "13km x 24km",
                    "frequency": "Daily",
                    "latency": "24-48 hours"
                },
                {
                    "name": "Landsat 8 NDVI",
                    "description": "Vegetation health and green space analysis",
                    "resolution": "30m",
                    "frequency": "16 days",
                    "latency": "2-4 weeks"
                },
                {
                    "name": "GPM Precipitation",
                    "description": "Precipitation and flood risk assessment",
                    "resolution": "0.1° x 0.1°",
                    "frequency": "30 minutes",
                    "latency": "4-6 hours"
                }
            ]
        }
    })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
