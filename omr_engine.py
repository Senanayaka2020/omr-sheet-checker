import cv2
import numpy as np

def order_points(pts):
    """කොන් 4හි ලක්ෂ්‍ය නිවැරදි පිළිවෙළට (Top-left, Top-right, Bottom-right, Bottom-left) සකසයි."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    """ඇදයට ඇති ඡායාරූපය සෘජුකෝණාස්‍රාකාර ලෙස සකසයි (Perspective Warp)."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def evaluate_sheet(image, master_key):
    """
    OMR Sheet එක scan කර පිළිතුරු සසඳන ප්‍රධාන Function එක.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Sheet Outline Detection
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    doc_cnt = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                doc_cnt = approx
                break

    if doc_cnt is not None:
        warped = four_point_transform(gray, doc_cnt.reshape(4, 2))
        warped_thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    else:
        warped_thresh = thresh

    # [Note: Grid mapping & bubble pixel counter section]
    # ප්‍රශ්න 50 හි අගයන් Evaluate කිරීමේ Logic එක
    student_answers = {}
    correct_count = 0

    # Output Structure
    results = {
        "score": correct_count,
        "total": len(master_key),
        "student_answers": student_answers
    }
    return results
