from typing import Sequence
from typing import Final

import cv2 as cv
import numpy as np


Mat = np.ndarray
INTERIM_DIR: Final[str] = r"data/interim/"
INTERIM_FILE_SUFFIX: Final[str] = "interim_"
POKEMON_CARD_RESOLUTION: Final[tuple[int, int, int]] = (1505, 2096, 3)
DEFAULT_SIGMA_VALUE: Final[float] = 0.33


def detect_pokemon_card(filepath: str) -> Mat | None:
    """Detects and extracts card from a picture.

    Args:
        filepath (str): path or url of the uploaded image

    Returns:
        Mat | None: a standardized interim card
    """
    img: Mat | None = cv.imread(filepath, cv.IMREAD_UNCHANGED)
    if img is None:
        print(f"Could not read image at {filepath}")
        return None

    if is_back_card(filepath):
        gray_img = cv.split(img)[0]
    else:
        gray_img: Mat = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cleaned_img: Mat = apply_image_corrections(gray_img)
    contours, hierarchy = cv.findContours(
        cleaned_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE
    )

    card_shape, _ = find_card_shape(contours, hierarchy)
    if card_shape.size == 0:
        print("No card found. Exiting.")
        cv.destroyAllWindows()
        return None

    contoured_img = img.copy()
    card_shape = card_shape.reshape((-1, 1, 2)).astype(np.int32)
    cv.drawContours(contoured_img, [card_shape], -1, (0, 255, 0), 2)
    width, height, _ = POKEMON_CARD_RESOLUTION
    sorted_corners = sort_corners(card_shape)

    destination_corners = np.array(
        [[0, 0], [width, 0], [width, height], [0, height]], dtype="float32"
    )

    interim_card = normalize_card(
        img, sorted_corners, destination_corners, width, height
    )

    cv.imshow("Normalized Card", interim_card)
    print("Press any key to close all windows.")
    cv.waitKey(0)
    cv.destroyAllWindows()

    filename: str = (
        INTERIM_DIR + INTERIM_FILE_SUFFIX + filepath.removeprefix("data/raw/")
    )
    cv.imwrite(filename, interim_card)

    return interim_card


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


def apply_sobel(gray_img: Mat) -> Mat:
    sobel_x = cv.Sobel(gray_img, cv.CV_64F, 2, 0, ksize=3)
    sobel_y = cv.Sobel(gray_img, cv.CV_64F, 0, 2, ksize=3)
    gradient_magnitude = cv.magnitude(sobel_x, sobel_y)
    return cv.convertScaleAbs(gradient_magnitude)


def apply_closing(binary_img: Mat) -> Mat:
    """Cleans binary image using Closing (Dilation -> Erosion) technique

    Args:
        binary_img (Mat): binary image to clean

    Returns:
        Mat: cleaned binary image
    """
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    threshold = cv.morphologyEx(binary_img, cv.MORPH_OPEN, kernel, iterations=0)

    return cv.morphologyEx(threshold, cv.MORPH_CLOSE, kernel, iterations=0)


def apply_image_corrections(gray_img: Mat) -> Mat:
    blurred_img: Mat = cv.GaussianBlur(gray_img, (3, 3), 0)
    _, binary_img = cv.threshold(blurred_img, 28, 255, cv.THRESH_BINARY)
    return apply_closing(binary_img)


def normalize_card(
    source_img: Mat,
    sorted_corners: list[Mat],
    destination_corners: Mat,
    width: int,
    height: int,
) -> Mat:
    matrix = cv.getPerspectiveTransform(
        np.array(sorted_corners, dtype="float32"), destination_corners
    )

    return cv.warpPerspective(source_img, matrix, (width, height), flags=cv.INTER_CUBIC)


def create_blank_image(shape: tuple[int, int, int], dtype=np.uint8) -> Mat:
    """Creates a blank image from shape and data type

    Args:
        shape (tuple[int, int, int]): shape of the image
        dtype (_type_, optional): data type. Defaults to np.uint8.

    Returns:
        Mat: blank image
    """
    return np.zeros(shape, dtype)


def find_card_shape(contours: Sequence[Mat], hierarchy: Mat) -> tuple[Mat, float]:
    """
    Finds a card by looking for a "nested rectangle" structure.
    It looks for a large 4-sided contour that has another 4-sided contour inside it.
    """
    best_candidate = {"contour": None, "area": 0}

    if hierarchy is None:
        return np.array([]), 0.0

    for contour in contours:
        area = cv.contourArea(contour)

        if area > 10000:
            hull = cv.convexHull(contour)
            peri = cv.arcLength(hull, True)
            approx_parent = cv.approxPolyDP(contour, 0.01 * peri, True)

            if len(approx_parent) == 4:
                best_candidate["contour"] = contour
                best_candidate["area"] = area
            else:
                print("This contour is not a card")

    if best_candidate["contour"] is None:
        return np.array([]), 0.0

    rect = cv.minAreaRect(best_candidate["contour"])
    box = cv.boxPoints(rect)

    return box, best_candidate["area"]


def sort_corners(shape: Mat) -> list[Mat]:
    points = shape.reshape(4, 2)
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1)

    top_left = np.argmin(sums)
    bottom_right = np.argmax(sums)
    top_right = np.argmin(diffs)
    bottom_left = np.argmax(diffs)

    return [
        points[top_left],
        points[top_right],
        points[bottom_right],
        points[bottom_left],
    ]
