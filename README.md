# TikTok Reversed API – Mobile & Web

### Follow: https://t.me/touchingcode

## Web API

### x-gnarly

1. Obtain the query string using the standard `urllib.parse` library:
> - Use `urlparse()` if you already have a URL with query parameters
> - Use `urlencode()` if your parameters are stored in a dict
2. Encode the request body using `urlencode()`, or pass an empty string if the request has no body
3. Obtain your User-Agent by any available method
4. Call the `get_x_gnarly()` method from `/web/x_gnarly.py`

### x-bogus, verifyFp
- Before using install JavaScript dependencies:

```bash
cd web/js
npm i
```

1. Obtain the full URL including all query parameters
2. Obtain your User-Agent
3. Call the `get_sign_params()` method from `/web/sign_params.py`

## Mobile API

### device_id, install_id

1. Run:
```bash
python register_device/register_device.py
```
> or call the `register_device()` method from the same file in your code


### x-khronos, x-ladon, x-argus, x-gorgon

1. Obtain the query string using the standard `urllib.parse` library:
> - Use `urlparse()` if you already have a URL with query parameters
> - Use `urlencode()` if your parameters are stored in a dict
2. Collect your request headers
3. Call the `sign_headers()` method from `/mobile/sign_headers.py`


## FAQ

### What is `TTEncrypt.java` in `/register_device`?

- Mobile API endpoints are kinda sensitive. The payload used for device registration is encoded using Java modules located in `/register_device/java`. The encoding process relies on `unidbg.jar`, which contains a `TTEncrypt.class`. In some cases, you may need to modify hardcoded values in payload.

- To do that:

1. Update the required values in `TTEncrypt.java`
2. Extract `unidbg.jar` into the same directory
3. Compile the file:
```bash
javac -cp "unidbg.jar" com/bytedance/frameworks/core/encrypt/TTEncrypt.java
```
4. Replace the original `.class` file:
```
com/bytedance/frameworks/core/encrypt/TTEncrypt.class
```
5. Compile `unidbg.jar`

# This project is for educational and research purposes only.
