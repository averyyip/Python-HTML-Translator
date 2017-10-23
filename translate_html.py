from googletrans import Translator
import glob2
from multiprocessing import Pool
from bs4 import BeautifulSoup

def run(html_path):
	html_paths = glob2.glob(html_path + "*.html")
	p = Pool(5)
	p.map(translator, html_paths)


def translator(html_path):
	translator = Translator()
	all_text = []
	translated = []
	output_path = output_folder_path + html_path[len(html_folder_path):]
	file_data = open(html_path, encoding="utf-8").read() #try latin1

	soup = BeautifulSoup(file_data)
	all_ns = soup.body.find_all(text=True)

	for element in all_ns:
		text = element.string
		text = text.replace(u"\u2026", "") #for handling weird windows encoding
		if text:
			all_text.append(text)

	translated = translator.translate(all_text, dest=trans_lang)

	for i in range(len(all_ns)):
		element = all_ns[i]
		element.replace_with(translated[i].text)

	with open(output_path, "wb") as file:
		file.write(soup.prettify("utf-8"))

def translate_html(html_folder, output_folder, lang="en"):
	global trans_lang
	trans_lang = lang
	run(html_folder)

if __name__ == "__main__":
	output_path = "copenhagen_translated_htmls\\"
	input_path = "copenhagen_htmls\\"
	translate_html(input_path)
	print("Complete")