import os
import sys
import pickle
import numpy as N
import invoke
from threading import Thread

pixels = " .,`'-~:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"

def Video_to_imgs(Video, size, seconds):
	"""
	param1: 视频文件路径,str	
	param2: 生成图片的尺寸,[H,L]	
	return: img_list
	"""
	import cv2
	
	img_list = []
	picture = cv2.VideoCapture(Video)
	fps = picture.get(cv2.CAP_PROP_FPS)
	frames_count = fps * seconds
	count = 0
	while picture.isOpened() and count < frames_count:
		ret,frame = picture.read()
		"""
		read()
		return: [是否读取到图像, 图像矩阵]
		"""
		if ret:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 转黑白图
			img = cv2.resize(gray, size, interpolation = cv2.INTER_AREA) #调整图片，保证图片可读取且打印
			img_list.append(img) # 保存结果
			count += 1
		else:
			break
			
	picture.release() # 释放空间
	return img_list, fps, int(frames_count)
"""	测试 Video_to_imgs
if __name__ == "__main__":
	imgs = Video_to_imgs("BadApple.mp4", (64, 48))
	assert len(imgs) > 10
"""

def img_to_chars(img, i):
	res = []
	height, width = img.shape
	"""
	param: 图像矩阵
	return: 字符串列表
	"""
	for row in range(height):
		line = ""
		for col in range(width):
			percent = img[row][col] / 255 # 将8位灰度值转换为0-1之间
			index = int(percent * (len(pixels) - 1)) #进一步转换灰度值以匹配字符列表 pixels
			line += pixels[index] + " " # 增加字符间距
		
		res.append(line)
	res.append("")
	i=str(round(i*100,2))+"%  "+"■"*int(i*width*2)  #打印输出进度条
	res.append(i)
	return res

def imgs_to_chars(imgs, frames_count):
	video_chars, i = [], 0
	for img in imgs:
		i += 1
		video_chars.append(img_to_chars(img, i/frames_count))
	return video_chars
"""	测试 imgs_to_chars
if __name__ == "__main__":
	imgs = Video_to_imgs("BadApple.mp4", (64, 48))
	video_chars = imgs_to_chars(imgs)
	assert len(video_chars) > 10
"""

def play_video(video_chars, frame_rate, frames_count):
	import time
	import curses
	width,height = len(video_chars[0][0]), len(video_chars[0]) # 获取文件尺寸

	stdscr = curses.initscr()
	curses.start_color()

	try:

		stdscr.resize(height, width * 2)

		for pic_i in range(len(video_chars)):
			for line_i in range(height): #打印当前帧
				stdscr.addstr(line_i, 0, video_chars[pic_i][line_i], curses.COLOR_WHITE) # 打印显示，并将字符调整为白色
			stdscr.refresh()
			time.sleep(1 / frame_rate)
	finally:
		curses.endwin()
	print("播放完毕")
	return

def dump(obj, file_name):
	with open(file_name, 'wb') as f:
		pickle.dump(obj, f)
	return

def load(filename):
	with open(filename,'rb') as f:
		return pickle.load(f)

def get_file_name(file_path):
	path, file_name_with_extension = os.path.split(file_path)
	file_name, file_extension = os.path.splitext(file_name_with_extension)
	return file_name

def has_file(path, file_name):
	return file_name in os.listdir(path)

def get_video_chars(video_path, size, seconds):
	video_dump = get_file_name(video_path) + ".pickle"
	if has_file(".", video_dump):
		print("正在读取")
		video_chars, fps, frames_count = load(video_dump)
	else:
		print("正在加载，请稍等")
		imgs, fps, frames_count = Video_to_imgs(video_path, size, seconds)
		video_chars = imgs_to_chars(imgs, frames_count)
		dump([video_chars, fps, frames_count], video_dump)
		print("加载完成")
	return video_chars, fps, frames_count


def play_audio(video_path):

	def call(video_path = video_path):
		filename = sys.argv[0]
		dirname = os.path.dirname(filename)
		abspath = os.path.abspath(dirname)
		cmd = "mpv --no-video " + abspath + "\\" + video_path
		invoke.run(cmd, hide=True, warn=True)
	return Thread(target=call)
	
	
	

def main(video_path):
	size = (80,45)  # 输出分辨率  建议是100*100以内，和原视频宽高比相同
	# video_path = "BadApple.mp4"
	seconds = 30
	video_chars, fps, frames_count = get_video_chars(video_path, size, seconds)
	input("开始播放")
	p = play_audio(video_path)
	p.setDaemon(True)
	p.start()
	play_video(video_chars, fps, frames_count)

	
	
	
	
if __name__ == "__main__":
	try:
		video_path = sys.argv[1]
	except:
		video_path = ""
	if Video_path == "":
		video_path = input("输入视频地址:")
	main(video_path)
