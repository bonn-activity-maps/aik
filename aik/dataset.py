from os.path import isdir, isfile, join
from aik.camera import Camera
import json
import cv2


class AIK:

    def __init__(self, dataset_loc):
        """
        :param dataset_loc: dataset location as path
        """
        assert isdir(dataset_loc), dataset_loc
        self.video_loc = join(dataset_loc, 'videos')
        assert isdir(self.video_loc), self.video_loc
        camera_loc = join(dataset_loc, 'cameras')
        assert isdir(camera_loc), camera_loc

        dataset_file = join(dataset_loc, 'dataset.json')
        assert isfile(dataset_file), dataset_file

        dataset = json.load(open(dataset_file))

        if 'image_extension' in dataset:
            self.image_extension = dataset['image_extension']
        else:
            self.image_extension = 'png'

        self.n_cameras = dataset['n_cameras']
        self.scale_to_mm = dataset['scale_to_mm']
        if 'valid_frames' in dataset:
            self.valid_frames = dataset['valid_frames']
        else:
            start_frame = dataset['start_frame']
            end_frame = dataset['end_frame']
            self.valid_frames = list(range(start_frame, end_frame + 1))
        self.valid_frames_lookup = set(self.valid_frames)

        self.frame_camera_lookup = {}
        for cid in range(self.n_cameras):
            cameras_info_json = join(camera_loc, 'camera%02d.json' % cid)
            assert isfile(cameras_info_json), cameras_info_json
            cameras_info = json.load(open(cameras_info_json))
            for cam_json in cameras_info:
                K = cam_json['K']
                rvec = cam_json['rvec']
                tvec = cam_json['tvec']
                dist_coef = cam_json['distCoef']
                w = cam_json['w']
                h = cam_json['h']
                start_frame = cam_json['start_frame']
                end_frame = cam_json['end_frame']
                cam = Camera(K, rvec, tvec, dist_coef, w, h)
                for frame in range(start_frame, end_frame+1):
                    self.frame_camera_lookup[frame, cid] = cam

    def get_frame(self, frame, return_paths=False):
        """ get all images and cams for a given frame
        """
        assert frame in self.valid_frames_lookup, 'non-valid frame:' + str(frame)
        images = []
        cameras = []
        for cid in range(self.n_cameras):
            if return_paths:
                fname = join('camera%02d' % cid, ('frame%09d.' + self.image_extension) % frame)
                fname = join('videos', fname)
                images.append(fname)
            else:
                local_vid_dir = join(self.video_loc, 'camera%02d' % cid)
                im_file = join(local_vid_dir, ('frame%09d.' + self.image_extension) % frame)
                im = cv2.cvtColor(cv2.imread(im_file), cv2.COLOR_BGR2RGB)
                images.append(im)
            cam = self.frame_camera_lookup[frame, cid]
            cameras.append(cam)
        return images, cameras
