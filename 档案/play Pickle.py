import os
import sys
import pickle
import numpy as N
import invoke
from threading import Thread

pixels = " .,`'-~:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"

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
		input("未发现有Plckle文件，播放失败,Enter键退出")
		exit()
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
		video_path = " "
	if Video_path = "":
		video_path = input("输入Plckle文件地址:")
	main(video_path)