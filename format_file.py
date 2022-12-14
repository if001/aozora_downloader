import sys
import pandas as pd
from pathlib import Path
import argparse
import glob

def text_cleanse_df(df, keep_title=False):
    # 本文の先頭を探す（'---…'区切りの直後から本文が始まる前提）
    head_tx = list(df[df['text'].str.contains(
        '-------------------------------------------------------')].index)
    # 本文の末尾を探す（'底本：'の直前に本文が終わる前提）
    atx = list(df[df['text'].str.contains('底本：')].index)
    if head_tx == []:
        # もし'---…'区切りが無い場合は、作家名の直後に本文が始まる前提
        head_tx = list(df[df['text'].str.contains(author_name)].index)
        head_tx_num = head_tx[0]+1
    else:
        # 2個目の'---…'区切り直後から本文が始まる
        head_tx_num = head_tx[1]+1
    
    df_e = df[head_tx_num:atx[0]]
    if keep_title:
        df_title = df[0:1]
        df_e = pd.concat([df_title, df_e])

    # 青空文庫の書式削除
    df_e = df_e.replace({'text': {'《.*?》': ''}}, regex=True)
    df_e = df_e.replace({'text': {'［.*?］': ''}}, regex=True)
    df_e = df_e.replace({'text': {'｜': ''}}, regex=True)

    # 字下げ（行頭の全角スペース）を削除
    df_e = df_e.replace({'text': {'　': ''}}, regex=True)

    # 節区切りを削除
    df_e = df_e.replace({'text': {'^.$': ''}}, regex=True)
    df_e = df_e.replace({'text': {'^―――.*$': ''}}, regex=True)
    df_e = df_e.replace({'text': {'^＊＊＊.*$': ''}}, regex=True)
    df_e = df_e.replace({'text': {'^×××.*$': ''}}, regex=True)

    # 記号、および記号削除によって残ったカッコを削除
    df_e = df_e.replace({'text': {'―': ''}}, regex=True)
    df_e = df_e.replace({'text': {'…': ''}}, regex=True)
    df_e = df_e.replace({'text': {'※': ''}}, regex=True)
    df_e = df_e.replace({'text': {'「」': ''}}, regex=True)

    # 一文字以下で構成されている行を削除
    df_e['length'] = df_e['text'].map(lambda x: len(x))
    df_e = df_e[df_e['length'] > 1]

    # インデックスがずれるので振りなおす
    df_e = df_e.reset_index().drop(['index'], axis=1)

    # 空白行を削除する（念のため）
    df_e = df_e[~(df_e['text'] == '')]

    # インデックスがずれるので振り直し、文字の長さの列を削除する
    df_e = df_e.reset_index().drop(['index', 'length'], axis=1)
    return df_e


def save_cleanse_text(target_file, tx_org_dir, tx_edit_dir, keep_title):
    try:
        # ファイルの読み込み
        print(target_file)
        # Pandas DataFrameとして読み込む（cp932で読み込まないと異体字が読めない）
        df_tmp = pd.read_csv(target_file, encoding='cp932', names=['text'])
        
        # 元データをUTF-8に変換してテキストファイルを保存
        out_org_file_nm = Path(target_file.stem + '_org_utf-8.tsv')
        df_tmp.to_csv(Path(tx_org_dir / out_org_file_nm), sep='\t',
                      encoding='utf-8', index=None)
        # テキスト整形
        df_tmp_e = text_cleanse_df(df_tmp, keep_title)
        out_edit_file_nm = Path(target_file.stem + '_clns_utf-8.txt')
        df_tmp_e.to_csv(Path(tx_edit_dir / out_edit_file_nm), sep='\t',
                        encoding='utf-8', index=None, header=False)
    except Exception as e:
        print(e)
        print(f'ERROR: {target_file}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True, help='author id')
    parser.add_argument('--keep_title', action='store_true', help='if ture, title set to start of sentence.')
    args = parser.parse_args()
    author_id = args.id
    keep_title = args.keep_title

    out_dir = Path(f'./out_{author_id}/')
    if keep_title:
        out_dir = Path(f'./out_{author_id}_title/')
    tx_org_dir = Path(out_dir / './org/')  # 元テキストのUTF-8変換ファイルの保存先
    tx_edit_dir = Path(out_dir / './edit/')  # テキスト整形後のファイル保存先

    tx_dir = Path(author_id)
    # zipファイルのリストを作成
    zip_list = list(tx_dir.glob('*.zip'))
    # 保存ディレクトリを作成しておく
    tx_edit_dir.mkdir(exist_ok=True, parents=True)

    tx_org_dir.mkdir(exist_ok=True, parents=True)

    for target_file in zip_list:
        save_cleanse_text(target_file, tx_org_dir, tx_edit_dir, keep_title)

def clean_test():
    target_file = 'out_001779/org/56645_ruby_58194_org_utf-8.tsv'
    # df_tmp = pd.read_csv(target_file, encoding='cp932', names=['text'])
    df_tmp = pd.read_csv(target_file,  names=['text'])
    text_cleanse_df(df_tmp)
    
def title_test():
    for target_file in glob.glob('./001779/*.zip'):
        try:
            print(target_file)
            df = pd.read_csv(target_file, encoding='cp932', names=['text'])
            print(df[0:1])
        except:
            print()
    
if __name__ == '__main__':
    main()
