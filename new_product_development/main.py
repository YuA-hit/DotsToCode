import pandas as pd
import random
import numpy as np
import GeneticAlgorithm as ga


def convert_elements(df):
    # 新しいDataFrameを格納するためのリスト
    new_df_data = []

    # DataFrameの各行に対して処理を行う
    for index, row in df.iterrows():
        # 行内の要素の順序を追跡するための辞書
        element_to_index = {}
        new_row = []

        for element in row:
            # 要素が辞書になければ追加し、インデックス（数字）を割り当てる
            if element not in element_to_index:
                element_to_index[element] = len(element_to_index)
            # 新しい行に数字を追加
            new_row.append(element_to_index[element])

        # 変換された行を新しいDataFrameのデータに追加
        new_df_data.append(new_row)

    # 新しいDataFrameを作成
    converted_df = pd.DataFrame(new_df_data, columns=df.columns)

    return converted_df


def create_genom(list):
    return ga.genom(list, 0)


def evaluation(genomClass):
    list = genomClass.getGenom()
    # 与えられたデータと母集団の各データポイントとのユークリッド距離を計算する
    distances = [
        np.linalg.norm(np.array(list) - np.array(sweets)) for sweets in sweets_lists
    ]
    # 最小の距離を計算する
    min_distance = np.min(distances)
    return min_distance


def select(ga, elite_length):
    # 現行世代個体集団の評価を高い順番にソートする
    sort_result = sorted(ga, reverse=True, key=lambda u: u.evaluation)
    # 一定の上位を抽出する
    result = [sort_result.pop(0) for i in range(elite_length)]
    return result


def crossover(population_one, population_second):
    # 子孫を格納するリストを生成する
    genom_list = []
    # 入れ替える二点の点を設定する
    cross_one = random.randint(0, GENOM_LENGTH)
    cross_second = random.randint(cross_one, GENOM_LENGTH)
    # 遺伝子を取り出す
    one = population_one.getGenom()
    second = population_second.getGenom()
    # 交叉する
    progeny_one = one[:cross_one] + second[cross_one:cross_second] + one[cross_second:]
    progeny_second = (
        second[:cross_one] + one[cross_one:cross_second] + second[cross_second:]
    )
    # genomClassインスタンスを生成して子孫をリストに格納する
    genom_list.append(ga.genom(progeny_one, 0))
    genom_list.append(ga.genom(progeny_second, 0))
    return genom_list


def next_generation_gene_create(ga, ga_elite, ga_progeny):
    # 現行世代個体集団の評価を低い順番にソートする
    next_generation_geno = sorted(ga, reverse=False, key=lambda u: u.evaluation)
    # 追加するエリート集団と子孫集団の合計ぶんを取り除く
    # `pop`する回数を計算する
    pop_count = min(len(next_generation_geno), len(ga_elite) + len(ga_progeny))
    # 実際に`pop`する
    for i in range(pop_count):
        next_generation_geno.pop(0)
    # エリート集団と子孫集団を次世代集団を次世代へ追加する
    next_generation_geno.extend(ga_elite)
    next_generation_geno.extend(ga_progeny)
    return next_generation_geno


def mutation(ga, individual_mutation, genom_mutation):
    ga_list = []
    for i in ga:
        # 個体に対して一定の確率で突然変異が起きる
        if individual_mutation > (random.randint(0, 100) / 100):
            genom_list = []
            for i_ in i.getGenom():
                # 個体の遺伝子情報一つ一つに対して突然変異が起きる
                if genom_mutation > (random.randint(0, 100) / 100):
                    genom_list.append(random.randint(0, 1))
                else:
                    genom_list.append(i_)
            i.setGenom(genom_list)
            ga_list.append(i)
        else:
            ga_list.append(i)
    return ga_list


# 遺伝子情報の長さ
GENOM_LENGTH = 21
# 遺伝子集団の大きさ
MAX_GENOM_LIST = 13
# 遺伝子選択数
SELECT_GENOM = 10
# 個体突然変異確率
INDIVIDUAL_MUTATION = 0.1
# 遺伝子突然変異確率
GENOM_MUTATION = 0.01
# 繰り返す世代数
MAX_GENERATION = 50
# ファイルパス
file_path = "0322_list.xlsx"

# Excelファイルの読み込み
df = pd.read_excel(file_path)
# 列を削除
df = df.drop(df.columns[0], axis=1)
# 行を削除
df = df.drop(df.index[0], axis=0)
# 文字を数字に変換
df = convert_elements(df)
# 各列の最初の20行をリストとして抽出し、それらのリストを含むリストを生成
sweets_lists = [df.iloc[:21, i].tolist() for i in range(df.shape[1])]

if __name__ == "__main__":

    #  最初の母集団を生成する
    current_group = []
    for i in range(MAX_GENOM_LIST):
        current_group.append(create_genom(sweets_lists[i]))

    for count_ in range(1, MAX_GENERATION + 1):
        # 現行世代個体集団の遺伝子を評価する
        for i in range(MAX_GENOM_LIST):
            evaluation_result = evaluation(current_group[i])
            current_group[i].setEvaluation(evaluation_result)
        # エリート個体を選択する
        elite_genes = select(current_group, SELECT_GENOM)
        # エリート遺伝子を交叉させ、リストに格納する
        progeny_gene = []
        for i in range(0, SELECT_GENOM):
            progeny_gene.extend(crossover(elite_genes[i - 1], elite_genes[i]))
        # 次世代個体集団を現行世代、エリート集団、子孫集団から作成する
        new_group = next_generation_gene_create(
            current_group, elite_genes, progeny_gene
        )
        # 次世代個体集団全ての個体に突然変異を施す
        new_group = mutation(new_group, INDIVIDUAL_MUTATION, GENOM_MUTATION)

        # 評価
        # 各個体適用度を配列化する
        fits = [i.getEvaluation() for i in current_group]

        # 進化結果を評価する
        min_ = min(fits)
        max_ = max(fits)
        avg_ = sum(fits) / len(fits)

        # 現行世代の進化結果を出力する
        print("-----第{}世代の結果-----".format(count_))
        print("  Min:{}".format(min_))
        print("  Max:{}".format(max_))
        print("  Avg:{}".format(avg_))

        # 現行世代と次世代を入れ替える
        current_group = new_group

    # 最終結果出力
    print("最も優れた個体は{}".format(elite_genes[0].getGenom()))
