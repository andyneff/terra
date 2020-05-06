import os
import logging.handlers
from concurrent.futures import Future, Executor, as_completed

import terra
from terra import settings
from terra.logger import getLogger
logger = getLogger(__name__)


class BaseExecutor(Executor):
  @staticmethod
  def reconfigure_logger(sender, **kwargs):
    # sender is logger in this case
    #
    # The default logging handler is a StreamHandler. This will reconfigure its
    # output stream

    print("SGR - reconfigure logging")

    if settings.terra.zone == 'controller' or settings.terra.zone == 'task_controller':
      log_file = os.path.join(settings.processing_dir,
                              terra.logger._logs.default_log_prefix)

      # if not os.path.samefile(log_file, sender._log_file.name):
      if log_file != sender._log_file.name:
        os.makedirs(settings.processing_dir, exist_ok=True)
        sender._log_file.close()
        sender._log_file = open(log_file, 'a')

  @staticmethod
  def configure_logger(sender, **kwargs):
    # sender is logger in this case

    # ThreadPoolExecutor will work just fine with a normal StreamHandler

    print('SGR - configure logging ' + settings.terra.zone)

    # REVIEW TERRA_IS_CELERY_WORKER may not be needed anymore, now that we have
    # zones. it is in the Justfile and docker-compose.yml

    # Setup log file for use in configure
    sender._log_file = os.path.join(settings.processing_dir,
                                terra.logger._logs.default_log_prefix)
    os.makedirs(settings.processing_dir, exist_ok=True)
    sender._log_file = open(sender._log_file, 'a')

    sender._logging_handler = logging.StreamHandler(stream=sender._log_file)
    handler = sender._logging_handler

    # TODO: ProcessPool - Log server

    # FIXME this is hacky. it requires the executor know it is responsible for
    # creating this variable on the logger
    terra.logger._logs.main_log_handler = handler


class BaseFuture(Future):
  pass
