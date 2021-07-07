
 <h1>Space Fan Art (SFA - API)</h1>

SFA-API is the prototype of an API with two different architectures (monolothic architecture and a microservice architecture). In both architectures, users have to register to get an authentication key, which allows them to download and upload images from NASA. The images come from two different sources: in the monolithic architecture, they come from a local database containing [365 images from NASA](https://github.com/alicevillar/sfa_api/blob/main/APOD_365). In the microserve architecture, they come directly from  APOD (one of the most famous NASA's Open API) because SFA-API and [APOD](https://github.com/nasa/apod-api) are integrated. 

:arrow_forward: Duration : 3 months
<br>
:arrow_forward: Team : Teamwork of 3

<h3>Currently in progress ! 💻</h3>

> :round_pushpin: Goals to be achieved: 
> * Create two working prototypes with [Flask REST-Plus](https://flask-restplus.readthedocs.io/en/stable/), an extension for Flask that adds support for quickly building REST APIs. 
> * The RESTful API server should be self-documented using [Swagger](https://swagger.io/), therefore with interactive documentation UI. 
> * Showcase the [OWASP Top Ten Proactive Controls](https://owasp.org/www-project-proactive-controls/), security techniques that should be included in every software development project.  
> * Implement extensive testing using [Automation Anywhere](https://www.automationanywhere.com/).
 
<h1>Table of Contents</h1>

<!-- TOC -->
- [1. Overview](#1-overview)
    - [1.1. Monolithic Architecture](#11-monolithic-architecture)
    - [1.2. Microservice Architecture](#12-microservice-architecture)
- [2. Project Interface](#2-project-interface)
- [3. Development timeline](#3-development-timeline)
- [4. Project Structure](#4-project-structure)
- [5. Project Files](#5-project-files)
- [6. Python Dependencies](#6-python-dependencies) 
- [7. Tools](#7-tools) 
- [8. Installation](#8-installation)
- [9. Quick Start](#9-quick-start)
- [10. Authentication Details](#10-authentication-details)
- [11. OWASP Proactive Controls](#11-owasp-proactive-controls)

<!-- /TOC -->

## 1. Overview 

This API, called SFA (Space Fan Art), is an API created with Flask REST-Plus following the best practices proven to secure a REST-API and showcasing the OWASP Top Ten Proactive Controls. This project contains two Prototypes: a monolithic architecture and a microsservice architecture. APOD, one of NASA's most famous Open API's, has been used as a model thoughout the development of both Prototypes:  
 
:arrow_forward: In the monolithic architecture APOD was used as an API model, specially for our web interface, user authentication, Web Service Rate Limits and DEMO_KEY Rate Limits. 
<br>
:arrow_forward:In the microservice architecture, SFA-API is connected with APOD, which returns the picture of the day. 

<br> 
 
Both prototypes allows authenticated users to download and upload images. Here is how it works: user have to register, the system generates an authentication key, which the user will use to download and upload fantastic images of planets and galaxies! SFA-API provides access via swagger and via web interface. The web interface of our API has an additional feature: it automatically puts a fascinating image of planets and galaxies on your desktop background!

> :radio_button: SFA-API FEATURES: 
> * :arrow_forward: user registration, which generates an authentication key
> * :arrow_forward: download images
> * :arrow_forward: upload images
> * :arrow_forward: sign in 
> * :arrow_forward: demo key


## 1.1. Monolithic Architecture

> :small_blue_diamond: Design based on a monolithic architecture, using MVC (Model-View-Controller) pattern. The images are taken from a local database. Here a small NASA dataset of images is used (365 pictures). To create this dataset we used APOD. 

* [Monolithic Architecture - High level system design (HLD) diagram](https://github.com/alicevillar/sfa_api/blob/main/readme_img/monolithic_architecture.jpg) 

## 1.2. Microservice Architecture

> :small_orange_diamond: Design based on a microservice architecture. The SFA-API is connected to a NASA Open API called Astronomy Picture Of The Day (APOD), which returns the picture of the day. 

* [Microsservice Architecture - High level system design (HLD) diagram](https://github.com/alicevillar/sfa_api/blob/main/readme_img/microservice_architecture.jpg) 
 
## 2. Project Interface

:large_blue_circle: SWAGGER INTERFACE

Swagger enabled the development across the entire API lifecycle, from design and documentation, to test and deployment. It has also been used as an interface. 
> :radio_button: FEATURES: 
> * :arrow_forward: user registration (generates an authentication key)
> * :arrow_forward: download images  
> * :arrow_forward: upload images (users can increment our database uploading new images)
> * :arrow_forward: demo key (the demo key is: DEMO_KEY)
> * :arrow_forward: sign in (to comply with GDPR, the system allows users to delete their data)

![print](/readme_img/swagger_print.PNG)

:large_blue_circle: WEB INTERFACE

The Web Interface is our main interface and it was built with HTML/CSS and Javascript. As swagger, it also allows:  a) users authentication, b) download images, and c) upload images. However, our web interface has an additional feature: when user downloads and image, the system automatically puts it as his or her desktop background. It has been  done with ctypes and Eel libraries. 
 
 > :radio_button: FEATURES: 
> * :arrow_forward: user registration, which generates an authentication key
> * :arrow_forward: download images (the system can automatically put an image on user's desktop background) warning:TODO
> * :arrow_forward: upload images (users can increment our database uploading new images)
> * :arrow_forward: demo key (the demo key is: DEMO_KEY)
> * :arrow_forward: sign in (to comply with GDPR, the system allows users to delete their data)

## 3. Development timeline 

:paperclip: VERSION 1

This is the first version of SFA-API. It contains one endpoint that allows you to download an image.
```
* Description:
* HTTP Request Type -> GET
* Response -> Download file
* URL GET Parameters -> N/A
* Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/download
```
:paperclip:VERSION 2 

This is the second version of SFA-API. It contains one more endpoint that allows you to upload an image.
```
* Description:
* HTTP Request Type -> POST
* Response -> Upload file
* URL GET Parameters -> file / title / explanation / date / copyright
* Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/upload
```
:paperclip:VERSION 3 

This is the first version of SFA-API. It contains one more endpoint that allows you to register a new user.

```
* Description:
* HTTP Request Type -> POST
* Response -> Register user
* URL POST Parameters -> First name / Last name / email / password
* Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/register
```
:paperclip:VERSION 4 

This is the first version of SFA-API. It contains one more endpoint that allows you to use a demo key.

```
* Description:
* HTTP Request Type -> GET
* Response -> Get demo key
* URL GET Parameters -> N/A
* Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/demo_key
```

:paperclip:VERSION 5 

:warning:TODO This is the fifth version of SFA-API. It contains one endpoint that allows users to sign in. To comply with GDPR, this allows users to delete their data in the system. 
 
 ```
* Description:
* HTTP Request Type -> POST
* Response -> User loggin    
* URL POST Parameters -> email / password
* Request URL (temporary): -> http://127.0.0.1:5000/pictures/api/v1/signin
```

## 4. Project Structure

The following directory diagram was generated with the comand "tree /F"

```
app/
│   APOD_365
│   application_structure.py
│   decorators.py
│   docker-compose.yaml
│   Dockerfile
│   minimal.py
│   populate_db.py
│   README.md
│   requirements.txt
│   senhas.py
│   server.py
├───images (this folder contains 365 images)
├───controllers
│   │   demo_key_controller.py
│   │   limiters_controller.py
│   │   picture_controller.py
│   │   users_controller.py
```

## 5. Project Files

* `README.md` [README.md](https://github.com/alicevillar/sfa_api/blob/main/README.md)- Contains the description and documentation of the project. 
* `users_controller.py` [users_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/users_controller.py) - defines operations/endpoints with users (user registration).
* `picture_controller.py` [picture_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/picture_controller.py) - defines operations/endpoints with pictures (download and upload).
* `limiters_controller.py` [limiters_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/limiters_controller.py) - This is file implements the counting to limit the use of the API (through user's IP address) and demo key. 
* `demo_key_controller.py` [demo_key_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/demo_key_controller.py) - This file implements the demo key.
* `decorators.py` [decorators.py](https://github.com/alicevillar/sfa_api/blob/main/decorators.py) - This file contains the decorators for the api key and the demo key (to verify the existence and authenticity of the key).   
* `Dockerfile`[Dockerfile](https://github.com/alicevillar/sfa_api/blob/main/Dockerfile) - Docker config file is a recipe to build a Docker image
  running this RESTful API Server.
* `docker-compose.yaml` [docker-compose.yaml](https://github.com/alicevillar/sfa_api/blob/main/docker-compose.yaml) - This is a config file to deploy and configure the docker-container to run. 
* `minimal.py` [minimal.py](https://github.com/alicevillar/sfa_api/blob/main/minimal.py) - This is a config file containing the class API.  
* `populate_db.py` [populate_db.py](https://github.com/alicevillar/sfa_api/blob/main/populate_db.py) - This file is aimed to populate the database.
* `senhas.py` - This file contains the passwords of the database.
* `server.py` [server.py](https://github.com/alicevillar/sfa_api/blob/main/server.py) - This file imports controllers and runs the API. 
* `gitignore` [gitignore](https://github.com/alicevillar/sfa_api/blob/main/.gitignore)- Lists files and file masks of the files which should not be added to git repository.
* `requirements.txt` [requirements.txt](https://github.com/alicevillar/sfa_api/blob/main/requirements.txt) - The list of Python (PyPi) requirements.
* `application_structure.py` [application_structure.py](https://github.com/alicevillar/sfa_api/blob/main/application_structure.py) - Directory tree structure in Python.
* `common_passwords.py` [common_passwords.py](https://github.com/alicevillar/sfa_api/blob/main/useful/common_passwords) - File containing the most 1000 most common passwords. 


## 6. Python Dependencies

* [**Flask-RestPlus**](https://github.com/noirbizarre/flask-restplus) (+
  [*flask*](http://flask.pocoo.org/))  
* [**Werkzeug**](https://pypi.org/project/Werkzeug/) - for password hashing  
  RESTful API documentation.
* [**Secrets**](https://pypi.org/project/python-secrets/) - for generating cryptographically strong pseudo-random numbers for managing user authentication.
* [**Pyodbc**](https://pypi.org/project/pyodbc/) - for accessing the database and carry our user registration.
* [**Requests**](https://pypi.org/project/requests/) - for making HTTP requests in Python. 
* [**Eel**](https://github.com/ChrisKnott/Eel) - a little Python library for hosting our local webserver, then lets us use [Python]( https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python) to automatically set a download image as user's desktop background.   
* [**Flask Login**](https://flask-login.readthedocs.io/en/latest/) - A Flask extension that provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.
* [**Flask Cors**](https://flask-cors.readthedocs.io/en/latest/) - A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible. 
* [**Flask Limiters**](https://flask-limiter.readthedocs.io/en/stable/) - Flask-Limiter provides rate limiting features to flask routes.
* [**Validator Collection**](https://pypi.org/project/validator-collection/) - to validade unsers' inputs. 
* [**Dependency Check**](https://pypi.org/project/dependency-check/) - scans application dependencies and checks whether they contain any published vulnerabilities.

 
## 7. Tools

* [**Docker**](https://www.docker.com/) - for storing the database (of the monolothic architecture) in a container.
* [**Swagger-UI**](https://github.com/swagger-api/swagger-ui) - used for documentation and to allow development team to visualize and interact with the API's. 
* [**SQL Server**](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) - to create the database of Prototype 1 (monolithic architecture)
* [**Ngrok**](https://ngrok.com/) - enabled the exposure of the a local development server to the Internet with minimal effort. 
* [**AWS EC2**](https://aws.amazon.com/pt/ec2/) - cloud computing service used in both prototypes to host and run the applications  
* [**Github**](https://github.com/alicevillar/sfa_api) - to document the project. 
* [**Insomnia**](https://insomnia.rest/) - used to consume APOD and retrieve the 365 images for our dataset (monolithic architecture). 
* [**NASA APOD**](https://api.nasa.gov/) - In the monolithic architecture it was used as an API model. In the microservice architecture it was connected to SFA-API, so our API could therefore provide APOD's functionality which is to return the picture of the day. 
* [**Automation Anywhere**](https://www.automationanywhere.com/) - for testing STF-API (both prototypes). 

## 8. Installation  

 :warning:TODO 
 
<h3>Using Docker</h3>

It's easy to start exploring SFA-API using Docker:

```bash
$ docker run -it --rm --publish 5000:5000 alicevillar/sfa_api
```
<h3>Clone the Project</h3> 

```bash
$ git clone https://github.com/alicevillar/sfa_api
``` 
<h3>Setup Environment </h3>

You will need `invoke` package to work with everything related to this project.

```bash
$ pip install -r tasks/requirements.txt
```
  
## 9. Quick Start  
 
 <br>
:warning:TODO 
  <br>

## 10. Authentication Details

The request body must follow the following structure: 

:large_blue_circle: USER MODEL:
```
{
  "First Name": "Teresa",
  "Last Name": "Saldanha",
  "Email": "mtsaldanha@terra.com.br",
  "Password": "123"
}
```

That is it! 

After regitration, the system will generate the API Key.

 
:large_blue_circle: USER REGISTRATION:

```
curl -X POST "http://127.0.0.1:5000/users/api/v1/register" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"First Name\": \"Teresa\", \"Last Name\": \"Saldanha\", \"Email\": \"mtsaldanha@terra.com.br\", \"Password\": \"123\"}"
{
  "API Key": "1665Sg0UlrAq1BhZOstyPMj9DF-9d-i2o0DcIIB9",
  "Expiration Date": "2021-07-30"
}
```
The response body contains the API Key and the expiration date. Once the access authentication key expires, you have to create a new one. 

## 11. OWASP Proactive Controls

The [OWASP Top Ten Proactive Controls](https://owasp.org/www-project-proactive-controls/) is a list of security techniques that should be included in every software development project. They are ordered by order of importance, with control number 1 being the most important.


 <h3>C1: Define Security Requirements</h3>

The [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) contains categories such as authentication, access control, error handling / logging, and web services. Each category contains a collection of requirements that represent the best practices for that category drafted as verifiable statements. Successful use of security requirements involves four steps: discovering / selecting, documenting, implementing, and then confirming correct implementation of new security features and functionality within an application.

The standard provides a basis for testing security controls to protect against vulnerabilities such as Cross-Site Scripting (XSS) and SQL injection. 

>  :white_check_mark: SFA-API prevents malicious code by using secure authentication methods:
>  * We use parameterised queries to avoid SQL injection attacks in all the operations with the database. 
>  * We also protect against Cross-Site Scripting (XSS) in our web page, using javascript. :warning:TODO

 <h3>C2: Leverage Security Frameworks and Libraries</h3>

Secure frameworks and libraries can help to prevent a wide range of web application vulnerabilities.  

>  :white_check_mark: In SFA-API we a tool recommended by OWASP called [Project Dependency](https://pypi.org/project/dependency-check/) to scan application dependencies and check if they contain any published vulnerabilities. :warning:TODO

 <h3>C3: Secure Database Access</h3>

 According to OWASP, secure access to databases consider: secure queries, secure configuration, secure communication and secure authentication. 

>  :white_check_mark: SFA-API handles secure database access with the following measures: 
> * Secure queries: In order to mitigate SQL injection we used use ‘Query Parameterization’. However, certain locations in a database query are not parameterizable. Because of the large variation in the pattern of SQL injection attacks they are often unable to protect databases. OWASP recomments testing queries for performance, but this is not done here because the queries are all very small and therefore is not necessary. 
> * Secure configuration: we run the database in a docker container, which has connectivvity restrictions (can only be accessed by the administrator and only has one door open - 1433). The server which runs the database does not allow external access. All access to the database should be properly authenticated. Thus, it is not possible to directly access the database from outside the instance. 
> Secure communication: we use Pyodbc, an open source Python module to communicate with the database. We apply secure (authenticated, encrypted) communications methods.  

<h3>C4: Encode and Escape Data</h3>

Encoding and escaping are defensive techniques meant to stop injection attacks. Here is the OWASP definition:
 * Encoding (commonly called “Output Encoding”) involves translating special characters into some different but equivalent form that is no longer dangerous in the target interpreter, for example translating the < character into the &lt; string when writing to an HTML page. 
 * Escaping involves adding a special character before the character/string to avoid it being misinterpreted, for example, adding a \ character before a " (double quote) character so that it is interpreted as text and not as closing a string.
 
> :white_check_mark: In SFA-API, we apply C4: 
> * Encoding in our webpage interface (HTML/CSS, Javascript). :warning:TODO 
> It should be highlightened that a hash is not ‘encryption’ – it cannot be decrypted back to the original text (it is a ‘one-way’ cryptographic function, Whereas encryption is a two-way function, hashing is a one-way function. Hashing is used in conjunction with authentication to produce strong evidence that a given message has not been modified and serves the purpose of ensuring integrity, i.e. making it so that if something is changed you can know that it’s changed.
password is stored in hashed into the database and the authentication process uses hashing comparison. For password hashing we use the library [Werkzeug](https://pypi.org/project/Werkzeug/). 

<h3>C5: Validate All Inputs</h3>

Input validation is a programming technique that ensures only properly formatted data may enter a software system component. It validates that an input value is what you think it should be. Syntax validity means that the data is in the form that is expected. 

> :white_check_mark: SFA-API validates inputs we use the Python library [Validator Collection](https://pypi.org/project/validator-collection/), which is a Python library that provides functions that can be used to validate the type and contents of an input value. :warning:TODO 

 
 <h3>C6: Implement Digital Identity</h3>

OWASP provides several recommendations for secure implementation of Digital Identity, a unique representation of a user. OWASP divide it in three levels: 
* Level 1 : Passwords => It's necessary to store them securely and follow OWASP password requirements. 
* Level 2 : Multi-Factor Authentication => Using passwords as a sole factor provides weak security. Multi-factor solutions provide a more robust solution by requiring an attacker to acquire more than one element to authenticate with the service. 
* Level 3 : Cryptographic Based Authentication => requires authentication that is "based on proof of possession of a key through a cryptographic protocol.” This type of authentication is used to achieve the strongest level of authentication assurance.  

> :white_check_mark: SFA-API applies digital identity, authentication and session management recommendation. We use libraries werkzeug (for password hashing) and secrets (to generate authentication key). 
However, we're only scratching the surface. We are maximizing the security in our API > following OWASP recommendations. Here are the basic security measures we apply to maximize the security in our AP:  
> * Level 1 : Passwords => 
> a) In SFA-API, passwords have at least 8 characters in length; 
> b) All printing ASCII characters as well as the space character are acceptable in memorized secrets. 
> c) We follow the the OWASP recommedation, which is to remove complexity requirements as these have been found to be of limited effectiveness. OWASP recommends the adoption of MFA or longer password lengths instead. What we do it to encourage the use of long passwords and passphrases by recommending this action in the interface. 
> b) we ensure that passwords used are not commonly used passwords by blocking the [top 1000 most common passwords](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt); c) we securely store user credentials, so is a password is compromised, the attacker does not immediately have access to this information. 
> * Level 2 : Multi-Factor Authentication (MFA) => SFA-API applies 2 layers of protection: passwords and authentication key (which works as a token).
> * Level 3 : Cryptographic Based Authentication => Once the initial successful user authentication has taken place, the application tracks this user (this is called Session Management) so it can store details about usage. Flask does it through encrypted cookies. This is implemented on top of cookies for you and signs the cookies cryptographically. What this means is that the user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing. 

 
 <h3>C7: Enforce Access Controls</h3>
 
Access Control functionality often spans many areas of software depending on the complexity of the access control system. In SFA-API, we apply two of the OWASP recommends: a) all request go through some kind of access control verification layer; a) all access control failures should be logged as these may be indicative of a malicious user probing the application for vulnerabilities.

> :white_check_mark: In SFA-API, we maximize the security by using multi-factor authentication in 2 layers of protection: hashing passwords and authentication key.
> Authentication key is given to users after their registration (to registrate, users have give: first name, last name, email and password). The authentication key is monitored
> in three different ways: 
> * a) expiration date – SFA-API has an expiration date, which is done only using pyodbc; 
> * b) rate limits - we implement rate limits with flask limiter. For this we follow one of APOD rules =>> Daily Limit: 50 requests per IP address per day. 
> * c) user IP – The system creates a key that corresponds the client’s IP. If the same client changes IP and tries to authenticate, the system does not allow it and will ask the client to authenticate again. This is done with pyodbc.  
 
<h3>C8: Protect Data Everywhere</h3>

Sensitive data such as passwords, credit card numbers, health records, personal information and business secrets require extra protection, particularly if that data falls under privacy laws (EU’s General Data Protection Regulation GDPR), financial data protection rules such as PCI Data Security Standard (PCI DSS) or other regulations. 

 * a) parametrized queries: makes it possible for the database to recognize the code and distinguish it from input data; 
 * b) least privilege on the database: the focus should be on identifying what access rights or elevated permissions the application needs; 
 * c) stored procedures: a group of SQL statements into a logical unit so subsequent executions allow statements to be automatically parameterized. Simply put, it is a type of code that can be stored for later and used many times.
 * d) escaping: use character-escaping functions for user-supplied input provided by each database management system (DBMS). This is done to make sure the DBMS never confuse it with the SQL statement provided by the developer.

> :white_check_mark: In SFA-API, we protect data with the following measures: 
> a) parametrized queries: are widely applied to protect against SQL injection. 
> b) least privilege on the database: :warning:TODO   
> c) stored procedures: This is not done in SFA-API because the queries are small, so this measure is unecessary. 
> d) escaping: is done in the file [picture_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/picture_controller.py), which defines operations/endpoints with pictures (download and upload). 
 
<h3>C9: Implement Security Logging and Monitoring</h3>
  
Security logging can be used for: Feeding intrusion detection systems, Forensic analysis and investigations, Satisfying regulatory compliance requirements

> :white_check_mark: In SFA-API, we use a logging framework, a utility designed to standardise the process of logging in your application. Our logging framework is Flask->  
> RESTPlus, an extension for Flask that adds support for quickly building REST APIs. Flask-RESTPlus encourages best practices with minimal setup. It provides a coherent
> collection of decorators and tools to describe your API and expose its documentation properly (using Swagger). The logging from FlasK-Rest-Plus is standardised: a request is
> received and then returned. In  FlasK-Rest-Plus the loggins are very simple, they are not very informative (thus, it is not possible to know details about each request). To
> have informative loggins we will use docker, which is where all the loggins will be stored. It is secure. 


<h3>C10:  Handle All Errors and Exceptions</h3>  

Exception handling is a programming concept that allows an application to respond to different error states (like network down, or database connection failed, etc) in various ways. Handling exceptions and errors correctly is critical to making your code reliable and secure.

> :white_check_mark: In SFA-API, we handle error and exceptions in the file [login_controller.py](https://github.com/alicevillar/sfa_api/blob/main/controllers/login_controller.py_

 
 
 ## Useful Links: 
 
[OWASP Proactive Controls](https://owasp.org/www-project-proactive-controls/)

[Flask RestPlus Server Example](https://github.com/frol/flask-restplus-server-example)
 
[Best Practices for a pragmatic restful API](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)
 
[how-to-prevent-sql-injection-attacks](https://www.ptsecurity.com/ww-en/analytics/knowledge-base/how-to-prevent-sql-injection-attacks/#6)

[APOD](https://github.com/nasa/apod-api)

 
 




 





