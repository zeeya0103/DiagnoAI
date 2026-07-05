from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
def dashboard():

    return {
        "reports": 350,
        "appointments": 80
    }