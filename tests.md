| Testcase Name                     | API Endpoint        | Testcase Description                                                        | Testcase Type | Steps to Test                                                                                                                                                                                                        |
|:----------------------------------|:--------------------|:----------------------------------------------------------------------------|:--------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Authenticate                      | /api/authenticate/  | User gets JWT tokens with valid credentials                                 | Positive      | 1. Send POST request with valid credentials: email, password 2. Check if the response is 200 3. Check if the response body contains valid JWT Tokens                                                                 |
| Authenticate - Invalid email/pass | /api/authenticate/  | Unsuccessful login request with invalid credentials                         | Negative      | 1. Send POST request with invalid credentials: email, password 2. Check if the response is 401 3. Check if the response body contains error message                                                                  |
| Authenticate - Missing email/pass | /api/authenticate/  | Unsuccessful login request with missing credentials                         | Negative      | 1. Send POST request with missing email or password 2. Check if the response is 400 3. Check if the response body contains error message                                                                             |
| Get User Details                  | /api/user/          | Get user details with valid JWT token as auth                               | Positive      | 1. Send GET request with valid JWT access token 2. Check if the response is 200 3. Check if the response body contains user details 4. Cross validate user details with database                                     |
| Get User - Invalid Auth           | /api/user/          | Unsuccessful user detail request with missing/invalid/expired JWT token     | Negative      | 1. Send GET request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message                                                                               |
| Follow User                       | /api/follow/{id}/   | Follow an existing user using JWT authentication                            | Positive      | 1. Send POST request with valid JWT access token 2. Check if the response is 200 3. Check both users following and follower updated from /user endpoint and db                                                       |
| Follow User - Invalid ID          | /api/follow/{id}/   | Unsuccessful follow request with follow non-existent user id                | Negative      | 1. Send POST request with valid JWT access token and invalid user ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no new follow added in db and /user               |
| Follow User - Missing ID          | /api/follow/        | Unsuccessful follow request with missing follow user id                     | Negative      | 1. Send POST request with valid JWT access token with no user ID 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no new follow added in db and /user                   |
| Follow User - Already followed    | /api/follow/{id}/   | Unsuccessful follow request if user already followed                        | Negative      | 1. Send POST request with valid JWT access token with user ID of already followed user 2. Check if response is 400 3. Check if the response body contains error message 4. Check no new follow added in db and /user |
| Follow User - Invalid Auth        | /api/follow/{id}/   | Unsuccessful follow request with missing/invalid/expired JWT token          | Negative      | 1. Send POST request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no new follow added in db and /user                                 |
| Unfollow User                     | /api/unfollow/{id}/ | Unfollow a followed user using JWT authentication                           | Positive      | 1. Send POST request with valid JWT access token 2. Check if the response is 200 3. Check both users following and follower updated from /user endpoint and db                                                       |
| Unfollow User - Invalid ID        | /api/unfollow/{id}/ | Unsuccessful unfollow request with unfollow non-existent user id            | Negative      | 1. Send POST request with valid JWT access token and invalid user ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no following removed in db and /user              |
| Unfollow User - Missing ID        | /api/unfollow/      | Unsuccessful unfollow request with missing unfollow user id                 | Negative      | 1. Send POST request with valid JWT access token with no user ID 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no following removed in db and /user                  |
| Unfollow User - Not followed      | /api/unfollow/{id}/ | Unsuccessful unfollow request if user not followed                          | Negative      | 1. Send POST request with valid JWT access token with user ID of user not followed 2. Check if response is 400 3. Check if the response body contains error message 4. Check no following removed in db and /user    |
| Unfollow User - Invalid Auth      | /api/unfollow/{id}/ | Unsuccessful unfollow request with missing/invalid/expired JWT token        | Negative      | 1. Send POST request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no following removed in db and /user                                |
| Create Post                       | /api/posts/         | Create post successfully on sending required fields in correct format       | Positive      | 1. Send POST request with valid JWT access token with required fields: title, desc 2. Check if the response is 201 3. Check if the response body contains post details 4. Cross validate post details with database  |
| Create Post - Missing fields      | /api/posts/         | Unsuccessful post creation on a missing required field                      | Negative      | 1. Send POST request with valid JWT access token with missing fields: title or desc 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no new post created in db          |
| Create Post - Invalid Auth        | /api/posts/         | Unsuccessful post creation on missing/invalid/expired JWT token             | Negative      | 1. Send POST request with invalid/expired JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no new post created in db                                   |
| Delete Post                       | /api/posts/{id}/    | Delete post successfully on sending DELETE request with correct auth        | Positive      | 1. Send DELETE request with valid JWT access token 2. Check if the response is 200 3. Check if the response body contains post details 4. Cross validate post details with database                                  |
| Delete Post - Invalid ID          | /api/posts/{id}/    | Unsuccessful post deletion on sending non-existent post id                  | Negative      | 1. Send DELETE request with valid JWT access token and invalid post ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no post deleted in db                           |
| Delete Post - Missing ID          | /api/posts/         | Unsuccessful post deletion on missing post id                               | Negative      | 1. Send DELETE request with valid JWT access token with no post ID 2. Check if the response is 405 (Same endpoint for creation) 3. Check if the response body contains error message 4. Check no post deleted in db  |
| Delete Post - Not owner           | /api/posts/{id}/    | Unsuccessful post deletion on sending post id of other user                 | Negative      | 1. Send DELETE request with valid JWT access token and post ID of other user 2. Check if the response is 403 3. Check if the response body contains error message 4. Check no post deleted in db                     |
| Delete Post - Invalid auth        | /api/posts/{id}/    | Unsuccessful post deletion on sending missing/invalid/expired JWT token     | Negative      | 1. Send DELETE request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no post deleted in db                                             |
| Get Post                          | /api/posts/{id}/    | Get post details successfully on sending valid post id                      | Positive      | 1. Send GET request with valid JWT access token and valid post ID 2. Check if the response is 200 3. Check if the response body contains post details 4. Cross validate post details with database                   |
| Get Post - Invalid ID             | /api/posts/{id}/    | Unsuccessful post details request on sending non-existent post id           | Negative      | 1. Send GET request with valid JWT access token and invalid post ID 2. Check if the response is 404 3. Check if the response body contains error message                                                             |
| Get Post - Missing ID             | /api/posts/         | Unsuccessful post details request on missing post id                        | Negative      | 1. Send GET request with valid JWT access token with no post ID 2. Check if the response is 405 (Same endpoint for creation) 3. Check if the response body contains error message                                    |
| Get All Posts                     | /api/all_posts/     | Get all posts successfully on sending GET request with valid auth           | Positive      | 1. Send GET request with valid JWT access token 2. Check if the response is 200 3. Check if the response body contains all posts of validated user 4. Cross validate post details with database                      |
| Get All Posts - Invalid Auth      | /api/all_posts/     | Unsuccessful all_posts request on sending missing/invalid/expired JWT token | Negative      | 1. Send GET request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message                                                                               |
| Like Post                         | /api/like/{id}/     | Like post successfully on sending valid post id                             | Positive      | 1. Send POST request with valid JWT access token and valid post ID 2. Check if the response is 200 3. Check post details updated in database                                                                         |
| Like Post - Invalid ID            | /api/like/{id}/     | Unsuccessful like request on sending non-existent post id                   | Negative      | 1. Send POST request with valid JWT access token and invalid post ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no like added in db                               |
| Like Post - Own post              | /api/like/{id}/     | Unsuccessful like request on sending post id of own post                    | Negative      | 1. Send POST request with valid JWT access token and post ID of own post 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no like added in db                           |
| Like Post - Already liked         | /api/like/{id}/     | Unsuccessful like request on sending post id of post already liked          | Negative      | 1. Send POST request with valid JWT access token and post ID of post already liked 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no like added in db                 |
| Like Post - Invalid Auth          | /api/like/{id}/     | Unsuccessful like request on sending missing/invalid/expired JWT token      | Negative      | 1. Send POST request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no like added in db                                                 |
| Unlike Post                       | /api/unlike/{id}/   | Unlike post successfully on sending valid post id                           | Positive      | 1. Send POST request with valid JWT access token and valid post ID 2. Check if the response is 200 3. Check post details updated in database                                                                         |
| Unlike Post - Invalid ID          | /api/unlike/{id}/   | Unsuccessful unlike request on sending non-existent post id                 | Negative      | 1. Send POST request with valid JWT access token and invalid post ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no like removed in db                             |
| Unlike Post - Own post            | /api/unlike/{id}/   | Unsuccessful unlike request on sending post id of own post                  | Negative      | 1. Send POST request with valid JWT access token and post ID of own post 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no like removed in db                         |
| Unlike Post - Not liked           | /api/unlike/{id}/   | Unsuccessful unlike request on sending post id of post not liked            | Negative      | 1. Send POST request with valid JWT access token and post ID of post not liked 2. Check if the response is 400 3. Check if the response body contains error message 4. Check no like removed in db                   |
| Unlike Post - Invalid Auth        | /api/unlike/{id}/   | Unsuccessful unlike request on sending missing/invalid/expired JWT token    | Negative      | 1. Send POST request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no like removed in db                                               |
| Comment Post                      | /api/comment/{id}/  | Comment on post successfully on sending valid post id with required fields  | Positive      | 1. Send POST request with valid JWT access token and valid post ID with required field: comment 2. Check if the response is 201 3. Check post details updated in database                                            |
| Comment Post - Invalid ID         | /api/comment/{id}/  | Unsuccessful comment request on sending non-existent post id                | Negative      | 1. Send POST request with valid JWT access token and invalid post ID 2. Check if the response is 404 3. Check if the response body contains error message 4. Check no comment added in db                            |
| Comment Post - Invalid Auth       | /api/comment/{id}/  | Unsuccessful comment request on sending missing/invalid/expired JWT token   | Negative      | 1. Send POST request with invalid JWT access token 2. Check if the response is 401 3. Check if the response body contains error message 4. Check no comment added in db                                              |