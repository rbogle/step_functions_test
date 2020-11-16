import boto3
import json
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def state_handler(event, context):
    logger.info("event: %s", event)
    payload = event.get('Payload',event)
    logger.info("payload: %s", payload)
    state = payload.get('state', None)
    lstate = payload.get('last_state', None)
    uuid = payload.get("uuid")
    if lstate != state:
        payload['message']=f"State Changed from {lstate} to {state}"
    return payload

def factory_handler(event, context):
    logger.info("event: %s", event)
    payload = event.get('Payload', event)
    logger.info("payload: %s", payload)
    action = payload.get('action', "CREATE")
    uuid = payload.get("uuid")
    payload['last_state'] = payload.get('state', None)
    if action == "POLL":
        payload['create_account_poll']=payload.get("create_account_poll",0)+1
        payload['state'] = random.choices(["PENDING", "READY"], [.9,.1])[0]
    elif action == "CREATE":
        payload['state'] = "CREATING"
        payload['action'] = "POLL"

    logger.info("output %s",payload)
    return payload

def config_handler(event, context):
    logger.info("event: %s", event)
    payload = event.get('Payload',event)
    logger.info("payload: %s", payload)
    action = payload.get('action', "CONFIG")
    uuid = payload.get("uuid")
    payload['last_state'] = payload.get('state')
    if action == "POLL":
        payload['config_account_poll']=payload.get("config_account_poll",0)+1
        payload['state']= random.choices(["PENDING", "READY"], [.9,.1])[0]
    elif action == "CONFIG":
        payload['state'] = "CONFIGURING"
        payload['action'] = "POLL"

    logger.info("payload %s",payload)
    return payload