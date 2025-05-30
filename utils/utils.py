# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import random

import cv2
import numpy as np
import torch
import torch.nn.functional as F

# set printoptions
torch.set_printoptions(linewidth=320, precision=5, profile="long")
np.set_printoptions(linewidth=320, formatter={"float_kind": "{:11.5g}".format})  # format short g, %precision=5


def load_classes(path):
    """Loads class labels at 'path'."""
    fp = open(path)
    return fp.read().split("\n")[:-1]


def modelinfo(model):
    """Displays model layer details including name, gradient status, number of parameters, shape, mean, and standard
    deviation.
    """
    nparams = sum(x.numel() for x in model.parameters())
    ngradients = sum(x.numel() for x in model.parameters() if x.requires_grad)
    print("\n%4s %70s %9s %12s %20s %12s %12s" % ("", "name", "gradient", "parameters", "shape", "mu", "sigma"))
    for i, (name, p) in enumerate(model.named_parameters()):
        name = name.replace("module_list.", "")
        print(
            "%4g %70s %9s %12g %20s %12g %12g" % (i, name, p.requires_grad, p.numel(), list(p.shape), p.mean(), p.std())
        )
    print(f"\n{i + 1:g} layers, {nparams:g} parameters, {ngradients:g} gradients")


def xview_class2name(classes):
    """Converts an xView class index to its corresponding name by reading from 'data/xview.names' file."""
    with open("data/xview.names") as f:
        x = f.readlines()
    return x[classes].replace("\n", "")


def xview_indices2classes(indices):  # remap xview classes 11-94 to 0-61
    """Remaps xView class indices from 11-94 to 0-61."""
    class_list = [
        11,
        12,
        13,
        15,
        17,
        18,
        19,
        20,
        21,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        40,
        41,
        42,
        44,
        45,
        47,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        66,
        71,
        72,
        73,
        74,
        76,
        77,
        79,
        83,
        84,
        86,
        89,
        91,
        93,
        94,
    ]
    return class_list[indices]


def xview_class_weights(indices):  # weights of each class in the training set, normalized to mu = 1
    """Returns normalized class weights for given indices in the xView dataset using torch.FloatTensor."""
    weights = 1 / torch.FloatTensor(
        [
            74,
            364,
            713,
            71,
            2925,
            209767,
            6925,
            1101,
            3612,
            12134,
            5871,
            3640,
            860,
            4062,
            895,
            149,
            174,
            17,
            1624,
            1846,
            125,
            122,
            124,
            662,
            1452,
            697,
            222,
            190,
            786,
            200,
            450,
            295,
            79,
            205,
            156,
            181,
            70,
            64,
            337,
            1352,
            336,
            78,
            628,
            841,
            287,
            83,
            702,
            1177,
            313865,
            195,
            1081,
            882,
            1059,
            4175,
            123,
            1700,
            2317,
            1579,
            368,
            85,
        ]
    )
    weights /= weights.sum()
    return weights[indices]


def xview_feedback_weights(indices):
    """Calculate normalization weights for given xView feedback indices using pre-defined values."""
    weights = 1 / torch.FloatTensor(
        [
            0,
            0.175,
            0.72,
            1.0,
            0.0441,
            0.486,
            0.168,
            0.0233,
            0.0304,
            0.0177,
            0.087,
            0.209,
            0.0308,
            0.103,
            0.0927,
            0.269,
            0.285,
            0,
            0.294,
            0.675,
            0,
            0.505,
            0.456,
            0.0557,
            0.157,
            0,
            0.621,
            0.24,
            0.222,
            0.222,
            0.145,
            0.0417,
            0.429,
            0.0606,
            0.025,
            0,
            0.547,
            0.531,
            0.00133,
            0.194,
            0.547,
            0.355,
            0.17,
            0.143,
            0.233,
            0.121,
            0.00567,
            0.0208,
            0.517,
            0.0184,
            0.0255,
            0.0191,
            0.0813,
            0.039,
            0.233,
            0.283,
            0.0904,
            0.0745,
            0.402,
            0,
        ]
    )
    weights = torch.clamp(weights, 0, 500)
    weights /= weights.max()
    return weights[indices]


