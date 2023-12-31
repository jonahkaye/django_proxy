### PRIORITIZATION:

**Crucial:**
- Security x
- Authenticate and Authorize x 
- User Management x 
- Request Validation x
- Error Handling x
- Rate Limiting x
- Asynch Processing x 
- Unit testing x
- env config x 

**Good but less crucial:**
- deployment
- Endpoint structure 
- Caching
- Integration testing (a little)
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
- Ideally should be HTTPS only. Middlewares.py enforces that. I got annoyed with using ngrok as a https proxy and so I commented out the middleware in settings.py, but as soon as you moved to prod you would obviously only be sending over https.
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
- Using celery. Normally, best to have same number of worker processes as CPU cores to limit context overhead switching. But because processes are I/O bound, using gevent makes more sense. Using guncicorn as production wsgi server, which is also using gevent.

- the way the task que is designed is that you configure how many asynchronous requests gevent can pass through to the api simaltaneously. That number can be 10 or 10000. I would experiment in more depth and understanding what the capacity of the inference endpoint is in order to determine what to set that number to.  

- I think I realized that I was struggling slightly to understand the latency of the APi endpoint because obviously on the inference end caching has been implemented so it can handle high latency because its just hitting the cache. 

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
* To test the async load handling you need to use an asynch request library and django doesnt support that within 
its testing framekwork. So call:
* `python test_que.py`

