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

### Task Blocks

#### 1. Submit Kontext Request

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

#### 2. Poll Kontext Result

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

### Subflows

Subflows are pre-built workflows that combine multiple task blocks into reusable, simplified interfaces.

#### 1. File Kontext Edit

Upload a local image file and edit it with Flux Pro Kontext AI.

**What it does:**
- Automatically uploads your local image file to cloud storage
- Submits the image transformation request with your prompt
- Polls for the result and downloads the edited image
- Saves the final image to your specified location

**Inputs:**
- `file` (file): Local image file to edit
- `prompt` (text): Editing instructions for the AI model
- `saved_path` (save path, optional): Path to save the edited image

**Output:**
- `saved_path` (string): Path of the successfully downloaded edited image

**Use case:** Perfect for batch processing local images or when working with files on your computer. Simply select an image file, describe how you want it edited, and get the result saved locally.

#### 2. URL Kontext Edit

Edit an online image from URL using Flux Pro Kontext AI.

**What it does:**
- Takes an online image URL directly
- Submits the transformation request
- Polls for the result and returns the edited image URL

**Inputs:**
- `image_url` (string): URL of the image to edit
- `prompt` (text): Editing instructions for the AI model

**Output:**
- `image_url` (string): URL of the edited image

**Use case:** Ideal for processing images already hosted online or when you need to chain multiple transformations. The output URL can be used directly or passed to other workflow blocks.

## Basic Usage

### Quick Start with Subflows (Recommended)

The easiest way to get started is using one of the pre-built subflows:

**For local images:**
1. Add the "File Kontext Edit" subflow to your workflow
2. Select your local image file
3. Enter your transformation prompt (e.g., "make it look like a vintage photograph")
4. (Optional) Choose where to save the result
5. Run the workflow - the edited image will be saved automatically

**For online images:**
1. Add the "URL Kontext Edit" subflow to your workflow
2. Provide the image URL
3. Enter your transformation prompt
4. Run the workflow - get back the URL of the edited image

### Advanced Usage with Task Blocks

For more control, you can build custom workflows using individual task blocks:

1. **Prepare your image**: Ensure you have a publicly accessible URL for the image you want to transform
2. **Add Submit block**: Use the "Submit Kontext Request" block and provide:
   - Your image URL
   - A descriptive prompt (e.g., "convert to watercolor painting style")
3. **Add Poll block**: Connect the "Poll Kontext Result" block to receive the request ID
4. **Get results**: The poll block will output the URL of your transformed image

### Example Workflow Configurations

**Using Subflow (Simple):**
```
[Local Image File] → [File Kontext Edit Subflow] → [Saved Image Path]
[Your Prompt]
```

**Using Task Blocks (Advanced):**
```
[Your Image URL] → [Submit Kontext Request] → [request_id] → [Poll Kontext Result] → [Transformed Image URL]
                   [Your Prompt]                              [Optional Settings]
```

Both approaches automatically:
- Authenticate with the OOMOL platform
- Submit your transformation request
- Monitor the processing status
- Return the final transformed image

## Integration

This package integrates with other OOMOL packages:
- **upload-to-cloud** (v0.0.5): Used in File Kontext Edit subflow for uploading local images to cloud storage
- **downloader** (v0.1.1): Used in File Kontext Edit subflow for downloading the edited image results

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
