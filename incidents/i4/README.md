Need to auto-migitate writer when DB gets updated.

Log:
```
October 23rd 2020, 7:48:10 am UTC Backing up DB instance
October 23rd 2020, 7:49:53 am UTC Finished DB Instance backup
October 23rd 2020, 7:53:13 am UTC DB instance shutdown
October 23rd 2020, 7:53:40 am UTC DB instance restarted
October 23rd 2020, 7:55:05 am UTC Database instance patched
```


![failure](https://raw.githubusercontent.com/alevchuk/minibank/first/incidents/i4/Screen%20Shot%202020-10-23%20at%209.34.37%20AM.png)


```
Rescheduling lner.tasks.run_many
Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.AdminShutdown: terminating connection due to administrator command
SSL connection has been closed unexpectedly


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 43, in bg_runner
    func(*args, **kwargs)
  File "/home/writer-www/ln-central/writer/project-basedir/lner/tasks.py", line 764, in run_many
    for node in node_list:
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/query.py", line 274, in __iter__
    self._fetch_all()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/query.py", line 1242, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/query.py", line 55, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1133, in execute_sql
    cursor.execute(sql, params)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 76, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.OperationalError: terminating connection due to administrator command
SSL connection has been closed unexpectedly

Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.AdminShutdown: terminating connection due to administrator command
SSL connection has been closed unexpectedly


```
