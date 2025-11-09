
from fastapi import FastAPI, UploadFile, File
from typing import Optional
import uvicorn

app = FastAPI(
    title="Somint Grading Engine",
    description="AI-powered TCG grading service.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"message": "Welcome to the Somint Grading Engine"}

@app.post("/grade-card/")
async def grade_card_image(file: UploadFile = File(...)):
    """
    Placeholder endpoint for the grading pipeline.

    This will eventually take an image, run it through the CV pipeline,
    and return a detailed grading report.
    """
    # For now, just return the filename and content type
    return {"filename": file.filename, "content_type": file.content_type}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
