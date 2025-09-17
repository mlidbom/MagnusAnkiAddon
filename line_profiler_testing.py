from time import sleep

from manually_copied_in_libraries.line_profiler_py_charm import profile

@profile
def wait() -> None:
    for i in range(2):
        sleep(1)


wait()