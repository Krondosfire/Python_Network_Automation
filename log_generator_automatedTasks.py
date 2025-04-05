import logging

logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('Starting network automation task...')
try:
    # Simulate network automation task
    logging.info('Configuring network device...')
    # Code to configure network device goes here
    logging.info('Network device configured successfully.')
except Exception as e:
    logging.error(f'Error occurred: {e}')

    # A script that logs the progress and errors of network automation tasks using Python's logging module.