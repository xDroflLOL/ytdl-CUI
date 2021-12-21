import sys, os, ctypes, pyperclip, traceback, subprocess
from colorama import init, Fore, Back, Style
init(convert=True)
# I could in theory pass those in command line arguments but NOPE, for some reason I can't get that to work. So here you go.
link = pyperclip.paste()
print(f"{Fore.CYAN}Your link: {link}{Style.RESET_ALL}")
print(f"{Fore.CYAN}(A)udio, (V)ideo+Audio, (C)ustom, Change (L)ink:{Style.RESET_ALL}", end="")
choice = input().lower()

try:
	if "l" in choice:
		print(f"{Fore.CYAN}Your link: {Style.RESET_ALL}", end="")
		link = input()
	if "a" in choice:
		print(f"{Fore.CYAN}[Downloading audio at 128kbps...]{Style.RESET_ALL}")
		readable_stream, error = subprocess.Popen(f'youtube-dl --cookies cookies.txt -o "%(uploader)s - %(title)s.%(ext)s" -f 140 {link}', 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	else:
		print(f"{Fore.CYAN}[Grabbing the videos information...]{Style.RESET_ALL}")

		readable_info, error_info = subprocess.Popen(f'youtube-dl --cookies cookies.txt -F {link}', 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

		if error_info:
			if "warning" in error_info.decode('utf-8').lower():
				print(f"{Fore.YELLOW}{error_info.decode('utf-8')}{Style.RESET_ALL}")
			else:
				raise Exception(error_info.decode('utf-8'))

		print(readable_info.decode('utf-8'))
		if "c" in choice:
			print(f"{Fore.CYAN}Your custom parameters (ex. 320+140, put the video parameter first): {Style.RESET_ALL}", end="")
			parameters = input()
			print(f"{Fore.CYAN}[Downloading the video with custom parameters...]{Style.RESET_ALL}")
			readable_stream, error = subprocess.Popen(f'youtube-dl --cookies cookies.txt -o "%(uploader)s - %(title)s.%(ext)s" -f {parameters} {link}', 
				stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		elif "v" in choice:
			print(f"{Fore.CYAN}Your video parameters: {Style.RESET_ALL}", end="")
			parameters = input()
			print(f"{Fore.CYAN}[Downloading the video...]{Style.RESET_ALL}")
			readable_stream, error = subprocess.Popen(f'youtube-dl --cookies cookies.txt -o "%(uploader)s - %(title)s.%(ext)s" -f {parameters}+140 {link}', 
				stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	if error:
		if "warning" in error.decode('utf-8').lower():
			print(f"{Fore.YELLOW}{error.decode('utf-8')}{Style.RESET_ALL}")
		else:
			raise Exception(error.decode('utf-8'))

	ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
	print(f"{Fore.GREEN}[Downloaded! Press enter to quit or type anything else to open the folder your download is in.]{Style.RESET_ALL}")
	choice_folder = input()
	if choice_folder:
		os.startfile(os.getcwd())	

	try:
		os.remove(f"{os.getcwd()}\\cookies.txt")
	except FileNotFoundError:
		pass

except Exception as e:
	print(traceback.format_exc())
	print(f"{Fore.RED}[Task failed! Press enter to quit.]{Style.RESET_ALL}")
	input()
