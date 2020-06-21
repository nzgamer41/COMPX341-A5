import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def store_number(number):
    retries = 5
    while True: 
        try:
            return cache.append("primes", number)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_primes():
    retries = 5
    while True: 
        try:
            return cache.get("primes")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<numberVar>')
def isPrime(numberVar):
    try:
        number = int(numberVar)
        if number > 1:
            for i in range(2, number):
                if (number % i) == 0:
                    return '{} is not prime'.format(number)
                    break
            else:
                store_number(numberVar + ",")
                return '{} is prime'.format(number)

        else:
            return '{} is not prime'.format(number)
    except ValueError:
        return 'ERROR: Value must be a decimal number!'

@app.route('/primesStored')
def primesStored():
    values = get_primes()
    return values
    