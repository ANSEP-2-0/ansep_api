from fastapi import APIRouter
from utils.api import R_MS_URL
from schemas.analysis import Parameters
import httpx

router = APIRouter()

containers = []
containers_running = []

@router.post("/r-ms/run-fba")   
async def run_fba(parameters: Parameters):
    global containers
    print("containers: ", containers)
    global containers_running
    print("containers_running: ", containers_running)
    sbml_model: str = "dopa_parkinsonwoC.xml"
    if not containers_running:
        if not containers:
            await createContainer()
        await startContainer(containers[-1])    
    container_id = containers_running[-1]
    # print(container_id)
    exec_id = await createExec(container_id, createCMD(parameters.parameters_string, sbml_model=sbml_model, script="run_fba.r"))
    print("exec_id: ", exec_id)
    result = await startExec(exec_id)
    # await stopContainer(container_id)
    # containers.append(container_id)
    # containers_running.remove(container_id)
    print("result: ", result) 
    return result

async def getContainersList():
    async with httpx.AsyncClient() as client:
        ans = httpx.get(R_MS_URL + "containers/json")
    return ans

async def createContainer():
    try:
        global containers
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "Image": "ansep/r_ms",
            "Tty": True
        }
        async with httpx.AsyncClient() as client:
            ans = httpx.post(R_MS_URL + f"/containers/create", json=body, headers=headers)
        id = ans.json()["Id"]
        containers.append(id)
        return id
    except Exception as e:
        print("Error creating contrainer: ", e)
        return False
    
async def startContainer(container_id):
    try:
        global containers_running
        headers = {
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            ans = httpx.post(R_MS_URL + f"/containers/{container_id}/start", headers=headers)
        if ans.status_code == 204:
            containers_running.append(container_id)
        else:
            print("Error starting container: ", ans.json())
    except Exception as e:
        print("Error starting container: ", e)
        return False

async def createExec(container_id, cmd):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "AttachStdout": True,
            "WorkingDir": "",
            "Cmd": cmd
        }
        async with httpx.AsyncClient() as client:
            ans = httpx.post(R_MS_URL + f"/containers/{container_id}/exec", json=body, headers=headers)
        return ans.json()["Id"]
    except Exception as e:
        print("Error creating exec: ", e)
        return False

async def startExec(exec_id):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "Detach": False,
            "Tty": True
        }
        async with httpx.AsyncClient() as client:
            ans = httpx.post(R_MS_URL + f"/exec/{exec_id}/start", json=body, headers=headers, timeout=None)
        print("Exec ans: ", ans.text)
        return ans.text
    except Exception as e:
        print("Error starting exec: ", e)
        return False

def createCMD(parameters, script="run_fba.r",sbml_model="dopa_parkinsonwoC.xml"):
    return ([
        "Rscript",
        f"r-scripts/{script}",
        f"sbml/{sbml_model}",
        parameters
    ])

async def stopContainer(container_id):
    headers = {
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        ans = httpx.get(R_MS_URL + f"containers/{container_id}/stop", headers=headers)
    return ans.json()