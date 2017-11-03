from googletrans import Translator
import glob2
from multiprocessing import Pool
from bs4 import BeautifulSoup
from time import gmtime, strftime, sleep
 

#Better documentation + check output folder if file already exists, if so skip

html_folder_path = "copenhagen_htmls\\"
output_folder_path = "copenhagen_translated_htmls\\"

def run():
	#html_paths = glob2.glob(html_folder_path + "*.html")
	html_paths = ["copenhagen_htmls\\13.html"]
	p = Pool(5)
	p.map(translator, html_paths)


def translator(html_path):
	try:
		#Sleep to prevent google ip ban
		sleep(1)

		#Initialize class and all_text will contain our translated text
		translator = Translator()
		all_text = []

		#Read HTML file
		output_path = output_folder_path + html_path[len(html_folder_path):]
		file_data = open(html_path, encoding="utf-8").read() #try latin1
		soup = BeautifulSoup(file_data)

		#Translate text
		all_ns = soup.body.findAll(text=True)
		for element in all_ns:
			text = element.string
			text = text.replace(u"\u2026", "")
			text = text.replace(u"\xa0", "") #test for nbsp in latin
			if text:
				all_text.append(text)

		all_text = translator.translate(all_text, dest="en")

		#Replace text in html file
		for i in range(len(all_ns)):
			element = all_ns[i]			
			element.replace_with(all_text[i].text)

		#Save translated html file
		with open(output_path, "wb+") as file:
			file.write(soup.prettify("utf-8"))

	#Catch any errors and append it to a error log file
	except Exception as e:
		with open("translate_log.txt", "a+") as log:
			curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
			log.write(curr_time + "," + html_path + "," + str(e) + "\n")

if __name__ == "__main__":
	run()
	print("Complete")