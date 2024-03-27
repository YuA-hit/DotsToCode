# GAを用いた新商品開発AI

2024年3月に行われたハッカソンDots To Code(https://dotstocode.studio.site/ )に提出したプロダクトです。

これは、GA（遺伝的アルゴリズム）を用いた新商品開発AIです。評価関数により新規性を測定し、より新しいコンビニスイーツを考案します。GAは自然選択のプロセスを模倣し、適応度関数に基づいて個体群を進化させることで最適解を探索します。

プレゼンテーション資料：https://www.canva.com/design/DAF-zp9xvZU/zOx2uHtZnHWEwPe2NvRzsg/view?utm_content=DAF-zp9xvZU&utm_campaign=designshare&utm_medium=link&utm_source=editor

## 機能

- Excelファイルからのデータ読み込み
- データの前処理と変換
- 初期母集団の生成
- 適応度に基づく選択、交叉、および突然変異の実行
- 世代を通じた進化の監視
- 最終世代からの最適解の抽出

## セットアップ

- Python 3.11.5
- Pandas
- Numpy

## コードの構造

### 関数の説明

 - convert_elements：データフレーム内の文字列を数値に変換します。
 - create_genom：初期母集団の個体を生成します。
 - evaluation：個体の適応度を評価します。
 - select：適応度に基づき個体を選択します。
 - crossover：選択された個体間で交叉を行い、新たな個体を生成します。
 - next_generation_gene_create：新世代の個体集団を生成します。
 - mutation：個体に突然変異を適用します。

# 著者

愛川 優

このプロダクトは、一橋大学 鷲田 祐一教授にアドバイスを頂いております。

鷲田先生、いつもありがとうございます。

# 参考資料
 - 『Pythonで始めるオープンエンドな進化的アルゴリズム』- 岡 瑞起 著
 - https://rurubu.jp/andmore/article/14253
 - https://kotodori.jp/strategy/product-development-ai/
 - http://www.iba.t.u-tokyo.ac.jp/rs/index.html
 - https://qiita.com/hamadu/items/b62ff71ee2ada9d2a846
 - https://qiita.com/Azunyan1111/items/975c67129d99de33dc21