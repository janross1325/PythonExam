## ReadMe
## How to run
1. Copy the .env file to the root directory
2. Run **pip install -r requirements.txt** for dependency installations
3. Run **uvicorn main:app --reload** to run the application
## Available Use Cases
* [POST] /user/register -> args: {email: str, password: str} (required)
* [GET] **image/get_images** args: {limit: int, default = 0}
* [GET] **image/get_image/{image_id}** args: {image_id: int} (required)
* [PATCH] **image/update_image/{image_id}** args: {image_id: int} (required)
* [POST] **image/create_image/{image_id}** args: {url: str (required), owner: str (optional)}(required)
* [DELETE] **image/delete_image/{image_id}** args: {image_id: int} (required) 