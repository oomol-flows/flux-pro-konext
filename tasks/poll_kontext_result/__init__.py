#region generated meta
import typing
class Inputs(typing.TypedDict):
    request_id: str
    max_attempts: float | None
    poll_interval: float | None
class Outputs(typing.TypedDict):
    image_url: typing.NotRequired[str]
    status: typing.NotRequired[str]
#endregion

from oocana import Context
import requests
import time

async def main(params: Inputs, context: Context) -> Outputs:
    """Poll for the result of a kontext API request"""

    request_id = params["request_id"]
    max_attempts = params.get("max_attempts", 60)
    poll_interval = params.get("poll_interval", 2)

    # Get OOMOL token for authentication
    token = await context.oomol_token()

    # Prepare request
    url = f"https://fusion-api.oomol.com/v1/fal-flux-pro-kontext/result/{request_id}"
    headers = {
        "Authorization": token
    }

    # Poll for result
    for attempt in range(max_attempts):
        # Report progress
        progress = int((attempt / max_attempts) * 100)
        context.report_progress(progress)

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Check if request is successful (has data)
            is_success = result.get("success") == True and "data" in result
            status = result.get("status", "").lower() if "status" in result else ("success" if is_success else "processing")
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # Network error - retry on next iteration
            if attempt < max_attempts - 1:
                time.sleep(poll_interval)
                continue
            else:
                raise RuntimeError(f"Network error after {max_attempts} attempts: {str(e)}")

        # Check if completed: either status is completed/success OR success=True with data
        if status == "completed" or status == "success" or (result.get("success") == True and "data" in result):
            # Try multiple possible locations for the image URL
            image_url = None
            possible_paths = [
                ("result['data']['images'][0]['url']", lambda r: r.get("data", {}).get("images", [{}])[0].get("url") if isinstance(r.get("data"), dict) and isinstance(r.get("data", {}).get("images"), list) and len(r.get("data", {}).get("images", [])) > 0 else None),
                ("result['image_url']", lambda r: r.get("image_url")),
                ("result['imageUrl']", lambda r: r.get("imageUrl")),
                ("result['output']['image_url']", lambda r: r.get("output", {}).get("image_url") if isinstance(r.get("output"), dict) else None),
                ("result['output']['imageUrl']", lambda r: r.get("output", {}).get("imageUrl") if isinstance(r.get("output"), dict) else None),
                ("result['data']['image_url']", lambda r: r.get("data", {}).get("image_url") if isinstance(r.get("data"), dict) else None),
                ("result['data']['imageUrl']", lambda r: r.get("data", {}).get("imageUrl") if isinstance(r.get("data"), dict) else None),
                ("result['output']", lambda r: r.get("output") if isinstance(r.get("output"), str) else None),
                ("result['data']", lambda r: r.get("data") if isinstance(r.get("data"), str) else None),
            ]

            for path_name, extractor in possible_paths:
                try:
                    extracted = extractor(result)
                    if extracted:
                        image_url = extracted
                        break
                except Exception:
                    continue

            if not image_url:
                raise ValueError(f"No image URL found in response: {result}")

            context.report_progress(100)
            return {
                "image_url": image_url,
                "status": status
            }

        # Check if failed
        if status == "failed" or status == "error":
            error_msg = result.get("error") or result.get("message") or "Unknown error"
            raise RuntimeError(f"Request failed with status '{status}': {error_msg}")

        # Wait before next poll
        if attempt < max_attempts - 1:
            time.sleep(poll_interval)

    # Timeout
    raise TimeoutError(f"Request timed out after {max_attempts} attempts")
