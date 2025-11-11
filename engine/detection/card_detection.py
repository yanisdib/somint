from typing import Sequence
import cv2 as cv
import numpy as np

POKEMON_CARD_RESOLUTION = (1505, 2096)
Mat = np.ndarray


def find_card(filepath: str) -> Mat | None:
    # TODO: Finetune thresholding for better and adaptive contours detection
    # Current results are not good enough.
    img = cv.imread(filepath)
    if img is None:
        print(f"Could not read image from {filepath}")
        return None

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contours = find_card_contours(gray_img)
    contoured_img = cv.drawContours(img, contours, -1, (0, 0, 255), 2)

    cv.imshow("Original with Contours", contoured_img)
    cv.waitKey(0)

    return None


def find_card_contours(img: Mat) -> Sequence[Mat]:
    thresholds = detect_threshold_values(img)
    canny_img = cv.Canny(img, thresholds[0], thresholds[1])
    contours, _ = cv.findContours(canny_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    return contours


def detect_threshold_values(img: Mat) -> tuple[float, float]:
    threshold, _ = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    high: float = threshold
    low: float = threshold * 0.5

    return (high, low)
