import concurrent.futures
from terra import settings
from terra.core.utils import ClassHandler
from importlib import import_module


class ExecutorHandler(ClassHandler):
  '''
  The :class:`ExecutorHandler` class gives a single entrypoint to interact with
  the ``concurrent.futures`` executor class.
  '''

  def _connect_backend(self):
    '''
    Loads the executor backend's base module, given either a fully qualified
    compute backend name, or a partial (``terra.executor.{partial}.executor``), and
    then returns a connection to the backend

    Parameters
    ----------
    self._overrite_type : :class:`str`, optional
        If not ``None``, override the name of the backend to load.
    '''

    backend_name = self._overrite_type

    if backend_name is None:
      backend_name = settings.executor.type
    if not backend_name:
      backend_name = 'ThreadPoolExecutor'

    if backend_name == "ThreadPoolExecutor":
      return concurrent.futures.ThreadPoolExecutor
    elif backend_name == "ProcessPoolExecutor":
      return concurrent.futures.ProcessPoolExecutor
    elif backend_name == "CeleryExecutor":
      import celery_executor.executors
      return celery_executor.executors.CeleryExecutor
    else:
      module_name = backend_name.rsplit('.', 1)
      module = import_module(f'{module_name[0]}')
      return getattr(module, module_name[1])


Executor = ExecutorHandler()
'''ExecutorHandler: The executor handler that all services will be interfacing
with when running parallel computation tasks.
'''