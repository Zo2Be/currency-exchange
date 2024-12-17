import logging
from fastapi import APIRouter, Depends
from app.utils.external_api import currency_list, convert_currency
from app.api.schemas.currency import Currency
from app.core.security import get_user_from_token


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list/", dependencies=[Depends(get_user_from_token)])
async def get_currency_list() -> dict:
    logger.info("User requested currency list")
    return await currency_list()


@router.post("/exchange/", dependencies=[Depends(get_user_from_token)])
async def get_convert_currency(currency: Currency):
    logger.info("User requested currency conversion")
    return await convert_currency(currency)
