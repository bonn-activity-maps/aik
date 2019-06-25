import sys
import json
from os.path import isdir, isfile, join, basename, normpath
from os import makedirs, listdir
from distutils.dir_util import copy_tree
import shutil
from tqdm import tqdm
assert len(sys.argv) == 2

dataset_path = sys.argv[1]
assert isdir(dataset_path), dataset_path

output_dir = basename(normpath(dataset_path))
output_loc = dataset_path[:-len(output_dir)]
output_path = join(output_loc, 'aik_' + output_dir)
if isdir(output_path):
    shutil.rmtree(output_path)
makedirs(output_path)

n_cameras = len(listdir(join(dataset_path, 'videos')))

print('\n===================')
print("converting..")
print('===================')
print("create directory:", output_path)
print("number of cameras:", n_cameras)

print('\tcopy tracks3d....')
tracks3d_src = join(dataset_path, 'tracks3d')
tracks3d_dst = join(output_path, 'tracks3d')
copy_tree(tracks3d_src, tracks3d_dst)

print('\tcopy videos....')
video_dir_src = join(dataset_path, 'videos')
# video_dir_dst = join(output_path, 'videos')
# copy_tree(video_dir_src, video_dir_dst)



print('\nconversion finished\n')
