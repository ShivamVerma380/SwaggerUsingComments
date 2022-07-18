from aiohttp import  web
import requests,json
from aiohttp_swagger import *


async def addUser(request):
    """
    ---
    summary: Create user
    description: This end-point allows to create a user.
    tags:
    - User
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: Created user object
      required: false
      schema:
       type: object
       properties:
        name:
         type:
          - "string"
          - "null"
        email:
         type:
          - "string"
          - "null"    
    responses:
        "201":
            description: successful operation. Return "User Created successfully with name " text
        "409":
            description: conflict. Returns "User exists with given email" text 
        "500":
            description: internal server error
    """
    try:  
        data = await request.json()
        # print(await request.read())
        print(data.get("name"))
        name = data.get("name")
        email = data.get("email")
        # name = request.query["name"]
        global users
        global userId
        flag = True
        for i in users:
            if users[i].get("email")==email:
                flag=False
                response_obj = {"Message":"User already exists"}
                return web.Response(text=json.dumps(response_obj),status=409)
        if(flag):
            users[userId] = {"email":email,"name":name}
            userId=userId+1
            response_obj={"Message":"User "+name+" created successfully"}
            return web.Response(text=json.dumps(response_obj),status=200)    
        
    except Exception as e:
        print(str(e))
        response_obj = {"Message":str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)

async def getUser(request):
    
    """
    ---
    description: This end-point allow to update existing user.
    tags:
    - User
    produces:
    - application/json
    summary: GET User
    responses:
        "200":
            description: successful operation. Returns user objects.   
        "500":
            description: Internal Server Errror. 
    """
    try:
        global users;
        return web.Response(text=str(users),status=200)
    except Exception as e:
        print(str(e))
        response_obj={"Message":str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)
    
async def updateUser(request):
    """
    ---
    summary: Update user
    description: This end-point allows to update a user.
    tags:
    - User
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: Created user object
      required: false
      schema:
       type: object
       properties:
        name:
         type:
          - "string"
          - "null"
        email:
         type:
          - "string"
          - "null"    
    responses:
        "200":
            description: successful operation. Returns "User with email updated successfully" text.
        "404":
            description: not found. Returns "User with specified email not found to update" text.    
        "500":
            description: Internal Server Errror. 
    """
    try:
        data = await request.json()
        email = data.get("email")
        name = data.get("name")
        global users;
        flag = True
        for i in users:
            if users[i].get("email") == email:
                flag=False
                users[i] = {"email":email,"name":name}
                response_obj={"Message":"User with email "+email+ " updated successfully"}
                return web.Response(text=json.dumps(response_obj),status=200)
        if(flag):
            response_obj={"Message":"User not found"}
            return web.Response(text=json.dumps(response_obj),status=404)
                
    except Exception as e:
        print(str(e))
        response_obj={"Message":str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)
    
async def deleteUser(request):
    """
    ---
    summary: Delete user
    description: This end-point allows to delete a user.
    tags:
    - User
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: Deleted user object
      schema:
       type: object
       properties:
        email:
         type:
         - "string"
         - "null"
    responses:
        "200":
            description: User deleted successfully.
        "404":
            description: User not found.
        "500":
            description: Internal server error in deleting user.
    """
    try:
        global users;
        data = await request.json()
        email = data.get("email")
        flag = True
        for i in users:
            print(users[i].get("email"))
            if users[i].get("email") == email:
                del users[i]
                flag = False
                response_obj={"Message":"User with email " + email + " deleted successfully"}
                return web.Response(text=json.dumps(response_obj),status=200)
        if flag==True:
            response_obj={"Message":"User with email "+email + " not found"}
            return web.Response(text=json.dumps(response_obj),status=404)
        
    except Exception as e:
        print(str(e))
        response_obj={"Message":str(e)}
        return web.Response(text=json.dumps(response_obj),status=500)

users={}
userId = 0

app = web.Application()
app.router.add_route('POST', "/user", addUser)
app.router.add_route('GET',"/user",getUser)
app.router.add_route("PUT","/user",updateUser)
app.router.add_route('DELETE',"/user",deleteUser)


setup_swagger(app,title="Swagger Documentation using comments" ,description="This swagger documentation for REST Apis is created with help of aiohttp_swagger. We don't need to create yaml file explicitly. For more information visit: https://aiohttp-swagger.readthedocs.io/en/latest/",contact="shivam.r.verma@seagate.com",swagger_url="/api/v1/doc", ui_version=2)  # <-- NEW Doc URI

web.run_app(app, host="127.0.0.1")