import time

import redis
from flask import Flask
from math import sqrt; from itertools import count, islice

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
            return cache.append("primes", number + ",")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_primes():
    try:
        retries = 5
        while True: 
            try:
                return cache.get("primes")
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)
    except:
        return "no primes"

@app.route('/debugging/reset')
def clear():
    cache.delete("primes")
    return "reset cache"


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<numberVar>')
def isPrime(numberVar):
    n = int(numberVar)
    try:
        prime = n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))
        if prime == True:
            store_number(numberVar)
            return '{} is prime'.format(n)
        else:
            return '{} is not prime'.format(n)
    except ValueError:
        return 'ERROR: Value must be a decimal number!'

@app.route('/primesStored/<ignored>')
def primesStored():
    try:
        values = get_primes()
        return values
    except:
        return "No primes are stored!"
    