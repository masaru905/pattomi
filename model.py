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

# 名詞抽出の関数作成
import MeCab


# 共起ネットワークの作成
import MeCab, itertools, collections, requests, os, re, nlplot
import pandas as pd
def co_network(file):
    # 文書化
    text = docx2txt.process(file)
    text = re.sub(r'\d+', '', text)

    def mecab_tokenizer(text):
        path = "-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"
        mecab = MeCab.Tagger(path)
        # 形態素解析
        node = mecab.parseToNode(text)
        # 形態素解析→リスト格納
        wordlist = []



        # stopwordsの作成
        filename = os.path.join(os.getcwd(), 'stopwords_japanese.txt')
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                stopwords = f.read().split('\n')
            
        else:
            url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
            r = requests.get(url)
            stopwords = r.text.split('\r\n')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(stopwords))
        

        
        # 名詞のみを格納    
        while node:
            if node.feature.split(',')[0] == '名詞' and node.surface not in stopwords:
                wordlist.append(node.surface)
            node = node.next
        return wordlist

    sentencs = [mecab_tokenizer(sentence) for sentence in text.split('。')]
    # 文章単位で名詞のコンビを作る
    sentencs_combs = [list(itertools.combinations(sentence,2) for sentence in sentencs)]
    # 単語の並びをソートする
    words_combs = [[tuple(sorted(words)) for words in sentence] for sentence in sentencs_combs]
    # 単語のコンビを一つのリスト化する
    target_combs = []
    for words_comb in words_combs:
        target_combs.extend(words_comb)
    # 単語のコンビを数える
    ct = collections.Counter(target_combs)

    # df化

    df = pd.DataFrame(ct.items(), columns=['pair', 'freq'])
    
    df['pair'] = df['pair'].apply(lambda x: ','.join(x))
    
    # グラフ化
    npt = nlplot.NLPlot(df, target_col='pair')
    limitwords = npt.get_stopword(top_n=0, min_freq=0)

    npt.build_graph(stopwords=limitwords, min_edge_frequency=100)

    fig_co_network = npt.co_network(title='Co-occurrence network', sizing=100, node_size='adjacency_freqency', color_palette='hls', width=1100, height=700, save=False)

    return fig_co_network.show('result.html')