from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from constants import URL_FOR_PARSE
from info_search_console_hw5 import load_index, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def root(q):
    index = load_index()
    results = search(q, index)

    sorted_by_score = sorted(results, key=lambda res: res[1], reverse=True)
    result = []
    for (doc_id, score) in sorted_by_score[:min(10, len(results))]:
        result.append(
            {
                "url": f"{URL_FOR_PARSE}/{doc_id}",
                "id": doc_id,
                "score": score
            }
        )
    return result


