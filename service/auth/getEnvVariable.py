from dotenv import load_dotenv
import os

def getAuthConfig(envName):
    load_dotenv()
    envValue = None
    try:
        envValue = os.getenv(envName)
    except:
        # should replace with serverLog
        print(f'get env variable {envName} error')
    finally:
        return envValue