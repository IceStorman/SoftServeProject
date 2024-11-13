import time
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from logic_auto_request import apis, auto_request_system

scheduler = BackgroundScheduler()
executor = ThreadPoolExecutor(max_workers=3)

for api in apis:
    print(f"Додаємо завдання для {api['name']}, |||  {api['index']} з частотою {api['frequency']} хвилин.")
    scheduler.add_job(
        auto_request_system,
        'interval',
        minutes=api["frequency"],
        misfire_grace_time=300,
        args = [api]
    )

if __name__ == "__main__":
    scheduler.start()
    print("Планувальник запущено. Натисніть Ctrl+C для зупинки.")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        executor.shutdown(wait=True)
        print("Планувальник зупинено.")

