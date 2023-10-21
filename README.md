
FE-url: https://capstone-fe-umber.vercel.app/
BE-url: https://capstone-be-8yhm.onrender.com/

because the FE I build on render got error out of memmory, look like the free tier of render not engough for my ionic angular so I use vercel instead of, but the BE I still use render as the requirements

- you can use the api the give below to test by post man or go to the FE to test via my account that I give you.

Full access and role:
   user22@yopmail.com
   123456

get:drinks-detail only:
   hsonnl.test.auth1@gmail.com
   Halodc@00000

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions: https://capstone-be-8yhm.onrender.com/
   - `get:drinks` : https://capstone-be-8yhm.onrender.com/drinks
   - `get:drinks-detail`: https://capstone-be-8yhm.onrender.com/drinks-detail
   - `post:drinks` https://capstone-be-8yhm.onrender.com/drinks
   - `patch:drinks`: https://capstone-be-8yhm.onrender.com/drinks/2
   - `delete:drinks`: https://capstone-be-8yhm.onrender.com/drinks/2
6. Create new roles for:
   - customer (EMAIL: user23@yopmail.com - PASSWORD: 123456):
     - can `get:drinks-detail`
     - can `get:drinks`

   - Manager (EMAIL: hsonnl.test.auth1@gmail.com - PASSWORD: Halodc@00000)
     - can perform all actions

7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
