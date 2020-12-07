def detectFacesByGoogleVisionAPIFromF(localFilePath, bucket, dirPathOut):
    try:
        keyFile = "service-account-key.json"
        scope = ["https://www.googleapis.com/auth/cloud-vision"]
        api_name = "vision"
        api_version = "v1"
        service = getGoogleService(keyFile, scope, api_name, api_version)

        ctxt = None
        with open(localFilePath, 'rb') as f:
            ctxt = b64encode(f.read()).decode()

        service_request = service.images().annotate(body={
            "requests": [{
                "image":{
                    "content": ctxt
                  },
                "features": [
                    {
                        "type": "FACE_DETECTION"
                    }, 
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }]
        })
        response = service_request.execute()

    except Exception as e:
        logger.exception(e)

def getGoogleService(keyFile, scope, api_name, api_version):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyFile, scopes=scope)
    return build(api_name, api_version, credentials=credentials, cache_discovery=False) 