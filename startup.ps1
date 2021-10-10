# not working yet
cd services
uvicorn game_service:app --reload
uvicorn dict_service:app --reload
uvicorn data_service:app --reload