import logging
from math import cos, radians
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session
from starlette import status

from models.address_book import AddressBook
from models.db import get_db_session
from schemas.address_book import AddressDetails, UpdateAddress

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


router = APIRouter(
    prefix="/book",
    tags=["Book"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/get/{distance}/{longitude}/{latitude}",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=List[AddressDetails],
)
async def get_address(
    distance: int,
    longitude: float,
    latitude: float,
    session: Session = Depends(get_db_session),
):
    try:
        logger.info("Getting Address")
        location_range = get_location_range(latitude, longitude, distance)
        return (
            session.query(
                AddressBook.address, AddressBook.latitude, AddressBook.longitude
            )
            .filter(
                AddressBook.latitude.between(
                    location_range["min_latitude"], location_range["max_latitude"]
                ),
                AddressBook.longitude.between(
                    location_range["min_longitude"], location_range["max_longitude"]
                ),
            )
            .all()
        )

    except Exception as error:
        logger.error(f"Internal server error {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )


@router.post(
    "/add",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def add_address(
    address: AddressDetails, session: Session = Depends(get_db_session)
):
    geolocator = Nominatim(user_agent="address_book")
    try:
        logger.info("Adding Address")
        if location := geolocator.geocode(address.address):
            logger.info(f"longitude {location.longitude} latitude {location.latitude}")
            add_address = AddressBook(
                latitude=location.latitude,
                longitude=location.longitude,
                address=address.address,
            )
            logger.info("Adding Address To The Db")
            session.add(add_address)
            session.commit()
            return {"message": "Succesfuly added the address"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to find the location",
            )
    except Exception as error:
        logger.error(f"Internal server error {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )


@router.put(
    "/update",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def update_address(
    address: UpdateAddress, session: Session = Depends(get_db_session)
):
    geolocator = Nominatim(user_agent="address_book")
    try:
        logger.info("Updating")
        old_location = (
            session.query(AddressBook).filter_by(address=address.old_address).first()
        )
        if not old_location:
            return {"message": "Unable to given find the location in db"}

        if location := geolocator.geocode(address.new_address):
            old_location.latitude = location.latitude
            old_location.longitude = location.longitude
            logger.info(f"longitude {location.longitude} latitude {location.latitude}")
            session.commit()
            return {"message": "Succesfuly updated the address"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to find the location",
            )
    except Exception as error:
        logger.error(f"Internal server error {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )


def get_location_range(latitude, longitude, distance):
    latitude_range = distance / 111.1
    longitude_range = distance / (111.1 * cos(radians(latitude)))

    return {
        "min_latitude": latitude - latitude_range,
        "max_latitude": latitude + latitude_range,
        "min_longitude": longitude - longitude_range,
        "max_longitude": longitude + longitude_range,
    }
