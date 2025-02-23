import logging
from PIL import Image
# from io import BytesIO
from fastapi import HTTPException
from google.genai import Client
# from fastapi.responses import FileResponse
from logging_config import setup_logging
from huggingface_hub import InferenceClient

# import os
setup_logging()
logger = logging.getLogger(__name__)


def process_image(client: Client(), file, user_message: str):
    """
    Identifies and describes the content of an image for AI agents using Gemini Flash.

    Args:
        client: Initialized Gemini client.
        file:  Image file-like object (e.g., UploadFile from FastAPI).
        user_message: User query message

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


async def gen_img(client: InferenceClient, prompt: str):
    """
    Generates an image based on a text query using Imagen and returns it as a FileResponse.

    Args:
        :param client : InferenceClient object.
        :param prompt: Text prompt for image generation.

    Returns:
        :return FilePath: Image file path containing the generated image.

    Raises:
        HTTPException: If there's an error generating the image or creating the FileResponse.
    """
    try:
        # output is a PIL.Image object
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        image_path = "agent/generated_images/image.png"
        image.save(image_path)

        return image_path

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during Imagen image generation: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating image with Imagen API: {e}")
