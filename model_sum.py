# 文書ファイルの受け取り→文章化→要約
import docx2txt
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

def summarize_docx(file):
    # 文書化
    text = docx2txt.process(file)
    # 自動要約のオブジェクト生成
    auto_abstractor = AutoAbstractor()
    # トークナイザー（単語分割）にMeCabを指定
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # 文書の区切りを指定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # テキストの抽象化→フィルタリング
    abstractable_doc = TopNRankAbstractor()
    # 文書の要約
    result_dict = auto_abstractor.summarize(text, abstractable_doc)
    summarize_result = result_dict["summarize_result"]

    result = " "
    for i in summarize_result:
        result += i
    return result