import time
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from service.implementation.auto_request_api.logic_auto_request import apis, auto_request_system, keep_db_alive

scheduler1 = BackgroundScheduler()
scheduler2 = BackgroundScheduler()

executor = ThreadPoolExecutor(max_workers=3)

for api in apis:
    print(f"Додаємо завдання для {api['name']}, |||  {api['index']} з частотою {api['frequency']} хвилин.")
    scheduler1.add_job(
        auto_request_system,
        'interval',
        minutes=api["frequency"],
        misfire_grace_time=300,
        args = [api]
    )

scheduler2.add_job(
    keep_db_alive,
    'interval',
    minutes=0.1,
    misfire_grace_time=300
)


if __name__ == "__main__":
    scheduler1.start()
    scheduler2.start()
    print("Schedulers starting work")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler1.shutdown()
        scheduler2.shutdown()
        executor.shutdown(wait=True)
        print("Schedulers shutting down")

