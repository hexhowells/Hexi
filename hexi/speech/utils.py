def load_api_key():
    with open("api_key.txt", "r") as apifile:
        api_key = apifile.read()
        return api_key
