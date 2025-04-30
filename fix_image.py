"""
Author: Ryheff24 on discord
"""

import os
import cv2
import numpy as np

input_folder = "images"
output_folder = "outimgs"
os.makedirs(output_folder, exist_ok=True)


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect


for fname in os.listdir(input_folder):
    in_path = os.path.join(input_folder, fname)
    # skip non-images
    if not fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        continue
    img = cv2.imread(in_path)
    if img is None:
        print(f"Failed to load {in_path}, skipping.")
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    blur = cv2.convertScaleAbs(blur, alpha=0.85, beta=0.1)
    _, thresh = cv2.threshold(blur, 80, 200, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_square = None
    max_area = 0
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                largest_square = approx
    overlay = img.copy()
    if largest_square is not None:
        cv2.drawContours(overlay, [largest_square], -1, (0, 255, 0), 3)
    out_overlay = os.path.join(
        output_folder, f"{os.path.splitext(fname)[0]}_overlay.jpg"
    )
    if largest_square is not None:
        pts = largest_square.reshape(4, 2).astype("float32")
        rect = order_points(pts)
        (tl, tr, br, bl) = rect
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = int(max(heightA, heightB))

        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1],
            ],
            dtype="float32",
        )
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        out_warp = os.path.join(
            output_folder, f"{os.path.splitext(fname)[0]}_warped.jpg"
        )
        cv2.imwrite(out_warp, warped)
    else:
        print(f"No quadrilateral found in {fname}, skipping warp.")
