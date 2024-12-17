import logging
import aiohttp
from app.api.schemas.currency import Currency
from app.core.config import Settings

settings = Settings()
logger = logging.getLogger(__name__)


async def currency_list():
    url = "https://api.apilayer.com/currency_data/list"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=settings.headers, data=settings.payload
            ) as response:
                json_data = await response.json()
                result = json_data["currencies"]
                logger.info("Fetched currency list successfully")
                return result
    except aiohttp.ClientError as e:
        logger.error("Error fetching currency list: %s", e)
        return {"error": "Failed to fetch currency list"}


async def convert_currency(currency: Currency) -> dict:
    url: str = (
        f"https://api.apilayer.com/currency_data/convert?to={currency.to_currency}"
        f"&from={currency.from_currency}&amount={currency.amount}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=settings.headers, data=settings.payload
            ) as response:
                json_data = await response.json()
                result = json_data["result"]
                logger.info(
                    "Converted %s from %s to %s successfully",
                    currency.amount,
                    currency.from_currency,
                    currency.to_currency,
                )
                return {"total": result}
    except KeyError:
        logger.error(
            "Invalid currency code %s or %s",
            currency.from_currency,
            currency.to_currency,
        )
        return {"error": "Для просмотра допустимых код валют перейдите в /list."}
    except aiohttp.ClientError as e:
        logger.error("Error converting currency: %s", e)
        return {"error": "Failed to convert currency"}
