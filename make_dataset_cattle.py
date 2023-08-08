# line 37 'head' or 'pig_head'
import os
import ipdb
import cv2
import json
from glob import glob

def is_path(path):
	if not os.path.exists(path):
		os.makedirs(path)


def main():
	frames_path = '/media/ubuntu/fb1dbd0d-04b4-4079-8c9f-db84eb5900fd/keymakr_frames/'
	annotations_path = '/media/ubuntu/fb1dbd0d-04b4-4079-8c9f-db84eb5900fd/keymakr_annotations/'
	images_path = '/media/ubuntu/fb1dbd0d-04b4-4079-8c9f-db84eb5900fd/images_raw/'
	labels_path = '/media/ubuntu/fb1dbd0d-04b4-4079-8c9f-db84eb5900fd/labels_raw/'
	is_path(images_path)
	is_path(labels_path)


	head_counter_dict = {}
	frame_counter_dict = {}

	for video in sorted(os.listdir(frames_path)):
		images = sorted(os.listdir(os.path.join(frames_path, video)))
		try:
			json_path = os.path.join(annotations_path, video + '.mp4.json')
			data = json.load(open(json_path))
		except:
			print('except: {}'.format(video))
			if video == 'WH_Ch1_4920_night':
				json_path = os.path.join(annotations_path, video + '_new.mp4.json')
				data = json.load(open(json_path))
			else:
				json_path = os.path.join(annotations_path, video + '.mp4.-1.json')
				data = json.load(open(json_path))	
		# ipdb.set_trace()
		# ipdb.set_trace()
		zero_frame = data[0]
		objects = zero_frame['objects']

		head_counter = 0
		head_list = []
		frame_counter = 0

		if len(objects) > 0:
			# ipdb.set_trace()
			# head_list = [item['nm'] for item in objects if item['type'] == 'head_sheep'] # cattle 'head' sheep 'head_sheep'
			head_list = [item['nm'] for item in objects if item['type'] == 'head'] # cattle 'head' sheep 'head_sheep'
			# ipdb.set_trace()
			head_counter = len(head_list)

			for i, annotation in enumerate(data[1:]):

				if len(annotation['objects']) > 0:
					try:
						image = images[i]
					except:
						ipdb.set_trace()
					name = '_'.join([video, image.split('.')[0]])
					
					# ipdb.set_trace()
					img = cv2.imread(os.path.join(frames_path, video, image))
					width = 960
					height = 540
					img = cv2.resize(img, (width, height))
					# ipdb.set_trace()
					if any([object['nm'] in head_list for object in annotation['objects']]):
						frame_counter += 1
						cv2.imwrite(os.path.join(images_path, name + '.jpg'), img)
					# ipdb.set_trace()
					for object in annotation['objects']:
						# print(object)
						if object['nm'] in head_list: # object['key'] == True
							# ipdb.set_trace() 
							label_txt = open(os.path.join(labels_path, name + '.txt'), 'a')
							# print(object)
							x1 = object['x1']
							y1 = object['y1']
							x2 = object['x2']
							y2 = object['y2']

							x_center = (x2 + x1) / 2  / 2 / width
							y_center = (y2 + y1) / 2 / 2 /height
							w = (x2 - x1) / 2 / width
							h = (y2 - y1) / 2 / height

							label_txt.write('0 {} {} {} {}\n'.format(x_center, y_center, w, h))






					# ipdb.set_trace()

			# ipdb.set_trace()
		head_counter_dict[video] = head_counter
		frame_counter_dict[video] = frame_counter

	print(head_counter_dict)
	print(frame_counter_dict)

	ipdb.set_trace()


if __name__ == '__main__':
	main()