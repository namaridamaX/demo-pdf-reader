# pip install tabula-py
# pip install pypdf2
import datetime
import json
import os.path
import re
import pytz
import tabula
import pandas as pd
import PyPDF2
from datetime import datetime, timedelta, timezone
import numpy as np
PDF_PATH = "/content/20230626162541331s.pdf"
SEARCH_WORDS = ["金融商品取引業協会名", "管理職に占める女性", "役員区分", "離職", "賃金の差異", "研修", "育児休業取得率"]
#特定の単語が存在するページ数を返す関数
def find_words_in_pdf(pdf_path, search_words):

  page_numbers = {word: [] for word in search_words}
  with open(pdf_path, 'rb') as file:
      pdf_reader = PyPDF2.PdfReader(file)
      for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          page_text = page.extract_text()
          for word in search_words:
              if word in page_text:
                  page_numbers[word].append(page_num + 1)

  return {word: pages if pages else ['none'] for word, pages in page_numbers.items()}
#上記の関数を動作させて各ワードのページ数を取得する関数
def get_words_in_pdf():
  page_numbers = find_words_in_pdf(PDF_PATH, SEARCH_WORDS)
  # for word, pages in page_numbers.items():
  #   if 'none' in pages:
  #       print(f"'{word}'は見つかりませんでした")
  #   else:
  #       print(f"'{word}'が見つかったページ番号: {pages}")
  print(page_numbers)
  return page_numbers
#PDFから市場区分を取得する関数
def get_dfs(page_number, search_word):
  dfs = tabula.read_pdf(PDF_PATH, lattice=False, pages=page_number, silent=True)
  index = 0
  for i, x in enumerate(dfs):
    array = np.array(x)
    for y in array:
      value = search_word
      matches = [str(s) for s in y if value in str(s)]
      if matches:
          print(f"{value}は配列に部分的に存在します。一致した値: {', '.join(matches)}")
          index = i
          break
        
  dfs = tabula.read_pdf(PDF_PATH, lattice=True, pages=page_number, silent=True)
  # print(dfs[index])
  return dfs[index]

def get_sizyo_word(dfs):
  array = np.array(dfs)
  target_row = 0
  target_column = np.where(np.any(np.char.find(array.astype(str), '証券取引所') >= 0, axis=0))[0] 
  return array[target_row, target_column]

def get_zyosei_word(dfs):
  array = np.array(dfs)
  target_row = 2
  target_column = np.where(np.any(np.char.find(array.astype(str), '管理職に占める女性') >= 0, axis=0))[0] 
  return array[target_row, target_column]

def get_ze_tingin_word(dfs):
  array = np.array(dfs)
  target_row = 2
  target_column = np.where(np.any(np.char.find(array.astype(str), '全労働者') >= 0, axis=0))[0] 
  return array[target_row, target_column]

def get_se_tingin_word(dfs):
  array = np.array(dfs)
  target_row = 2
  target_column = np.where(np.any(np.char.find(array.astype(str), '正規雇用') >= 0, axis=0))[0] 
  return array[target_row, target_column]

def get_hi_tingin_word(dfs):
  array = np.array(dfs)
  target_row = 2
  target_column = np.where(np.any(np.char.find(array.astype(str), '正規雇用') >= 0, axis=0))[0] 
  return array[target_row, target_column + 1]

def get_da_ikuji_word(dfs):
  array = np.array(dfs)
  target_row = 2
  target_column = np.where(np.any(np.char.find(array.astype(str), '男性労働者の育児') >= 0, axis=0))[0] 
  return array[target_row, target_column]

def get_sousisan_word():
  dfs = tabula.read_pdf("/content/20230626162541331s.pdf", lattice=True, pages=2, silent=True)
  none_null_df_list = [df.dropna(axis=1) for df in dfs]
  array = np.array(none_null_df_list[0])
  for i, index in enumerate(none_null_df_list[0]):
    target_column = i
  rows = np.where(np.any(np.char.find(array.astype(str), '総資産額') >= 0, axis=1))[0] 
  return array[rows, target_column][0]

def get_touzyunrieki_word():
  dfs = tabula.read_pdf("/content/20230626162541331s.pdf", lattice=True, pages=2, silent=True)
  none_null_df_list = [df.dropna(axis=1) for df in dfs]
  array = np.array(none_null_df_list[0])
  for i, index in enumerate(none_null_df_list[0]):
    target_column = i
  rows = np.where(np.any(np.char.find(array.astype(str), '当純利益') >= 0, axis=1))[0] 
  return array[rows, target_column][0]


pages_pdf = get_words_in_pdf()
# 市場区分
sizyo_array = get_dfs(pages_pdf['金融商品取引業協会名'][0], '金融商品取引業協会名')
word1 = get_sizyo_word(sizyo_array)
print(word1)
# 本店所在地
# 女性労働者
zyosei_array = get_dfs(pages_pdf['管理職に占める女性'][0], '管理職に占める女性')
word2 = get_zyosei_word(zyosei_array)
print(word2)
# 【全体】男女の賃金の差異
ze_tingin_array = get_dfs(pages_pdf['管理職に占める女性'][0], '全労働者')
word3 = get_ze_tingin_word(ze_tingin_array)
print(word3)
# 【正規】男女の賃金の差異
se_tingin_array = get_dfs(pages_pdf['管理職に占める女性'][0], '全労働者')
word4 = get_se_tingin_word(se_tingin_array)
print(word4)
# 【非正規】男女の賃金の差異
hi_tingin_array = get_dfs(pages_pdf['管理職に占める女性'][0], '全労働者')
word5 = get_hi_tingin_word(hi_tingin_array)
print(word5)
# 従業員一人当たりの平均研修時間
# 従業員一人当たりの平均研修費
# 【全体】育児休業取得率
# 【女性】育児休業取得率
# 【男性】育児休業取得率
da_ikuji_array = get_dfs(pages_pdf['管理職に占める女性'][0], '男性労働者の育児')
word6 = get_da_ikuji_word(da_ikuji_array)
print(word6)
# 3年以内離職率
# 報酬の総額（社外取締役除く）
yaku_hosyu_array = get_dfs(pages_pdf['役員区分'][0], '役員区分')
word7 = get_yaku_hosyu_word(yaku_hosyu_array)
print(word7)
# 報酬等の総額（社外監査を除く）
kan_hosyu_array = get_dfs(pages_pdf['役員区分'][0], '役員区分')
word8 = get_kan_hosyu_word(kan_hosyu_array)
print(word8)
# 社外取締役とその他役員の報酬等の総額
sonota_hosyu_array = get_dfs(pages_pdf['役員区分'][0], '役員区分')
word9 = get_sonota_hosyu_word(sonota_hosyu_array)
print(word9)
# 当純利益
word10 = get_touzyunrieki_word()
print(word10)
# 総資産額
word11 = get_sousisan_word()
print(word11)