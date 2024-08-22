from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from data_extraction import (
    get_coordinates,
    get_nearby_projects,
    get_air_quality,
    get_nearby_facilities
)
from analysis import generate_analysis

router = APIRouter()

class Project(BaseModel):
    name: str
    distance: float
    categories: str
    address: str
    postcode: str
    country: str
    developer_reputation: str
    aqi: Optional[int] = None
    facilities: Optional[List[dict]] = None

class AnalysisRequest(BaseModel):
    place_name: str

@router.post("/analyze")
async def analyze_project(request: AnalysisRequest):
    coordinates = get_coordinates(request.place_name)
    if not coordinates:
        raise HTTPException(status_code=404, detail="Failed to get coordinates")

    lat, lon = coordinates
    nearby_projects = get_nearby_projects(lat, lon)
    
    if not nearby_projects:
        return {"message": "No competitive real estate projects found"}

    main_project_aqi = get_air_quality(lat, lon)
    if not main_project_aqi:
        raise HTTPException(status_code=500, detail="Could not retrieve air quality data for the main project")

    for project in nearby_projects:
        proj_coordinates = get_coordinates(project["name"])
        if proj_coordinates:
            project["coordinates"] = proj_coordinates
            proj_lat, proj_lon = proj_coordinates
            project["aqi"] = get_air_quality(proj_lat, proj_lon)
            categories = ['13018', '13065', '17067', '18025', '18037']
            project["facilities"] = get_nearby_facilities(proj_lat, proj_lon, categories)

    analysis = generate_analysis(request.place_name, main_project_aqi, nearby_projects)
    
    return {
        "main_project": {
            "name": request.place_name,
            "coordinates": coordinates,
            "aqi": main_project_aqi
        },
        "nearby_projects": nearby_projects,
        "analysis": analysis
    }