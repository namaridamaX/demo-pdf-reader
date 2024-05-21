from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

# 読み込みたいPDFファイル(http://it-gyousei.com/download/doc/koyoukeiyaku.pdf)
input_file = open('/content/20240214AC_5.pdf', 'rb')
# 書き込み用のテキストファイル
output_file = open('output.txt', 'w')

laparams = LAParams()
resource_manager = PDFResourceManager()
device = TextConverter(resource_manager, output_file, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)

for page in PDFPage.get_pages(input_file):
    interpreter.process_page(page)