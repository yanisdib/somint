from typing import Sequence
import cv2 as cv
import numpy as np


POKEMON_CARD_RESOLUTION: tuple[int, int, int] = (1505, 2096, 3)
DEFAULT_SIGMA_VALUE: float = 0.33
Mat = np.ndarray


def detect_pokemon_card(filepath: str) -> Mat | None:
    """Detects a Pokémon card from a picture

    Args:
        filepath (str): _description_

    Returns:
        Mat | None: _description_
    """
    img: Mat | None = cv.imread(filepath)
    if img is None:
        print(f"Could not read image at {filepath}")
        return None

    if is_back_card(filepath):
        blue, _, _ = cv.split(img)
        gray_img = blue
    else:
        gray_img: Mat = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv.imshow("Higher contrast Gray", gray_img)

    blurred_img: Mat = cv.GaussianBlur(gray_img, (5, 5), 0)
    canny_img: Mat = apply_auto_canny(blurred_img)
    kernel: Mat = np.ones((5, 5))
    dilated_img: Mat = cv.dilate(canny_img, kernel, iterations=2)
    eroded_img: Mat = cv.erode(dilated_img, kernel, iterations=1)

    cv.imshow("Clean Thresholded Image", eroded_img)

    contoured_img: Mat = img.copy()
    contours, hierarchy = cv.findContours(
        eroded_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )
    cv.drawContours(contoured_img, contours, -1, (0, 255, 0), 5)

    # TODO: Continue instructions
    card_frame: Mat = img.copy()
    processed_img: Mat = create_blank_image(POKEMON_CARD_RESOLUTION)
    corners, max_area = find_card_contour(contours)

    cv.imshow("Contoured Card", contoured_img)
    cv.waitKey(0)

    return None


def apply_auto_canny(img: Mat, sigma: float = 0.33):
    """Applies automatic edge detection

    Args:
        img (Mat): target image
        sigma (float, optional): quantifier. Defaults to 0.33.

    Returns:
        _type_: _description_
    """
    median_value = np.median(img)
    lower: float = int(min(255, (1.0 + sigma) * median_value))
    higher: float = int(max(0, (1.0 - sigma) * median_value))
    return cv.Canny(img, lower, higher)


def is_back_card(filename: str) -> bool:
    """Detect if the current image is a back shot of the current evaluated card.
    This is particularly needed because non japanese cards have a blue background
    which makes it more difficult to detect edges and contours.

    Args:
        filename (str): path or url of the card picture

    Returns:
        bool: whether is the card's back or not
    """
    return filename.__contains__("back")


def create_blank_image(shape: tuple[int, int, int], dtype=np.uint8) -> Mat:
    """Creates a blank image from shape and data type

    Args:
        shape (tuple[int, int, int]): shape of the image
        dtype (_type_, optional): data type. Defaults to np.uint8.

    Returns:
        Mat: blank image
    """
    return np.zeros(shape, dtype)


def find_card_contour(contours: Sequence[Mat]) -> tuple[Mat, float]:
    biggest = Mat([])
    max_area: float = 0

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 5000:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    return biggest, max_area
