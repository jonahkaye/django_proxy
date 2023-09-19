PRIORITIZATION:

Crucial: 
- Security x
- Authenticate and Authorize x 
- User Management x 
- Request Validation 
- Error Handling
- Rate Limiting
- Asynch Processing
- Unit testing

Good but less crucial:
- deployment
- Scalability
- Integration testing
- Endpoint structure
- Caching

Not crucial :
- Endpoint versioning
- batch processing
- documentation
- env config
- code structure and design

My thinking is this:
- security is most important. So that means auth, user management, and request val come first. 
- the product achieving the objective minimally is the next most imporant. that means error handling, rate limiting, and asynch processing, which as I see it, make up the core of the proxy api
- 



Authentication and Authorization: They need to register and get an API key. Then using django rest DRF framework to auth in. 

Scalability



SECURITY:
- HTTPS only. Middlewares.py ensures
- I didn't encrypt the database at rest, but once in prod, just a click of a button to configure RDS to encrypt at rest with AWS KMS

AUTHENTICATION and AUTHORIZATION:
- Registration with username and password to get API key. 
- 




Using celery. Normally, best to have same number of worker processes as CPU cores to limit context overhead switching. But because processes are I/O bound, using gevent makes more sense. 

Using guncicorn as production wsgi server. 


COMMANDS:
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `cd genhealth; gunicorn genhealth.wsgi:application`
* `python start_celery.py -A genhealth worker -P gevent -c 10 --loglevel=info`
<!-- --pool=solo -->
* `redis-server`
* `monitor celery tasks with flower: celery -A genhealth flower`