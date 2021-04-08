import cv2
import cv2.aruco
import numpy as np
from imutils.object_detection import non_max_suppression


image = cv2.imread('badminton-template.png')

# Test image
# image = cv2.imread('badminton-test-clean.png')
template = cv2.imread('badminton-test-cross.png')

# # Resize the image
# scale_percent = 50 # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
#
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()

(corners, ids, rejected) = cv2.aruco.detectMarkers(image, dictionary=arucoDict, parameters=arucoParams)


originalpts = {}
# verify *at least* one ArUco marker was detected
if len(corners) > 0:
    # flatten the ArUco IDs list
    ids = ids.flatten()
    # loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        print(markerID)
        print('topLeft', 'topRight', 'bottomRight', 'bottomLeft')
        print(topLeft, topRight, bottomRight, bottomLeft)

        # We use the bottomright of each marker to compute homography
        originalpts[markerID] = bottomRight

        # draw the bounding box of the ArUCo detection
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the ArUco
        # marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

        # draw the ArUco marker ID on the image
        cv2.putText(image, str(markerID),
                    (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
# print(originalpts)
sorted_originalpts = []
for id in sorted(originalpts):
    sorted_originalpts.append(originalpts[id])

sorted_originalpts = np.array(sorted_originalpts)
# print(sorted_originalpts)

# convert both the image and template to grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)


# ### Single template matching
# result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)
#
# # determine the starting and ending (x, y)-coordinates of the
# # bounding box
# (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
#
# (startX, startY) = maxLoc
# endX = startX + template.shape[1]
# endY = startY + template.shape[0]
#
# # draw the bounding box on the image
# cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)
#
# ###

# ### Multi-template matching
# # template = cv2.imread(temp)
# templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#
# result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)
#
# (tH, tW) = template.shape[:2]
#
# # find all locations in the result map where the matched value is
# # greater than the threshold, then clone our original image so we
# # can draw on it
# (yCoords, xCoords) = np.where(result >= 0.7)
# clone = image.copy()
# print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
# print(yCoords)
# print(xCoords)
# # loop over our starting (x, y)-coordinates
# for (x, y) in zip(xCoords, yCoords):
#     # draw the bounding box on the image
#     cv2.rectangle(clone, (x, y), (x + tW, y + tH),
#         (255, 0, 0), 3)
#
# # show our output image *before* applying non-maxima suppression
# # cv2.imshow("Before NMS", clone)
# # cv2.waitKey(0)
#
# # initialize our list of rectangles
# rects = []
# # loop over the starting (x, y)-coordinates again
# for (x, y) in zip(xCoords, yCoords):
#     # update our list of rectangles
#     rects.append((x, y, x + tW, y + tH))
# # apply non-maxima suppression to the rectangles
# pick = non_max_suppression(np.array(rects))
# print(pick)
# print("[INFO] {} matched locations *after* NMS".format(len(pick)))
# # loop over the final bounding boxes
# for (startX, startY, endX, endY) in pick:
#     # draw the bounding box on the image
#     cv2.rectangle(image, (startX, startY), (endX, endY),
#         (255, 0, 0), 3)
#
# # show the output image
# # cv2.imshow("After NMS", image)
# # cv2.waitKey(0)
#
#
# scale_percent = 70  # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
#
# resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
# print("[INFO] ArUco marker ID: {}".format(markerID))
#
# # show the output image
# cv2.imshow("Image", resized)
# cv2.waitKey(0)
#
# cv2.imwrite('badminton-test-output.png', resized)


def matchingwithmultitemplates():
    # Read image to be processed
    image = cv2.imread('badminton-test-clean.png')
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Process the markers in the new image
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, dictionary=arucoDict, parameters=arucoParams)

    newpts = {}
    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            print(markerID)
            print('topLeft', 'topRight', 'bottomRight', 'bottomLeft')
            print(topLeft, topRight, bottomRight, bottomLeft)

            # We use the bottomright of each marker to compute homography
            newpts[markerID] = bottomRight

            # draw the bounding box of the ArUCo detection
            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

            # draw the ArUco marker ID on the image
            cv2.putText(image, str(markerID),
                        (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
    # print(newpts)
    sorted_newpts = []
    for id in sorted(newpts):
        sorted_newpts.append(newpts[id])

    sorted_newpts = np.array(sorted_newpts)
    # print(sorted_newpts)

    templateslist = ['badminton-test-cross.png', 'badminton-test-cross-2.png']
    rects = []
    for temp in templateslist:
        template = cv2.imread(temp)
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)

        (tH, tW) = template.shape[:2]

        # find all locations in the result map where the matched value is
        # greater than the threshold, then clone our original image so we
        # can draw on it
        (yCoords, xCoords) = np.where(result >= 0.7)
        clone = image.copy()
        print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))

        for (x, y) in zip(xCoords, yCoords):
            # update our list of rectangles
            rects.append((x, y, x + tW, y + tH))

    print(len(rects))

    pick = non_max_suppression(np.array(rects))

    print(len(pick))

    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
        # draw the bounding box on the image
        cv2.rectangle(image, (startX, startY), (endX, endY),
            (255, 0, 0), 3)
        cv2.putText(image, f"({startX},{startY})", (startX,startY), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=1, color = (255,0,0))

    # Compute homography
    h, status = cv2.findHomography(sorted_newpts, sorted_originalpts)

    # Calculate new point using homography matrix, h
    point = np.array([[[681,280]]], dtype="float32")
    dst = cv2.perspectiveTransform(point, h)
    print(dst, type(dst))
    original = cv2.imread('badminton-template.png')
    newdst = tuple(dst.reshape(1,-1)[0])
    newdst = (int(newdst[0]),int(newdst[1]))
    cv2.circle(original, newdst, radius=5, color=(255,255,0), thickness=3)

    cv2.imshow('whatever', original)
    cv2.waitKey(0)

    # np.dot(h, np.array([[681,280]]))
    # cv2.perspectiveTransform()

    scale_percent = 60  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    print("[INFO] ArUco marker ID: {}".format(markerID))

    # show the output image
    cv2.imshow("Image", resized)
    cv2.waitKey(0)

matchingwithmultitemplates()



