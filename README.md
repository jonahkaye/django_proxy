### PRIORITIZATION:

**Crucial:**
- Security x
- Authenticate and Authorize x 
- User Management x 
- Request Validation x
- Error Handling
- Rate Limiting x
- Asynch Processing x 
- Unit testing x
- env config x 

**Good but less crucial:**
- deployment
- Endpoint structure x 
- Caching
- Integration testing
- Scalability

**Not crucial:**
- Endpoint versioning
- batch processing
- documentation
- code structure and design

### THINKING and IMPLEMENTATION:
- security is most important. So that means auth, user management, and request val come first. Rate limiting is like on the border here with DDos. Env config is probably here too since poor handling of env variables is security issue.
- the product achieving the objective minimally is the next most imporant. that means error handling, rate limiting, and asynch processing, which as I see it, make up the core of the proxy api


**SECURITY:**
- HTTPS only. Middlewares.py ensures
- I didn't encrypt the database at rest, but once in prod, just a click of a button to configure RDS to encrypt at rest with AWS KMS

**AUTHENTICATION and AUTHORIZATION:**
- Registration with username and password to get API key. 
- 

**USER MANAGEMENT:**
- see models.py

**REQUEST VALIDATION:**
- see validation.py

**ERROR HANDLING:**
- see views.py

**RATE LIMITING:**
- see UserRateThrottle in InferenceProxyView. Set at 100 RPM/user
- see AnonRateThrottle in RegisterView. Set at 20 registrations per minute. Not really sure what this ought to be

**ASYNC PROCESSING:**
- Using celery. Normally, best to have same number of worker processes as CPU cores to limit context overhead switching. But because processes are I/O bound, using gevent makes more sense. Using guncicorn as production wsgi server. 

- the way the task que is designed is that you configure how many asynchronous requests gevent can pass through to the api simaltaneously. That number can be 10 or 10000. I would experiment in more depth and understanding what the capacity of the inference endpoint is in order to determine what to set that number to. 

- gunicorn is also using gevent. I realized by the end that I 


**UNIT TESTING:**
- see tests folder

**ENV CONFIG:**
- .env file loading into settings.py. Very basic. 


**ENDPOINT STRUCTURE:**
- uses django rest framework. stateless, 

### RUNNING things:

**Env setup**
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `cd genhealth`
* `python manage.py makemigrations`
* `python manage.py migrate`

**Run things**

* `cp .env.example .env` and add your API key
* `cd genhealth; gunicorn genhealth.wsgi:application -k gevent --worker-connections 1000`
* `python start_celery.py -A genhealth worker -P gevent -c 10 --loglevel=info`
<!-- --pool=solo -->
* `redis-server`
* `monitor celery tasks with flower: celery -A genhealth flower`

**Test things**
* `./manage.py test`
* `./manage.py test tests.test_rate_limit`