def plot_one_box(x, im, color=None, label=None, line_thickness=None):
    """Draws a bounding box with optional label on an image using specified coordinates, color, and line thickness."""
    tl = line_thickness or round(0.003 * max(im.shape[:2]))
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1)  # filled
        cv2.putText(im, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def weights_init_normal(m):
    """Initialize the weights of convolutional and batch normalization layers with a normal distribution."""
    classname = m.__class__.__name__
    if classname.find("Conv") != -1:
        torch.nn.init.normal_(m.weight.data, 0.0, 0.03)
    elif classname.find("BatchNorm2d") != -1:
        torch.nn.init.normal_(m.weight.data, 1.0, 0.03)
        torch.nn.init.constant_(m.bias.data, 0.0)


def xyxy2xywh(box):
    """Convert bounding box format from (x1, y1, x2, y2) to (x_center, y_center, width, height)."""
    xywh = np.zeros(box.shape)
    xywh[:, 0] = (box[:, 0] + box[:, 2]) / 2
    xywh[:, 1] = (box[:, 1] + box[:, 3]) / 2
    xywh[:, 2] = box[:, 2] - box[:, 0]
    xywh[:, 3] = box[:, 3] - box[:, 1]
    return xywh


def compute_ap(recall, precision):
    """
    Compute the average precision, given the recall and precision curves.

    Code originally from https://github.com/rbgirshick/py-faster-rcnn.
    # Arguments
        recall:    The recall curve (list).
        precision: The precision curve (list).
    # Returns
        The average precision as computed in py-faster-rcnn.
    """
    # correct AP calculation
    # first append sentinel values at the end
    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([0.0], precision, [0.0]))

    # compute the precision envelope
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    # to calculate area under PR curve, look for points
    # where X axis (recall) changes value
    i = np.where(mrec[1:] != mrec[:-1])[0]

    return np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])


