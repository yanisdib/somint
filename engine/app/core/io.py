import cv2
import numpy as np
import logging


from typing import Optional

RECTIFIED_IMG_FILENAME_PREFIX = "rectified_card_"
INPUT_DIR_PATH = "data/00_raw"
RECTIFIED_OUTPUT_DIR_PATH = "data/01_rectified"


def read_image_bgr(path: str) -> Optional[np.ndarray]:
    """
    Read an image from a file path or URL in BGR format using OpenCV.
    This function handles both local file paths and URLs.
    Args:
        path (str): The file path or URL of the image to read.
    Returns:
        numpy.ndarray: The image in BGR format.
    Raises:
        ValueError: If the image cannot be read from the given path or URL.
    """

    logging.debug(f"Trying to read image from URL/path: {path}")

    try:
        image_bgr = cv2.imread(path)
    except Exception as e:
        logging.error(f"Error reading image from {path}: {e}")
        return None

    if image_bgr is None:
        logging.error(
            f"Failed to read image from {path}. The file may not exist or is not a valid image."
        )
        return None

    return image_bgr


def save_rectified_image(img: np.ndarray, filename: str) -> None:
    cv2.imwrite(filename, img)
    logging.info(f"Rectified image saved as {filename}")
