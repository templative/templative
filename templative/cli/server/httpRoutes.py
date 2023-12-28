from aiohttp import web
from templative.lib.create import projectCreator, componentCreator

routes = web.RouteTableDef()

@routes.get("/status")
async def getStatus(_):
  return web.Response(status=200)

@routes.post("/project") 
async def createProject(request):
  data = await request.json()
  if data["directoryPath"] == None:
    return "Missing directoryPath", 400
  
  result = await projectCreator.createProjectInDirectory(data["directoryPath"])
  if result != 1:
    return web.Response(status=500)
  return web.Response(status=200)

@routes.post("/component") 
async def createComponent(request):
  data = await request.json()
  if data["componentName"] == None:
    return "Missing componentName", 400
  if data["componentType"] == None:
    return "Missing componentType", 400
  if data["directoryPath"] == None:
    return "Missing directoryPath", 400
  
  await componentCreator.createCustomComponent(data["directoryPath"], data["componentName"], data["componentType"])

  return web.Response(status=200)