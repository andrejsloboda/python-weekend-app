from typing import List
import datetime 
import uvicorn
from rapidfuzz.distance import Levenshtein as ls
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status
from .scrapers import RegiojetScraper
from .schemas import RouteOut, RouteCombination
from .database.database import is_in_db, get_combinations_from_db, get_routes_from_db
from .database.database import add_routes_to_db
from .keys import create_route_key
from .cache import Cache

# Init cache 
cache = Cache()

# Init scraper and FastAPI 
scraper = RegiojetScraper(cache)
app = FastAPI() 

# API configuration for Kiwi front-end
origins = ["*"] 

app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["GET"],
    allow_headers=["application/json"]
)


@app.get('/ping')
def ping():
    return 'pong'


@app.get("/whisper") 
def whisper(text: str):
    return [city for city in scraper.cities if ls.normalized_similarity(text, city) > 0.5]


@app.get("/search", response_model=List[RouteOut])
def search(origin: str, destination: str, departure: datetime.date):
    route_key = create_route_key(origin, destination, departure)

    if cache.is_in_cache(route_key):
        print_out = cache.get_routes(route_key)
        
    else:
        if is_in_db(origin, destination, departure):
            db_routes = get_routes_from_db(origin, destination, departure)
            cache.set_routes(route_key, db_routes)
            print_out = db_routes
            
        else:
            scraped_routes = scraper.scrape(origin, destination, departure)
            add_routes_to_db(scraped_routes)
            cache. set_routes(route_key, scraped_routes)
            print_out = scraped_routes
            
    if print_out:
        return print_out
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/search/combinations", response_model=List[RouteCombination])
def combinations(origin: str, destination: str, departure: datetime.date):
    print_out = get_combinations_from_db(origin, destination, departure)
    
    if print_out:
        return print_out
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, log_level="info")




    








  







    

    
    
    
    
    
    
    
