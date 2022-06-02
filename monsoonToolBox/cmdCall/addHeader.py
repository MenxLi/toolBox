from typing import List
import argparse, os, sys, string, datetime
from monsoonToolBox.filetools.files import recursivlyFindFilesByExtension

MARKER = "+==***---------------------------------------------------------***==+"

def _splitLine(line: str, n_max: int, keep_word = False) -> List[str]:
	if len(line) <= n_max:
		return [line]
	else:
		if not keep_word:
			line_start = line[:n_max]
			line_follow = line[n_max:]
			return [line_start] + _splitLine(line_follow, n_max)
		# if keep_word
		line_split = [l + " " for l in line.split(" ")]
		n_current = 0
		for i in range(len(line_split)):
			l = line_split[i]
			n_current += len(l)
			if n_current < n_max:
				# length not enouth
				continue

			if n_current == n_max and l[-1] == ' ':
				# just good
				return [line[:-1]]
			if i > 0:
				n_needed = 0
				for j in range(i):
					print(line_split[j])
					n_needed += len(line_split[j])
			else:
				# i==0, single long line
				n_needed = n_max
			return [line[:n_needed]] + _splitLine(line[n_needed:], n_max)

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
	
	header = Replacer(header).parse()

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
	return "#" + line + "#"

def addHeader(content: str, header: str) -> str:
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
	
	def config(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, "VAL_"+k.upper(), v)
	
	def _date(self):
		date = datetime.datetime.now()
		date = date.strftime("%Y-%m-%d")
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
			modified = addHeader(f_content, header)
		else:
			modified = delHeader(f_content)
		with open(f_path, 'w') as fp:
			fp.write(modified)

if __name__ == "__main__":
	main()

