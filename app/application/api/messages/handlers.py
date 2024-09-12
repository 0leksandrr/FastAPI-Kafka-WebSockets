from fastapi.routing import APIRouter

router = APIRouter(
    tags=["Chat"],
)


@router.post("/")
async def create_chat_handler():
    return {"message": "Hello World"}