def bbox_iou(box1, box2, x1y1x2y2=True):
    # if len(box1.shape) == 1:
    #    box1 = box1.reshape(1, 4)
    """Returns the IoU of two bounding boxes."""
    if x1y1x2y2:
        # Get the coordinates of bounding boxes
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[:, 0], box1[:, 1], box1[:, 2], box1[:, 3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[:, 0], box2[:, 1], box2[:, 2], box2[:, 3]
    else:
        # Transform from center and width to exact coordinates
        b1_x1, b1_x2 = box1[:, 0] - box1[:, 2] / 2, box1[:, 0] + box1[:, 2] / 2
        b1_y1, b1_y2 = box1[:, 1] - box1[:, 3] / 2, box1[:, 1] + box1[:, 3] / 2
        b2_x1, b2_x2 = box2[:, 0] - box2[:, 2] / 2, box2[:, 0] + box2[:, 2] / 2
        b2_y1, b2_y2 = box2[:, 1] - box2[:, 3] / 2, box2[:, 1] + box2[:, 3] / 2

    # get the coordinates of the intersection rectangle
    inter_rect_x1 = torch.max(b1_x1, b2_x1)
    inter_rect_y1 = torch.max(b1_y1, b2_y1)
    inter_rect_x2 = torch.min(b1_x2, b2_x2)
    inter_rect_y2 = torch.min(b1_y2, b2_y2)
    # Intersection area
    inter_area = torch.clamp(inter_rect_x2 - inter_rect_x1, 0) * torch.clamp(inter_rect_y2 - inter_rect_y1, 0)
    # Union Area
    b1_area = (b1_x2 - b1_x1) * (b1_y2 - b1_y1)
    b2_area = (b2_x2 - b2_x1) * (b2_y2 - b2_y1)

    return inter_area / (b1_area + b2_area - inter_area + 1e-16)


def build_targets(pred_boxes, pred_conf, pred_cls, target, anchor_wh, nA, nC, nG, requestPrecision):
    """Returns nGT, nCorrect, tx, ty, tw, th, tconf, tcls."""
    nB = len(target)  # target.shape[0]
    nT = [len(x) for x in target]  # torch.argmin(target[:, :, 4], 1)  # targets per image
    tx = torch.zeros(nB, nA, nG, nG)  # batch size (4), number of anchors (3), number of grid points (13)
    ty = torch.zeros(nB, nA, nG, nG)
    tw = torch.zeros(nB, nA, nG, nG)
    th = torch.zeros(nB, nA, nG, nG)
    tconf = torch.ByteTensor(nB, nA, nG, nG).fill_(0)
    tcls = torch.ByteTensor(nB, nA, nG, nG, nC).fill_(0)  # nC = number of classes
    TP = torch.ByteTensor(nB, max(nT)).fill_(0)
    FP = torch.ByteTensor(nB, max(nT)).fill_(0)
    FN = torch.ByteTensor(nB, max(nT)).fill_(0)
    TC = torch.ByteTensor(nB, max(nT)).fill_(0)  # target category

    for b in range(nB):
        nTb = nT[b]  # number of targets (measures index of first zero-height target box)
        if nTb == 0:
            continue
        t = target[b]  # target[b, :nTb]
        FN[b, :nTb] = 1

        # Convert to position relative to box
        TC[b, :nTb], gx, gy, gw, gh = t[:, 0].long(), t[:, 1] * nG, t[:, 2] * nG, t[:, 3] * nG, t[:, 4] * nG
        # Get grid box indices and prevent overflows (i.e. 13.01 on 13 anchors)
        gi = torch.clamp(gx.long(), min=0, max=nG - 1)
        gj = torch.clamp(gy.long(), min=0, max=nG - 1)

        # iou of targets-anchors (using wh only)
        box1 = t[:, 3:5] * nG
        # box2 = anchor_grid_wh[:, gj, gi]
        box2 = anchor_wh.unsqueeze(1).repeat(1, nTb, 1)
        inter_area = torch.min(box1, box2).prod(2)
        iou_anch = inter_area / (gw * gh + box2.prod(2) - inter_area + 1e-16)

        # Select best iou_pred and anchor
        iou_anch_best, a = iou_anch.max(0)  # best anchor [0-2] for each target

        # Two targets can not claim the same anchor
        if nTb > 1:
            iou_order = np.argsort(-iou_anch_best)  # best to worst
            # u = torch.cat((gi, gj, a), 0).view(3, -1).numpy()
            # _, first_unique = np.unique(u[:, iou_order], axis=1, return_index=True)  # first unique indices
            u = gi.float() * 0.4361538773074043 + gj.float() * 0.28012496588736746 + a.float() * 0.6627147212460307
            _, first_unique = np.unique(u[iou_order], return_index=True)  # first unique indices
            # print(((np.sort(first_unique) - np.sort(first_unique2)) ** 2).sum())
            i = iou_order[first_unique]
            # best anchor must share significant commonality (iou) with target
            i = i[iou_anch_best[i] > 0.10]
            if len(i) == 0:
                continue

            a, gj, gi, t = a[i], gj[i], gi[i], t[i]
            if len(t.shape) == 1:
                t = t.view(1, 5)
        elif iou_anch_best < 0.10:
            continue
        else:
            i = 0

        tc, gx, gy, gw, gh = t[:, 0].long(), t[:, 1] * nG, t[:, 2] * nG, t[:, 3] * nG, t[:, 4] * nG

        # Coordinates
        tx[b, a, gj, gi] = gx - gi.float()
        ty[b, a, gj, gi] = gy - gj.float()
        # Width and height
        tw[b, a, gj, gi] = torch.sqrt(gw / anchor_wh[a, 0]) / 2
        th[b, a, gj, gi] = torch.sqrt(gh / anchor_wh[a, 1]) / 2

        # One-hot encoding of label
        tcls[b, a, gj, gi, tc] = 1
        tconf[b, a, gj, gi] = 1

        if requestPrecision:
            # predicted classes and confidence
            tb = torch.cat((gx - gw / 2, gy - gh / 2, gx + gw / 2, gy + gh / 2)).view(4, -1).t()  # target boxes
            pcls = torch.argmax(pred_cls[b, a, gj, gi], 1).cpu()
            pconf = torch.sigmoid(pred_conf[b, a, gj, gi]).cpu()
            iou_pred = bbox_iou(tb, pred_boxes[b, a, gj, gi].cpu())

            TP[b, i] = (pconf > 0.99) & (iou_pred > 0.5) & (pcls == tc)
            FP[b, i] = (pconf > 0.99) & (TP[b, i] == 0)  # coordinates or class are wrong
            FN[b, i] = pconf <= 0.99  # confidence score is too low (set to zero)

    return tx, ty, tw, th, tconf, tcls, TP, FP, FN, TC


def non_max_suppression(prediction, conf_thres=0.5, nms_thres=0.4, mat=None, img=None, model2=None, device="cpu"):
    """
    Removes detections with lower object confidence score than 'conf_thres' and performs Non-Maximum Suppression to
    further filter detections.

    Returns detections with shape:
        (x1, y1, x2, y2, object_conf, class_score, class_pred)
    """
    prediction = prediction.cpu()

    output = [None for _ in range(len(prediction))]
    # Filter out confidence scores below threshold
    # Get score and class with highest confidence

    # cross-class NMS ---------------------------------------------
    thresh = 0.8
    radius = 30  # area to search for cross-class ious
    # Gather bbox priors
    srl = 3  # sigma rejection level
    for image_i, pred in enumerate(prediction):
        a = pred.clone()
        a = a[np.argsort(-a[:, 4])]  # sort best to worst
        for i in range(len(a)):
            if i >= len(a) - 1:
                break

            close = (np.abs(a[i, 0] - a[i + 1 :, 0]) < radius) & (np.abs(a[i, 1] - a[i + 1 :, 1]) < radius)
            close = close.nonzero()

            if len(close) > 0:
                close = close + i + 1
                iou = bbox_iou(a[i : i + 1, :4], a[close.squeeze(), :4].reshape(-1, 4), x1y1x2y2=False)
                bad = close[iou > thresh]

                if len(bad) > 0:
                    mask = torch.ones(len(a)).type(torch.ByteTensor)
                    mask[bad] = 0
                    a = a[mask]
        pred = a
        # cross-class NMS ---------------------------------------------

        x, y, w, h = pred[:, 0].numpy(), pred[:, 1].numpy(), pred[:, 2].numpy(), pred[:, 3].numpy()
        a = w * h  # area
        ar = w / (h + 1e-16)  # aspect ratio
        log_w, log_h, log_a, log_ar = np.log(w), np.log(h), np.log(a), np.log(ar)

        # n = len(w)
        # shape_likelihood = np.zeros((n, 60), dtype=np.float32)
        # x = np.concatenate((log_w.reshape(-1, 1), log_h.reshape(-1, 1)), 1)
        # from scipy.stats import multivariate_normal
        # for c in range(60):
        # shape_likelihood[:, c] = multivariate_normal.pdf(x, mean=mat['class_mu'][c, :2], cov=mat['class_cov'][c, :2, :2])

        if model2 is None:
            class_prob, class_pred = torch.max(F.softmax(pred[:, 5:], 1), 1)
        else:
            # Start secondary classification of each chip
            class_prob, class_pred = secondary_class_detection(x, y, w, h, img.copy(), model2, device)
            # for i in range(len(class_prob2)):
            #     if class_prob2[i] > class_prob[i]:
            #         class_pred[i] = class_pred2[i]

        mu = mat["class_mu"][class_pred].T
        sigma = mat["class_sigma"][class_pred].T * srl

        v = ((pred[:, 4] > conf_thres) & (class_prob > 0.3)).numpy()
        v *= (a > 20) & (w > 4) & (h > 4) & (ar < 10) & (ar > 1 / 10)
        v *= (log_w > mu[0] - sigma[0]) & (log_w < mu[0] + sigma[0])
        v *= (log_h > mu[1] - sigma[1]) & (log_h < mu[1] + sigma[1])
        v *= (log_a > mu[2] - sigma[2]) & (log_a < mu[2] + sigma[2])
        v *= (log_ar > mu[3] - sigma[3]) & (log_ar < mu[3] + sigma[3])
        v = v.nonzero()

        pred = pred[v]
        class_prob = class_prob[v]
        class_pred = class_pred[v]
        # x, y, w, h = x[v], y[v], w[v], h[v]

        # If none are remaining => process next image
        nP = pred.shape[0]
        if not nP:
            continue

        # From (center x, center y, width, height) to (x1, y1, x2, y2)
        box_corner = pred.new(nP, 4)
        xy = pred[:, 0:2]
        wh = pred[:, 2:4] / 2
        box_corner[:, 0:2] = xy - wh
        box_corner[:, 2:4] = xy + wh
        pred[:, :4] = box_corner

        # Detections ordered as (x1, y1, x2, y2, obj_conf, class_prob, class_pred)
        detections = torch.cat((pred[:, :5], class_prob.float().unsqueeze(1), class_pred.float().unsqueeze(1)), 1)
        # Iterate through all predicted classes
        unique_labels = detections[:, -1].cpu().unique()
        if prediction.is_cuda:
            unique_labels = unique_labels.cuda()
        for c in unique_labels:
            # Get the detections with the particular class
            detections_class = detections[detections[:, -1] == c]
            # Sort the detections by maximum objectness confidence
            _, conf_sort_index = torch.sort(detections_class[:, 4], descending=True)
            detections_class = detections_class[conf_sort_index]
            # Perform non-maximum suppression
            max_detections = []

            # print(detections_class)
            while detections_class.shape[0]:
                # Get detection with highest confidence and save as max detection
                max_detections.append(detections_class[0].unsqueeze(0))
                # Stop if we're at the last detection
                if len(detections_class) == 1:
                    break
                # Get the IOUs for all boxes with lower confidence
                ious = bbox_iou(max_detections[-1], detections_class[1:])

                # Remove detections with IoU >= NMS threshold
                detections_class = detections_class[1:][ious < nms_thres]

            max_detections = torch.cat(max_detections).data
            # print(max_detections)
            # Add max detections to outputs
            output[image_i] = (
                max_detections if output[image_i] is None else torch.cat((output[image_i], max_detections))
            )

            # # NMS2
            # for c in unique_labels:
            #     # Get the detections with the particular class
            #     detections_class = detections[detections[:, -1] == c]
            #     # Sort the detections by maximum objectness confidence
            #     _, conf_sort_index = torch.sort(detections_class[:, 4], descending=True)
            #     detections_class = detections_class[conf_sort_index]
            #     # Perform non-maximum suppression
            #     max_detections = []
            #
            #     while detections_class.shape[0]:
            #         if len(detections_class) == 1:
            #             break
            #
            #         ious = bbox_iou(detections_class[0:1], detections_class[1:])
            #
            #         if ious.max() > 0.5:
            #             max_detections.append(detections_class[0].unsqueeze(0))
            #
            #         # Remove detections with IoU >= NMS threshold
            #         detections_class = detections_class[1:][ious < nms_thres]
            #
            #     if len(max_detections) > 0:
            #         max_detections = torch.cat(max_detections).data
            #         # Add max detections to outputs
            #         output[image_i] = max_detections if output[image_i] is None else torch.cat(
            #             (output[image_i], max_detections))

    return output


# @profile
def secondary_class_detection(x, y, w, h, img, model, device):
    """Detect secondary classes from input image chips using a specified model and device, returning class
    predictions.
    """
    img = np.ascontiguousarray(img.transpose([1, 2, 0]))  # torch to cv2
    height = 64

    l = np.round(np.maximum(w, h) + 2) / 2
    x1 = np.maximum(x - l, 1).astype(np.uint16)
    x2 = np.minimum(x + l, img.shape[1]).astype(np.uint16)
    y1 = np.maximum(y - l, 1).astype(np.uint16)
    y2 = np.minimum(y + l, img.shape[0]).astype(np.uint16)

    n = len(x)
    images = [
        cv2.resize(
            img[y1[i] : y2[i], x1[i] : x2[i]],
            (height, height),
            interpolation=cv2.INTER_LINEAR,
        )
        for i in range(n)
    ]
    # # plot
    # images_numpy = images.copy()
    # import matplotlib.pyplot as plt
    # rgb_mean = [60.134, 49.697, 40.746]
    # rgb_std = [29.99, 24.498, 22.046]
    # for i in range(36):
    #     im = images_numpy[i + 300].copy()
    #     for j in range(3):
    #         im[:, :, j] *= rgb_std[j]
    #         im[:, :, j] += rgb_mean[j]
    #
    #     im /= 255
    #     plt.subplot(6, 6, i + 1).imshow(im)

    images = np.stack(images).transpose([0, 3, 1, 2])  # cv2 to pytorch
    images = np.ascontiguousarray(images)
    images = torch.from_numpy(images).to(device)

    with torch.no_grad():
        classes = []
        nB = n // 500 + 1
        for i in range(nB):
            # print(i,nB)
            j0 = int(i * 500)
            j1 = int(min(j0 + 500, n))
            im = images[j0:j1]
            classes.append(model(im).cpu())

        classes = torch.cat(classes, 0)
    return torch.max(F.softmax(classes, 1), 1)


def createChips():
    """Generates image chips from unique images and saves them with labels into an HDF5 file."""
    from sys import platform

    import cv2
    import h5py
    import numpy as np
    import scipy.io

    mat = scipy.io.loadmat("utils/targets_c60.mat")
    unique_images = np.unique(mat["id"])

    height = 64
    full_height = 128
    X, Y = [], []
    for counter, i in enumerate(unique_images):
        print(counter)

        if platform == "darwin":  # macos
            img = cv2.imread(f"/Users/glennjocher/Downloads/DATA/xview/train_images/{i:g}.bmp")
        else:  # gcp
            img = cv2.imread(f"../train_images/{i:g}.bmp")

        for j in np.nonzero(mat["id"] == i)[0]:
            c, x1, y1, x2, y2 = mat["targets"][j]
            x, y, w, h = (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1
            if ((c == 48) | (c == 5)) & (random.random() > 0.1):  # keep only 10% of buildings and cars
                continue

            l = np.round(np.maximum(w, h) * 1.0 + 2) / 2 * (full_height / height)  # square
            lx, ly = l, l

            # lx = np.round(w * 1.4 + 2) / 2 * (full_height / height)  # fitted
            # ly = np.round(h * 1.4 + 2) / 2 * (full_height / height)

            x1 = np.maximum(x - lx, 1).astype(np.uint16)
            x2 = np.minimum(x + lx, img.shape[1]).astype(np.uint16)
            y1 = np.maximum(y - ly, 1).astype(np.uint16)
            y2 = np.minimum(y + ly, img.shape[0]).astype(np.uint16)

            img2 = cv2.resize(img[y1:y2, x1:x2], (full_height, full_height), interpolation=cv2.INTER_LINEAR)

            X.append(img2[np.newaxis])
            Y.append(c)

        # plot
        # import matplotlib.pyplot as plt
        # for j in range(36):
        #     plt.subplot(6, 6, j + 1).imshow(X[-36 + j][0, 32:-32, 32:-32, ::-1])

    X = np.concatenate(X)[:, :, :, ::-1]
    X = torch.from_numpy(np.ascontiguousarray(X))
    Y = torch.from_numpy(np.ascontiguousarray(np.array(Y))).long()

    with h5py.File("chips_0pad_square.h5") as hf:
        hf.create_dataset("X", data=X)
        hf.create_dataset("Y", data=Y)


def plotResults():
    """Plot results from multiple text files for various metrics using matplotlib."""
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(18, 9))
    s = ["x", "y", "w", "h", "conf", "cls", "loss", "prec", "recall"]
    for f in (
        "/Users/glennjocher/Downloads/results650.txt",
        "/Users/glennjocher/Downloads/results_71.txt",
        "/Users/glennjocher/Downloads/results.txt",
        "/Users/glennjocher/Downloads/results (1).txt",
    ):
        results = np.loadtxt(f, usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10]).T
        for i in range(9):
            plt.subplot(2, 5, i + 1)
            plt.plot(results[i, :], marker=".", label=f)
            plt.title(s[i])
        plt.legend()
