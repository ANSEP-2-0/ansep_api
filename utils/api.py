from dotenv import load_dotenv
import os

load_dotenv()

# CORS ORIGINS
FRONT_END_PROTOCOL = os.environ.get('FRONT_END_PROTOCOL')
FRONT_END_HOST = os.environ.get('FRONT_END_HOST')
FRONT_END_PORT = os.environ.get('FRONT_END_PORT')
FRONT_END_URL = f"{FRONT_END_PROTOCOL}://{FRONT_END_HOST}:{FRONT_END_PORT}"
origins = ["*"]

# R Microservice
R_MS_HOST = os.environ.get('R_MS_HOST')
R_MS_PORT = os.environ.get('R_MS_PORT')
DOCKER_API_VERSION = os.environ.get('DOCKER_API_VERSION')
R_MS_URL = f"http://{R_MS_HOST}:{R_MS_PORT}/{DOCKER_API_VERSION}"
print("R_MS_URL: ", R_MS_URL)

# User Microservice
USER_MS_HOST = os.environ.get('USER_MS_HOST')
USER_MS_PORT = os.environ.get('USER_MS_PORT')
USER_MS_URL = f"http://{USER_MS_HOST}:{USER_MS_PORT}"
# print("USER_MS_URL: ", USER_MS_URL)