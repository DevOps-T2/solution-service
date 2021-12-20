import logging

from fastapi import FastAPI
from sqlalchemy import create_engine

from .models import SolutionRequest, PastComputations
from .database import Session, Base, Solution
from .file_storage import drop_file


app = FastAPI()


@app.on_event("startup")
async def init() -> None:
    engine = create_engine('sqlite:///solutions.db', echo=True)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)


@app.get("/computations/{user_id}/")
def get_computations(user_id: str):
    with Session() as session:
        solutions = session.query(Solution).filter_by(user_id=user_id)

    return PastComputations(computation_ids=[s.computation_id for s in solutions])


@app.get("/solution/{computation_id}")
def get_solution(computation_id: str):
    with Session() as session:
        solution = session.query(Solution).filter_by(computation_id=computation_id).first()

    return {"url": solution.url}



@app.post("/solution/{computation_id}")
def add_solution(solution_request: SolutionRequest):

    url = drop_file(solution_request.body)
    solution = Solution(user_id=solution_request.user_id,
                        computation_id=solution_request.computation_id,
                        url=url)

    with Session() as session:
        session.add(solution)
        session.commit()
