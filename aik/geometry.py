import numpy as np
import cv2


def triangulate(point1, point2, cam1, cam2):
    """ triangulate point1 in cam1 with point2 in cam2
    :param point1: [2,]
    :param point2: [2,]
    """
    point1 = np.expand_dims(point1, axis=1).astype('float64')  # 2 x n
    point2 = np.expand_dims(point2, axis=1).astype('float64')
    P1 = cam1.P
    P2 = cam2.P
    point3d = np.squeeze(cv2.triangulatePoints(P1, P2, point1, point2))  # (4, ) // homogenous
    h = point3d[3]
    point3d = point3d/h
    return point3d[0:3]


def triangulate_multiple(points, cams):
    """ triangulate all points with each other and take the avg point
    :param points: list([ (x,y), (x,y), ...  ])
    :param cams: list([{cam}, {cam}])
    """
    assert len(points) == len(cams), 'number of points and cameras must agree!'
    n_cameras = len(points)
    assert n_cameras >= 2, 'number of cameras must be 1 < but was ' + str(n_cameras)
    pts3d = []
    for cid1 in range(n_cameras-1):
        for cid2 in range(cid1+1, n_cameras):
            cam1 = cams[cid1]
            cam2 = cams[cid2]
            point1 = points[cid1]
            point2 = points[cid2]
            p3d = triangulate(point1, point2, cam1, cam2)
            pts3d.append(p3d)
    pt3d = np.mean(pts3d, axis=0)
    return pt3d


def compute_epiline(point1, cam1, cam2):
    """ computes the epiline ax + by + c = 0
    :param point1: [x, y]
    :param cam1: source camera
    :param cam2: target camera
    """
    point1 = np.array(point1, np.float64)
    if len(point1.shape) == 1:
        point1 = np.expand_dims(point1, axis=0)
    F = get_fundamental_matrix(cam1, cam2)

    epiline = np.squeeze(cv2.computeCorrespondEpilines(point1, 1, F))
    return epiline
    

def get_fundamental_matrix(cam1, cam2):
    """ finds the fundamental matrix between two views
    :param P1: {3x4} projection matrix
    :param P2: {3x4} projection matrix
    :return:
    """
    P1 = cam1.P
    P2 = cam2.P

    points3d = np.array([
        [0, 0, 0],
        [1505, 1493, 1501],
        [300, 300, 0],
        [1200, 0, 1200],
        [0, 0, 1355],
        [1355, 0, 1],
        [999, 999, 1001],
        [1005, 1001, 1000],
        [551, 5, 333],
        [-100, -100, 1005],
        [1004, -100, 531],
        [-999, 5, 33],
        [-1500,-1000, -503],
        [99, -99, 99],
        [-99, 99, 99],
        [99, 99, -99],
        [5, 5, 5],
        [-5, -5, 5],
        [0.5, 0.5, 0.5],
        [0.1, 0.9, 0.8],
        [-0.1, -0.8, -.9]
    ], 'float64')

    points1 = np.zeros((21, 2))
    points2 = np.zeros((21, 2))
    for i, (x, y, z) in enumerate(points3d):
        p3d = np.array([x, y, z, 1])
        a1, b1, c1 = P1 @ p3d
        a2, b2, c2 = P2 @ p3d
        assert c1 != 0 and c2 != 0
        points1[i, 0] = a1 / c1
        points1[i, 1] = b1 / c1
        points2[i, 0] = a2 / c2
        points2[i, 1] = b2 / c2

    F, mask = cv2.findFundamentalMat(
        points1, points2, cv2.FM_8POINT
    )
    return F
