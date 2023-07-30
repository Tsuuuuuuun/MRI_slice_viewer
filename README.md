
# MRI_slice_viewer

大学院の講義の自由課題で作成したもの. 対応する.giiファイルを読み込むと, 3D脳データを2Dで表示することができる. また, 2Dで表示した際に, xyzのスライドを動かすことで, 3D脳データのスライスを動かすことができる.

## 使い方

見たい脳データの.giiファイルを用意し, 以下のコマンドを実行する.

```bash
python your_saved_script_name.py path_to_your_nii_file.nii.gz
```

なお, cmapはデフォルトでgrayになっているが, 任意のものに変更することができる.

```bash
python your_saved_script_name.py path_to_your_nii_file.nii.gz jet
```

データ例の元: [https://dataportal.brainminds.jp/atlas-package-download-main-page/bma-2019-ex-vivo](https://dataportal.brainminds.jp/atlas-package-download-main-page/bma-2019-ex-vivo)

データ元論文:
Woodward, Alexander; Gong, Rui; Nakae, Ken; Hata, Junichi; Okano, Hideyuki; Ishii, Shin; Yamaguchi, Yoko : Brain/MINDS 3D Marmoset Reference Brain Atlas 2019 (DataID: 4520) [https://doi.org/10.24475/bma.4520](https://doi.org/10.24475/bma.4520)
