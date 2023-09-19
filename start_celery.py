from gevent import monkey
monkey.patch_all()

from celery.bin.celery import main

if __name__ == '__main__':
    main()