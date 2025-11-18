# Flux Pro Kontext

AI-powered image transformation using Flux Pro Kontext API for advanced visual content processing and generation.

## Overview

Flux Pro Kontext is a powerful OOMOL package that provides seamless integration with the fal-flux-pro-kontext API. It enables you to transform and enhance images using advanced AI models by simply providing a source image and a descriptive prompt. The package handles the entire workflow from submitting requests to retrieving processed results.

## Features

- **Easy Image Transformation**: Transform images using natural language prompts
- **Asynchronous Processing**: Submit requests and poll for results efficiently
- **Robust Error Handling**: Comprehensive error messages and retry mechanisms
- **Progress Tracking**: Real-time progress updates during result polling
- **Flexible Configuration**: Customizable polling intervals and timeout settings

## Functional Modules

### 1. Submit Kontext Request

This block submits an image processing request to the Flux Pro Kontext API.

**What it does:**
- Takes a source image URL and transformation prompt as input
- Authenticates with the OOMOL platform automatically
- Submits the request to the Flux Pro Kontext API
- Returns a unique request ID for tracking the processing job

**Use case:** Use this block when you want to start an image transformation job. For example, you might provide an image of a landscape and ask the AI to "make it look like a sunset scene" or "add dramatic lighting".

**Inputs:**
- `image_url` (string): URL of the image you want to process
- `prompt` (text): Description of the desired transformation

**Output:**
- `request_id` (string): Unique identifier for tracking the processing job

### 2. Poll Kontext Result

This block retrieves the processed result from a previously submitted request.

**What it does:**
- Monitors the processing status of your image transformation job
- Automatically retries until the result is ready or timeout occurs
- Reports progress during the polling process
- Returns the URL of the processed image when complete

**Use case:** Use this block after submitting a request to wait for and retrieve the transformed image. It handles all the complexity of checking status and waiting for completion.

**Inputs:**
- `request_id` (string): The ID returned from the Submit Kontext Request block
- `max_attempts` (number, optional): Maximum polling attempts before timeout (default: 60)
- `poll_interval` (number, optional): Seconds between each status check (default: 2)

**Outputs:**
- `image_url` (string): URL of the processed/transformed image
- `status` (string): Final status of the request (e.g., "success", "completed")

## Basic Usage

### Simple Workflow

1. **Prepare your image**: Ensure you have a publicly accessible URL for the image you want to transform
2. **Add Submit block**: Use the "Submit Kontext Request" block and provide:
   - Your image URL
   - A descriptive prompt (e.g., "convert to watercolor painting style")
3. **Add Poll block**: Connect the "Poll Kontext Result" block to receive the request ID
4. **Get results**: The poll block will output the URL of your transformed image

### Example Workflow Configuration

Here's how the two blocks work together:

```
[Your Image URL] → [Submit Kontext Request] → [request_id] → [Poll Kontext Result] → [Transformed Image URL]
                   [Your Prompt]                              [Optional Settings]
```

The workflow automatically:
- Authenticates with the OOMOL platform
- Submits your transformation request
- Monitors the processing status
- Returns the final transformed image

## Integration

This package integrates with the `upload-to-cloud` package (v0.0.5) for seamless cloud storage and image URL management.

## Authentication

Authentication is handled automatically through the OOMOL platform. The blocks use the platform's built-in token system, so you don't need to provide API keys manually.

## Error Handling

The package includes robust error handling:
- **Network errors**: Automatic retry with configurable attempts
- **API errors**: Detailed error messages from the service
- **Timeout handling**: Customizable timeout settings
- **Missing data**: Clear validation messages

## Technical Details

### API Endpoints

- **Submit**: `https://fusion-api.oomol.com/v1/fal-flux-pro-kontext/submit`
- **Result**: `https://fusion-api.oomol.com/v1/fal-flux-pro-kontext/result/{request_id}`

### Dependencies

The package uses standard Python libraries:
- `requests`: HTTP client for API communication
- `oocana`: OOMOL platform context and authentication

### Performance

- **Default timeout**: 120 seconds (60 attempts × 2 seconds interval)
- **Configurable polling**: Adjust `max_attempts` and `poll_interval` based on your needs
- **Progress reporting**: Real-time percentage updates during polling

## Installation

This package is installed through the OOMOL platform. The bootstrap script automatically handles dependency installation:

```bash
npm install
poetry install --no-root
```

## Repository

Source code and issue tracking: https://github.com/oomol-flows/flux-konext

## Version

Current version: 0.0.1

## License

Please refer to the repository for license information.
