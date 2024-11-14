from typing import Callable
from fastapi import Request, Response
import logging
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("middleware_logger")


class BaseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, custom_param: str = None):
        super().__init__(app)
        self.custom_param = custom_param
        logger.info(
            f"{self.__class__.__name__} initialized with custom_param: {self.custom_param}"
        )

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logger.info(f"Request method: {request.method}, URL: {request.url}")

        response = await self.process_request(request, call_next)

        return response

    async def process_request(self, request: Request, call_next: Callable) -> Response:

        raise NotImplementedError("Subclasses should implement this method.")


class HeaderMiddleware(BaseMiddleware):
    async def process_request(self, request: Request, call_next: Callable) -> Response:

        logger.info(f"Request headers: {request.headers}")

        response = await call_next(request)

        response.headers["X-Processed-By"] = "HeaderMiddleware"

        logger.info(f"Response headers: {response.headers}")

        return response


class BodyMiddleware(BaseMiddleware):
    async def process_request(self, request: Request, call_next: Callable) -> Response:
        try:
            body = await request.body()
            logger.info(f"Request body: {body.decode()}")
        except Exception as e:
            logger.error(f"Error reading request body: {e}")

        response = await call_next(request)

        return response
