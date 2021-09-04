# conn to db "already closed"


```
2021-09-03 07:54:31,040 W [tasks.py:777] Exception in one of the nodes in run_many: terminating connection due to administrator command
SSL connection has been closed unexpectedly

Rescheduling lner.tasks.run_many
Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

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
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1131, in execute_sql
    cursor = self.connection.cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 256, in cursor
    return self._cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

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
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1131, in execute_sql
    cursor = self.connection.cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 256, in cursor
    return self._cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:


Traceback (most recent call last):
  File "./manage.py", line 31, in <module>
    execute_from_command_line(sys.argv)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/core/management/__init__.py", line 375, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/core/management/base.py", line 323, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/core/management/base.py", line 364, in execute
    output = self.handle(*args, **options)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/management/commands/process_tasks.py", line 94, in handle
    if not self._tasks.run_next_task(queue):
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 137, in run_next_task
    return self._runner.run_next_task(self, queue)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 263, in run_next_task
    self.run_task(tasks, task)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 258, in run_task
    tasks.run_task(task)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 134, in run_task
    self._bg_runner(proxy_task, task, *args, **kwargs)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/tasks.py", line 59, in bg_runner
    task.reschedule(t, e, traceback)
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/models.py", line 248, in reschedule
    self.increment_attempts()
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/models.py", line 233, in increment_attempts
    self.save()
  File "/home/writer-www/ln-central/writer/project-basedir/background_task/models.py", line 323, in save
    return super(Task, self).save(*arg, **kw)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/base.py", line 741, in save
    force_update=force_update, update_fields=update_fields)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/base.py", line 779, in save_base
    force_update, using, update_fields,
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/base.py", line 851, in _save_table
    forced_update)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/base.py", line 900, in _do_update
    return filtered._update(values) > 0
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/query.py", line 760, in _update
    return query.get_compiler(self.db).execute_sql(CURSOR)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1462, in execute_sql
    cursor = super().execute_sql(result_type)
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1131, in execute_sql
    cursor = self.connection.cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 256, in cursor
    return self._cursor()
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/utils.py", line 89, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/base/base.py", line 235, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/writer-www/ln-central/writer-env/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 223, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
```
