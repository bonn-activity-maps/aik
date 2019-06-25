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
        self.K = K
        self.rvec = rvec
        self.tvec = tvec
        self.dist_coef = dist_coef
        self.w = w
        self.h = h