# ワードクラウドの作成
import docx2txt, MeCab, requests, os, re, nlplot, os
import pandas as pd

def word_cloud(file):
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

    # df化
    df = pd.DataFrame({'sentencs': sentencs})
    
    # グラフ化
    npt = nlplot.NLPlot(df, target_col='sentencs')
    fig_wc = npt.wordcloud(width=900, height=600, max_words=100, max_font_size=100, colormap='tab20_r', save=False)

    save_dir = os.path.join("static", "images", "wc")
    
    save_path = os.path.join(save_dir, "wordcloud.png")

    image = fig_wc.to_file(save_path)

    return image