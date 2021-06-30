# sfa_api
Space Fan Art is an API tailored to automatically put a fascinating image of planets and galaxy on your desktop background.


### Version 1
This is the first version of SFA-API. It contains one endpoint that allows you to download an image.

Description:
HTTP Request Type -> GET
Response -> Download file
URL GET Parameters -> N/A
Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/download

### Version 2
This is the second version of SFA-API. It contains one more endpoint that allows you to upload an image.

Description:
HTTP Request Type -> POST
Response -> Upload file
URL GET Parameters -> file / title / explanation / date / copyright
Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/upload

### Version 3
This is the first version of SFA-API. It contains one more endpoint that allows you to register a new user.

Description:
HTTP Request Type -> POST
Response -> Register user
URL POST Parameters -> First name / Last name / email / password
Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/register

### Version 4
This is the first version of SFA-API. It contains one more endpoint that allows you to use a demo key.

Description:
HTTP Request Type -> GET
Response -> Get demo key
URL GET Parameters -> N/A
Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/demo_key



