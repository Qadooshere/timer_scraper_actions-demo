import datetime
import logging
import requests
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_actions(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # Define the URLs
    trigger_url = "https://google.com"
    processing_url = "https://juh.wesser.info/wp-load.php?import_key=GKlhEzpN&import_id=9&action=processing"

    try:
        # Trigger the import
        trigger_response = requests.get(trigger_url)
        if trigger_response.status_code == 200:
            logging.info("Import trigger URL called successfully.")
        else:
            logging.error(f"Failed to trigger import. Status code: {trigger_response.status_code}")
        
        # Call the processing URL if needed
        processing_response = requests.get(processing_url)
        if processing_response.status_code == 200:
            logging.info("Processing URL called successfully.")
        else:
            logging.error(f"Failed to call processing URL. Status code: {processing_response.status_code}")

    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)



@app.blob_trigger(arg_name="myblob", path="instadataupload/{name}.csv",
                  connection="instascraperstorage_STORAGE") 
def wp_blob_trigger(myblob: func.InputStream):
    
    logging.info(f"Python blob trigger function processed blob"
                 f"Name: {myblob.name}"
                 f"Blob Size: {myblob.length} bytes")
    
    # Define the URLs
    trigger_url = "https://google.com"
    processing_url = "https://juh.wesser.info/wp-load.php?import_key=GKlhEzpN&import_id=8&action=processing"

    try:
        # Trigger the import
        trigger_response = requests.get(trigger_url)
        if trigger_response.status_code == 200:
            logging.info("Blob Import trigger URL called successfully .")
        else:
            logging.error(f"Failed to trigger import in Blob. Status code: {trigger_response.status_code}")
        
        # Call the processing URL if needed
        processing_response = requests.get(processing_url)
        if processing_response.status_code == 200:
            logging.info("Blob Processing URL called successfully.")
        else:
            logging.error(f"Failed to call processing URL inn BLOB. Status code: {processing_response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")