from typing import List
import argparse, os, sys, string, datetime, json
from monsoonToolBox.filetools.files import recursivlyFindFilesByExtension

MARKER = "+==***---------------------------------------------------------***==+"
replace_config = {}

def _splitLine(line: str, n_max: int, keep_word = False) -> List[str]:
	if len(line) <= n_max:
		return [line]
	else:
		if not keep_word:
			line_start = line[:n_max]
			line_follow = line[n_max:]
			return [line_start] + _splitLine(line_follow, n_max)
		# if keep_word, don't split word
		line_split = [l + " " for l in line.split(" ")]
		n_current = 0
		for i in range(len(line_split)):
			l = line_split[i]
			n_current += len(l)
			if n_current < n_max:
				# length not enouth, go to next word
				continue

			if n_current == n_max and l[-1] == ' ':
				# just good, should not happen though...
				return [line[:-1]]
			if i > 0:
				n_needed = 0
				for j in range(i):
					n_needed += len(line_split[j])
			else:
				# i is 0, single long line
				n_needed = n_max
			return [line[:n_needed]] + _splitLine(line[n_needed:], n_max)

		return []	# Should never reach here, for type checking purposes

def _markerPos(content: str) -> List[int]:
	content_split = content.split("\n")
	marker_pos = []
	for i in range(len(content_split)):
		line = content_split[i]
		if line == MARKER:
			marker_pos.append(i)
	return marker_pos

def delHeader(content: str) -> str:
	#  marker_pos = _markerPos(content)
	content_split = content.split("\n")
	marker_pos = []
	for i in range(len(content_split)):
		line = content_split[i]
		if line == wrapLine(MARKER):
			marker_pos.append(i)
	if len(marker_pos) != 2 or marker_pos[0] > 3:
		raise LookupError("Can't find proper header")
	content_split = content_split[:marker_pos[0]] + content_split[marker_pos[1] + 1:]
	return "\n".join(content_split)

def _getHeader(header: str) -> str:
	LINE_HEAD = "|  "
	LINE_TAIL = "  |"
	HEAD_TAIL = LINE_HEAD + LINE_TAIL
	n_max = len(MARKER) - len(HEAD_TAIL)       # maximum characters per line
	assert n_max > 0
	
	header = Replacer(header).config(**replace_config).parse()

	header_split = header.split("\n")
	_aim_split = []
	for line in header_split:
		_aim_split += _splitLine(line, n_max, True)
	
	aim_split = []
	for line in _aim_split:
		n_less = n_max - len(line)
		aim_split.append(LINE_HEAD + line + " "*n_less + LINE_TAIL)
	aim_split = [MARKER] + aim_split + [MARKER]
	aim_split = [ wrapLine(line) for line in aim_split ]
	return "\n".join(aim_split)

def wrapLine(line: str) -> str:
	return "# " + line + " #"

def addHeader(content: str, header: str, config: dict) -> str:
	global replace_config
	replace_config = config
	try:
		content = delHeader(content)
	except LookupError:
		...
	return _getHeader(header) + "\n" + content

class Replacer:
	STAMP_DATE = "DATE"
	STAMP_AUTHOR = "AUTHOR"
	STAMP_REPO = "REPO"
	STAMP_FILENAME = "FILENAME"
	def __init__(self, content: str):
		self.content = string.Template(content)

		self.VAL_AUTHOR = ""
		self.VAL_REPO = ""
		self.VAL_FILENAME = ""
		self.VAL_DATE = ""
	
	def config(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, "VAL_"+k.upper(), v)
		return self
	
	def _date(self):
		if not self.VAL_DATE:
			date = datetime.datetime.now()
			date = date.strftime("%Y-%m-%d")
		else:
			date = self.VAL_DATE
		return date

	def _author(self):
		return self.VAL_AUTHOR

	def _repo(self):
		return self.VAL_REPO

	def _filename(self):
		return self.VAL_FILENAME

	def parse(self):
		return self.content.substitute(
			{
				self.STAMP_DATE: self._date(),
				self.STAMP_AUTHOR: self._author(),
				self.STAMP_REPO: self._repo(),
				self.STAMP_FILENAME: self._filename(),
			}
		)

def main():
	parser = argparse.ArgumentParser("Add header")
	parser.add_argument("input_file")
	parser.add_argument("-d", "--delete", action="store_true")
	parser.add_argument("-c", "--config", type=json.loads, default={})

	args = parser.parse_args()
	aim = args.input_file

	if args.delete:
		header = None
	else:
		header = sys.stdin.read()

	if os.path.isdir(aim):
		py_files = recursivlyFindFilesByExtension(aim, [".py"])
	else:
		assert aim.endswith(".py")
		py_files = [aim]

	for f_path in py_files:
		with open(f_path, 'r') as fp:
			f_content = fp.read()
		if header:
			config = {
				"filename": os.path.basename(f_path),
			}
			for k, v in args.config.items():
				config[k] = v
			modified = addHeader(f_content, header, config)
			with open(f_path, 'w') as fp:
				fp.write(modified)
		else:
			try:
				modified = delHeader(f_content)
				with open(f_path, 'w') as fp:
					fp.write(modified)
			except LookupError:
				print("Failed to delete header for: %s" % f_path)

if __name__ == "__main__":
	main()

