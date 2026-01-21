from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

from pathlib import Path
import joblib
import pickle
import sklearn

