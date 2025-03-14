import time
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from service.implementation.auto_request_api.logic_auto_request import apis, auto_request_system, keep_db_alive
from logger.logger import Logger


class AutoSchedulerService:
    def __init__(self):
        self.logger = Logger("logger", "all.log").logger
        self.api_scheduler = BackgroundScheduler()
        self.db_scheduler = BackgroundScheduler()


    def scheduler_auto_api_parser(self, apis):
        self.logger.debug("Started api_scheduler")
        try:
            for api in apis:
                self.logger.debug(f"Work with {api['name']} | {api['index']} with frequency {api['frequency']} minutes.")
                self.api_scheduler.add_job(
                    auto_request_system,
                    'interval',
                    minutes=api["frequency"],
                    misfire_grace_time=300,
                    args=[api]
                )

        except Exception as e:
            self.logger.error(f"Error in Api Scheduler /: {str(e)}")


    def scheduler_keep_db_alive(self):
        self.logger.debug("Started db_scheduler")
        try:
            self.db_scheduler.add_job(
                keep_db_alive,
                'interval',
                minutes=1,
                misfire_grace_time=300
            )

        except Exception as e:
            self.logger.error(f"Error in DB Scheduler /: {str(e)}")

    def start(self):
        self.api_scheduler.start()
        self.db_scheduler.start()
        self.logger.debug("Schedulers started.")


    def stop(self):
        self.api_scheduler.shutdown()
        self.db_scheduler.shutdown()
        self.logger.debug("Schedulers stopped.")



if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=5)

    scheduler_service = AutoSchedulerService()

    scheduler_service.scheduler_auto_api_parser(apis)
    scheduler_service.scheduler_keep_db_alive()

    scheduler_service.start()
    try:
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        scheduler_service.stop()
        executor.shutdown(wait=True)

