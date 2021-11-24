from PIL import ImageGrab
import numpy as np
import cv2

def get_from_clipboard():
    if ImageGrab.grabclipboard():
        clip_from_pillow = ImageGrab.grabclipboard()
        return np.array(clip_from_pillow)
    else:
        raise Exception("No image was found on clipboard")

def make_threshold(source_mat, threshold_value=130):
    def to_grayscale(source_mat):
        if len(source_mat.shape) == 3:
            #se for igual 3, significa que possui mais de um canal de cor
            return cv2.cvtColor(source_mat, cv2.COLOR_RGB2GRAY)
        else:
            return source_mat
    
    source_mat = to_grayscale(source_mat)

    _, thresh = cv2.threshold(source_mat, threshold_value, 255, cv2.THRESH_BINARY)
    
    #contando qual cor é prevalecente na threshold
    counts = np.bincount(np.reshape(thresh, (-1)))
    if np.argmax(counts) == 255:
        return thresh
    else:
        _, thresh = cv2.threshold(source_mat, threshold_value, 255, cv2.THRESH_BINARY_INV)
        return thresh


def make_contours(source_mat, min_thresh=170, max_thresh=200):
    canny = cv2.Canny(source_mat, min_thresh, max_thresh)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return (canny, contours)

def resizeCalc(img, limite):
    #https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized
    # espaço para desenhar na tela do gartic é de (473, 815)

    if img.shape[0] <= limite[0] and img.shape[1] <= limite[1]:
        return img
    elif img.shape[0] > limite[0] and img.shape[1] > limite[1]:
        if img.shape[0] > img.shape[1]:
            return image_resize(img, height=limite[0])
        elif img.shape[1] >= img.shape[0]:
            return image_resize(img, width=limite[1])
    elif img.shape[0] > limite[0]:
        return image_resize(img, height=limite[0])
    elif img.shape[1] > limite[1]:
        return image_resize(img, width=limite[1])



if __name__ == "__main__":
    # grey = to_grayscale(get_from_clipboard())
    # image_mean = np.mean(grey)


    # # canny_grey = cv2.Canny(grey, 170, 180)
    # _, thresh_grey = cv2.threshold(grey, 120, 255, cv2.THRESH_BINARY)

    # canny_grey = cv2.Canny(thresh_grey, 170, 200)

    # cv2.imshow("canny_grey", canny_grey)
    thresh_grey = make_threshold(get_from_clipboard())
    thresh_grey = cv2.Canny(thresh_grey, 170, 200)
    contours, hierarchy = cv2.findContours(thresh_grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(hierarchy[0].shape)
    print(len(contours))
    print(contours[5].shape)
    print(contours[5])


    cv2.imshow("thresh_grey", thresh_grey)
    cv2.waitKey()