
import os
import ipdb
from sklearn.model_selection import train_test_split
from collections import defaultdict
import shutil

def is_path(path):
	if not os.path.exists(path):
		os.makedirs(path)

def main():
	images_raw_path = '/media/ubuntu/ubuntu_storage/kewpie/images_raw'
	labels_raw_path = '/media/ubuntu/ubuntu_storage/kewpie/labels_raw'
	images_path = '/media/ubuntu/ubuntu_storage/08jan2023/dataset/images'
	labels_path = '/media/ubuntu/ubuntu_storage/08jan2023/dataset/labels'


	is_path(images_path)
	is_path(labels_path)

	for item in ['train', 'validation']:
		for path in [images_path, labels_path]:
			is_path(os.path.join(path, item))




	images = sorted(os.listdir(images_raw_path))
	# ipdb.set_trace()
	
	images_dict = defaultdict(list)
	for image in images:
		video = image.rsplit('_', 1)[0]
		images_dict[video].append(image)
	# ipdb.set_trace()
	for value in images_dict.values():
		value_train = []
		value_validation = []
		if len(value) > 1 :
		# print('\n')
			value_train, value_validation = train_test_split(value, test_size=0.25, train_size = 0.75, random_state=0)
		else:
			value_train = value
		# ipdb.set_trace()
		for image in value_train:
			txt = image.split('.jpg')[0] + '.txt'
			shutil.copy(os.path.join(images_raw_path, image), os.path.join(images_path, 'train', image))
			shutil.copy(os.path.join(labels_raw_path, txt), os.path.join(labels_path, 'train', txt))

		for image in value_validation:
			txt = image.split('.jpg')[0] + '.txt'
			shutil.copy(os.path.join(images_raw_path, image), os.path.join(images_path, 'validation', image))
			shutil.copy(os.path.join(labels_raw_path, txt), os.path.join(labels_path, 'validation', txt))

	ipdb.set_trace()
	os._exit(0)
	

		




if __name__ == '__main__':
	main()
