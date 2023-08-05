from api_test import *
import subprocess
import datetime

def main():
    
    #Trying to get valid token
    access_token = generate_oauth_token_api()

    if access_token is not None:

        #testing response types to get actual and expected responses without pytest
        test_response_types(access_token)
        
        #Testing with pytest framework
        # Some of the pytests assumes that a valid token is generated

        #creates xml report from pytest
        pytest_args = ['-v', '--capture=no', '--disable-warnings', f"--junitxml={os.environ['PATH_TO_PYTEST_XML_LOGS']}"]
        
        #creates txt report from pytest
        result = subprocess.run(['pytest',os.environ['PATH_TO_PYTEST']] + pytest_args, stdout=subprocess.PIPE, text=True)
        with open(os.environ['PATH_TO_PYTEST_LOGS'], 'a') as f:
            f.write(f"Tests run on: {generate_timestamp()}\n\n")
            f.write(result.stdout)
        print("Pytest completed succesfully please refer to pytest_logs to for further information")
    else:
        print("Pytest could not be run because OAuth token could not be generated.")



if __name__ == "__main__":
    main()