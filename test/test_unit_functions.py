import pytest
import unittest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from db.repository.berries import get_berry, get_berries


@pytest.mark.asyncio
async def test_get_berry_failure():
    with patch("httpx.AsyncClient") as MockAsyncClient:
        mock_client_instance = MockAsyncClient.return_value
        mock_client_instance.get.return_value = AsyncMock(status_code=500)

        with unittest.TestCase().assertRaises(HTTPException):
            await get_berry("cheri")


@pytest.mark.asyncio
async def test_get_berries_failure():
    with patch("httpx.AsyncClient") as MockAsyncClient:
        mock_client_instance = MockAsyncClient.return_value
        mock_client_instance.get.return_value = AsyncMock(status_code=500)

        with unittest.TestCase().assertRaises(HTTPException):
            await get_berries(offset=0, limit=10)
