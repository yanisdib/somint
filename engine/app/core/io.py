import os
import cv2
import numpy as np
import logging


from typing import Optional


def read_image_bgr(path: str) -> Optional[np.ndarray]:
    """
    Read an image from a file path or URL in grayscale format using OpenCV.
    This function handles both local file paths and URLs.
    Args:
        path (str): The file path or URL of the image to read.
    Returns:
        numpy.ndarray: The image in grayscale format.
    Raises:
        ValueError: If the image cannot be read from the given path or URL.
    """
    logging.debug(f"Trying to read image from URL/path: {path}")

    try:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            logging.error("Image not found or unable to read. Check the path or URL.")
            return None
    except Exception as e:
        logging.error(f"Error reading image from {path}: {e}")
        return None
    return img


def save_image(img: np.ndarray, filename: str, path: str) -> None:
    if path is None:
        try:
            cv2.imwrite(filename, img)
            logging.info(f"Image saved as {filename} in the current directory.")
            return
        except Exception as e:
            logging.error(f"Error saving image to {filename}: {e}")
            return

    if not os.path.exists(path):
        logging.info(f"Output directory {path} does not exist")
        return

    try:
        cv2.imwrite(os.path.join(path, filename), img)
        logging.info(f"Image saved as {filename} in {path}.")
    except Exception as e:
        logging.error(f"Error saving image to {os.path.join(path, filename)}: {e}")
        return
