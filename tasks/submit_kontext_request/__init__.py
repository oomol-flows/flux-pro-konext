#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_url: str
    prompt: str
class Outputs(typing.TypedDict):
    request_id: typing.NotRequired[str]
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """Submit an image processing request to fal-flux-pro-kontext API"""

    image_url = params["image_url"]
    prompt = params["prompt"]

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    # Prepare request
    url = "https://fusion-api.oomol.com/v1/fal-flux-pro-kontext/submit"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "imageURL": image_url,
        "prompt": prompt
    }

    # Submit request
    response = requests.post(url, json=payload, headers=headers)

    # Handle errors with detailed message
    if not response.ok:
        try:
            error_detail = response.json()
        except:
            error_detail = response.text
        raise RuntimeError(f"API request failed with status {response.status_code}: {error_detail}")

    response.raise_for_status()

    # Extract request ID from response
    result = response.json()
    request_id = result.get("sessionID") or result.get("request_id") or result.get("requestId") or result.get("id")

    if not request_id:
        raise ValueError(f"No request ID found in response: {result}")

    return {"request_id": request_id}
