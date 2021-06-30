## AWS Amplify Frontend Automation
This Python automation script can be included in a CI/CD pipeline to push frontend deployment packages to AWS Amplify.

*NOTE: Do not use this in production without extensive testing. This can be used in dev/test environments or as a reference for other implementations*

### Usage
```
python3 amplify-build.py --app-name "app-name" --branch-name "main" --dep-loc ./deployment.zip
```