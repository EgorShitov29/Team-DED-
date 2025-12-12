import threading
import time

from Model.Orchestrator import Orchestrator


class BotMain:
    """
    Запуск/остановка оркестратора в отдельном потоке.
    """

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        self._thread = None
        self._running = False

    def _run_loop(self) -> None:
        self._running = True
        try:
            self.orchestrator.run()
        finally:
            self._running = False

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.orchestrator.stop()
        # можно дождаться завершения
        if self._thread is not None:
            self._thread.join(timeout=5.0)
