from flask import Flask
from flask import request
import json
from io import StringIO
import re
import pandas as pd
import os

from anomaly.anomaly import get_anomalous_values

from celery import Celery
from celery.signals import after_setup_logger
from redis import StrictRedis


app = Flask(__name__)

app.config['CELERY_RESULT_BACKEND'] = 'redis://%s:6379/0' % os.environ.get('REDIS_HOST')
app.config['CELERY_BACKEND_URL'] = 'redis://%s:6379/0' % os.environ.get('REDIS_HOST')
celery = Celery(app.name, broker=app.config['CELERY_BACKEND_URL'])
celery.conf.update(app.config)

REDIS_CACHE = StrictRedis(
    host='%s' % os.environ.get('REDIS_HOST'),
    port=6379,
    db=1,
    decode_responses=True)


def bloat2float(x):
    """
    convert to float pairs, return the raw data otherwise
    """

    y = re.search("\((.*),(.*)\)", x).group(1, 2)

    try:
        return float(y[0]), float(y[1])
    except ValueError:
        # log somewhere ...
        return None, None


@celery.task(bind=True)
def wrap_long_task(self, arg):
    """
    The asynchronous decorator
    """

    return get_anomalous_values(arg)

@app.route('/get_anomalous_data', methods=['GET','POST'])
def get_anomalous_data():
    """
    - POST a new submission
    - GET the async response
    """

    # GET
    if not request.get_data():
        task_id = REDIS_CACHE.get("running_task_id")

        if not task_id:
            return '', 202

        task = wrap_long_task.AsyncResult(task_id)
        if task.state == 'SUCCESS':
            REDIS_CACHE.delete("running_task_id")
            return json.dumps(task.result), 200
        elif task.state == 'FAILURE':
            REDIS_CACHE.delete("running_task_id")
            return str(task.traceback), 500
        else:
            return '', 202
    # POST
    else:
        stream = pd.DataFrame([bloat2float(x) for x in StringIO(
             request.get_data().decode('utf-8')).getvalue().split()])

        stream = stream[(pd.to_numeric(stream[0], errors='coerce').notnull()) \
             & (pd.to_numeric(stream[1], errors='coerce').notnull())]

        task = wrap_long_task.apply_async(args=[stream])
        REDIS_CACHE.set("running_task_id", task.id)
        return 'submitted', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)