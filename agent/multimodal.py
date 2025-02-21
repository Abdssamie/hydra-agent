import logging

from google.genai import types, Client
from PIL import Image
# from io import BytesIO
from fastapi import HTTPException
# from fastapi.responses import FileResponse
from logging_config import setup_logging

# import os
setup_logging()
logger = logging.getLogger(__name__)


def process_image(client: Client(), file, user_message: str):
    """
    Identifies and describes the content of an image for AI agents using Gemini Flash.

    Args:
        client: Initialized Gemini client.
        file:  Image file-like object (e.g., UploadFile from FastAPI).

    Returns:
        str: Textual description of the image content.

    Raises:
        HTTPException: If there's an error processing the image or calling the Gemini API.
    """
    try:
        image = Image.open(file.file)  # Access file content via file.file for UploadFile
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Identify everything about the photo so an ai agent that is incapable of processing images can "
                f"understand it fully as if it was processed by it. You are talking to the agent directly."
                f"Here is the user message: {user_message}",
                image
            ]
        )
        # Basic error handling for Gemini API response
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            raise HTTPException(status_code=400,
                                detail=f"Gemini API blocked the request: {response.prompt_feedback.block_reason}")
        if not response.text:
            raise HTTPException(status_code=500, detail="Gemini API returned an empty response.")

        return response.text

    except HTTPException as e:  # Re-raise HTTPExceptions directly
        raise e
    except Exception as e:  # Catch other potential exceptions during API call
        logger.error(f"Error during Gemini image processing: {e}")  # Log error
        raise HTTPException(status_code=500, detail=f"Error processing image with Gemini API: {e}")


async def gen_img(client: Client(), query: str):
    """
    Generates an image based on a text query using Imagen and returns it as a FileResponse.

    Args:
        client: Initialized Gemini client.
        query: Text prompt for image generation.

    Returns:
        FilePath: Image file path containing the generated image.

    Raises:
        HTTPException: If there's an error generating the image or creating the FileResponse.
    """
    try:
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=query,
            config=types.GenerateImageConfig(
                number_of_images=1,
            ),
            aspect_ratio="1.1"
        )
        if not response.generated_images:  # Check if images were generated
            raise HTTPException(status_code=500, detail="Imagen API failed to generate image(s).")

        generated_image = response.generated_images[0]  # Assuming number_of_images=1
        image_path = 'generated_images/ai_generated_image.png'
        generated_image.save(location=image_path)

        # # Determine image format and MIME type (default to PNG if format is unknown)
        # image_format = image.format or "PNG"
        # mime_type = Image.MIME[image_format] if image_format in Image.MIME else "image/png"
        #
        # # Save image to a temporary file (required for FileResponse)
        # temp_image_file = f"temp_image_{os.urandom(8).hex()}.{image_format.lower()}" # Create a unique filename
        # image.save(temp_image_file)

        return image_path

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during Imagen image generation: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating image with Imagen API: {e}")
