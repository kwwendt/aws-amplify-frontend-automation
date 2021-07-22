import boto3
import requests
import argparse

amplify_client = boto3.client('amplify')

def list_apps(app_name):
    apps = amplify_client.list_apps()['apps']
    for app in apps:
        if app['name'] == app_name:
            return app['appId']
    
    return None

def create_app(app_name):
    resp = amplify_client.create_app(name=app_name)
    return resp['app']['appId']

def create_branch(app_id, branch_name):
    try:
        resp = amplify_client.get_branch(appId=app_id, branchName=branch_name)
    except:
        resp = amplify_client.create_branch(appId=app_id, branchName=branch_name)

def create_deployment(app_id, branch_name):
    resp = amplify_client.create_deployment(appId=app_id, branchName=branch_name)
    return resp['jobId'],resp['zipUploadUrl']

def upload_payload(upload_url, deployment_loc):
    f = open(deployment_loc, 'rb')
    headers = {"Content-Type": "application/zip"}
    resp = requests.put(upload_url, data=f.read(), headers=headers)
    print(resp)

def start_deployment(app_id, branch_name, job_id):
    resp = amplify_client.start_deployment(appId=app_id, branchName=branch_name, jobId=job_id)
    return resp['jobSummary']['status']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AWS Amplify App Build Script')
    parser.add_argument('--app-name', help='Amplify App Name', default='amplify-deploy', dest='app_name')
    parser.add_argument('--branch-name', help='Amplify Branch Name', default='main', dest='branch_name')
    parser.add_argument('--dep-loc', help='Deployment package location', default='deployment.zip', dest='dep_loc')
    args = parser.parse_args()

    app_id = list_apps(app_name=args.app_name)
    if app_id is None:
        app_id = create_app(app_name=args.app_name)
    
    create_branch(app_id=app_id, branch_name=args.branch_name)
    job_id, upload_url = create_deployment(app_id=app_id, branch_name=args.branch_name)

    upload_payload(upload_url=upload_url, deployment_loc=args.dep_loc)
    start_deployment(app_id=app_id, branch_name=args.branch_name, job_id=job_id)
