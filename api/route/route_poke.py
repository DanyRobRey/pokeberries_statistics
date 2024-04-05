from fastapi import FastAPI, APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from db.repository.berries import get_berries_statistics, get_berries_statistics_plot
from schemas import schema_poker_berry

router = APIRouter()

app = FastAPI(
    debug=False,
    title="Poke Berry Service",
)


@router.get(
    "/allBerryStats",
    response_model=schema_poker_berry.PokerBerrysStats,
)
async def get_berries_stats():
    """
    Endpoint to retrieve statistics for all berries.

    Returns:
        schema_poker_berry.PokerBerrysStats: Statistics for all berries.

    Raises:
        HTTPException: If there's a bad request.
        Exception: If there's an internal server error.
    """
    try:
        poker_berrys_stats, berries_growth_times = await get_berries_statistics()

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "Bad Request", "error": e.detail},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "Internal Server Error", "error": str(e)},
        )
    return poker_berrys_stats


@router.get("/allBerryStatsPlot")
async def plot_image():
    """
    Endpoint to retrieve a plot of statistics for all berries.

    Returns:
        Response: A response containing the plot image in PNG format.

    Raises:
        HTTPException: If there's a bad request.
        Exception: If there's an internal server error.
    """
    try:
        poker_berrys_stats_plot = await get_berries_statistics_plot()

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "Bad Request", "error": e.detail},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "Internal Server Error", "error": str(e)},
        )
    return Response(content=poker_berrys_stats_plot.getvalue(), media_type="image/png")


app.include_router(router)
