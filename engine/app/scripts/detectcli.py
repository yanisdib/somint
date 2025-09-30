import logging
import cv2
import numpy as np

from typing import Optional
from engine.app.core.io import read_image_bgr


RECTIFIED_IMG_FILENAME_PREFIX = "rectified_card_"
INPUT_DIR_PATH = "data/00_raw"
RECTIFIED_OUTPUT_DIR_PATH = "data/01_rectified"


def rectify_image(img: str) -> Optional[np.ndarray]:
    # Placeholder for image rectification logic
    # This function should implement the actual rectification algorithm
    # TODO: should get image as np.ndarray instead of str to draw contours directly
    # TODO: refactoring needed after implementing the actual rectification logic
    img_origin = read_image_bgr(img)
    if img_origin is not None and isinstance(img_origin, np.ndarray):
        gray_img = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
        assert gray_img is not None, logging.error(
            "Image conversion to grayscale failed."
        )

        logging.info("Image converted to grayscale.")

        _, thresholds = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
        logging.info("Image thresholding applied.")
        cv2.imshow("Thresholded Image", thresholds)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        contours, _ = cv2.findContours(
            thresholds, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        logging.info(f"Found {len(contours)} contours in the image.")

        img_copy = img_origin.copy()
        cnt = contours[4]
        cv2.drawContours(img_copy, [cnt], 0, (0, 255, 0), 3)
        cv2.imshow("Contours", img_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        logging.error("Failed to read image or image is not a valid numpy array.")
    return None


def apply_quad_detection(img: np.ndarray) -> Optional[tuple[bool, np.ndarray]]:
    # Placeholder for quad detection logic
    # This function should implement the actual quad detection algorithm
    logging.info("Quad detection not implemented yet.")
    return None


def apply_perspective_transformation() -> Optional[np.ndarray]:
    # Placeholder for perspective transform logic
    # This function should implement the actual perspective transformation algorithm
    logging.info("Perspective transform not implemented yet.")
    return None
