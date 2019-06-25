import numpy as np
import cv2


class Camera:

    def __init__(self, K, rvec, tvec, dist_coef, w, h):
        """
        :param K: [3x3]
        :param rvec: [3x1]
        :param tvec: [3x1]
        :param dist_coef: [5x1]
        :param w: int
        :param h: int
        """
        self.K = np.array(K)
        self.rvec = np.array(rvec)
        self.tvec = np.array(tvec)
        self.dist_coef = np.array(dist_coef)
        self.w = w
        self.h = h

        # -- P --
        R = cv2.Rodrigues(self.rvec)[0]
        Rt = np.zeros((3, 4))
        Rt[:, 0:3] = R
        Rt[:, 3] = self.tvec
        self.P = self.K @ Rt

        # -- location --
        self.pos = -np.transpose(R) @ tvec

    
    def location(self):
        """ return the camera position in world coordinates
        """
        return self.pos

    
    def project_points(self, points3d):
        """
        :param points3d: [n x 3]
        """
        points3d = np.array(points3d, dtype=np.float64)
        if len(points3d.shape) == 1:
            points3d = np.expand_dims(points3d, axis=0)
        pts2d, _ = cv2.projectPoints(points3d, self.rvec, self.tvec, self.K, self.dist_coef)

        pts2d = np.squeeze(pts2d)
        if len(pts2d.shape) == 1:
            pts2d = np.expand_dims(pts2d, axis=0)

        return pts2d
