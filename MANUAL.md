# AIクラウド利用手順書

マークダウン記法で記載されています。マークダウンの表示できるツールで見ると多少綺麗に見えます。

---
## 概要
- AIクラウドはGPUリソースをシェアして使うためのコンピュータクラスタシステムです。
GPUサーバとヘッドサーバによるクラスタシステムが組まれています。

- クラスタ内では一部のディスクが共有されており、そこに置かれたプログラムやデータを使って、GPUによる計算を行います。

- 処理はジョブとして投入し、コンテナとして実行します。
サーバにはツールやライブラリ類はほとんどインストールされていませんので、必要なツールやライブラリはコンテナ内にインストールして使います。


---
## GPUサーバとヘッドサーバ
### GPUサーバ
- GPUが搭載されており、GPU計算を行う役割です。

- GPUサーバには通常はログインせず、ヘッドサーバからジョブを投入します。

### ヘッドサーバ
- GPUサーバにジョブを依頼する役割です。

- ジョブのうち、GPUを必要としないものはヘッドサーバでも実行されます。

- 例えば、計算用のデータを準備するなど、GPUを必要としない通常の作業はヘッドサーバ上で行います。


---
## 作業の大まかな流れ
1. ヘッドサーバにファイルを配置する(scpなどで、共有ディスク上に転送)。
2. ヘッドサーバにログインする。
3. コンテナを作成する。
4. ジョブを投入する。
5. 結果を確認する。
6. 結果のデータを自分のコンピュータに転送する(scp, rsyncなど)。


---
## 細かいことを言わずに使ってみる
### コンテナの作成
- ヘッドサーバにて、以下のようにコマンドを実行します。

- 例1: デフォルトのベースdockerイメージ(nvidia/tensorflow-tf2-py3の最新版)を使用して、カレントディレクトリ名をコンテナ名として作成する。
```
sbuild.sh
```

- 例2: ベースdockerイメージを自分で指定してコンテナを作成する。
```
sbuild.sh nvcr.io#nvidia/tensorflow:22.02-tf2-py3
```

- 例3: DockerHubのUbuntu20.04をを指定してコンテナを作成する。
```
sbuild.sh ubuntu:20.04
```

### ジョブの投入
- ヘッドサーバにて、以下のようにコマンドを実行します。

- 例1: コンテナ内でbashにより作業を行う。
```
srun.sh
```

- 例2: セットアップ用のスクリプト(setup.sh)を実行する。
```
chmod +x setup.sh
srun.sh sestup.sh
```

- 例3: pythonプログラムを実行する。
```
srun.sh python do_something.py
```


---
## 知っておく必要のあるツール
### slurm
- slurmはジョブスケジューラであり、これを用いてジョブの投入実行を行います。

### enroot
- enrootはコンテナ環境であり、enrootのコンテナ環境としてジョブを動かします。

- enrootのコンテナはenroot自身で作り出せますが、dockerイメージをインポートして使うこともできます。

### pyxis
- enrootのコンテナをslurmから扱えるよう、slurmのコマンドオプションを拡張するのがpyxisです。

- pyxisを直接使うことはなく、slurmのジョブ投入コマンドであるsrunに対してpyxisの拡張オプションが追加されているので、それを使用します。


---
## enrootコンテナ
### enrootコンテナ名
- enrootコンテナ名が重複するとエラーが起きたり上書きされたりするため、ユニークな名前を付けます。

### enrootコンテナの作成
- dockerイメージをベースとして、myrepoという名前のコンテナを作成するには以下のようにします。

- NVIDIA GPU CLOUDのtensorflowイメージをそのまま利用する。
```
srun --gres=gpu:1 --container-image=nvcr.io#nvidia/tensorflow:20.12-tf2-py3 --container-name=myrepo true
```

- 作成済みのコンテナにパッケージやpythonライブラリを追加する
```
chmod +x setup.sh
srun --gres=gpu:1 --container-name=myrepo --container-mounts=.:/workspace ./setup.sh
```

- setup.shの例
```
#!/bin/bash
apt-get update
apt-get install -y time # インストールしたいパッケージを列挙
pip install -U pip
pip install optuna # インストールしたいpythonライブラリを列挙
```

### enrootコンテナの確認や削除
- enrootコンテナの一覧表示
```
enroot list
```
(コンテナ名は先頭に`pyxis_`が付いている)


- enrootコンテナの削除
```
enroot remove -f コンテナ名
```
(コンテナ名の先頭には`pyxis_`が必要)


---
## ジョブの投入例
- CPUのみを使用する処理(処理が実行されたホスト名を表示)
```
srun --container-name=myrepo --container-mounts=.:/workspace hostname
```

- システムのコマンドを実行する例(GPUを1個割り当てて、nvidia-smiによりGPUの状態を表示)
```
srun --gres=gpu:1 --container-name=myrepo --container-mounts=.:/workspace nvidia-smi
```

- シェルを起動してコマンドを実行する例(GPUを1個割り当てて、そのIDを見てみる)
```
srun --gres=gpu:1 --container-name=myrepo --container-mounts=.:/workspace /bin/sh -c 'echo $CUDA_VISIBLE_DVICES'
```

- シェルスクリプトを起動する例(GPUを1個割り当てて何かする)
```
chmod +x do_something.sh
srun --gres=gpu:1 --container-name=myrepo --container-mounts=.:/workspace ./do_something.sh
```


---
## コマンドリファレンス

### 本家の情報
- [slurm](https://slurm.schedmd.com/overview.html)

- [slurmコマンドマニュアル](https://slurm.schedmd.com/man_index.html)

- [slurmコマンドチートシート](https://slurm.schedmd.com/pdfs/summary.pdf)

### slurmの主要なコマンド
- srun: ジョブのコマンドラインからの投入

- sbatch: ジョブのバッチ定義ファイルによる投入

- squeue: ジョブの状態確認(例: `squeue -l`)

- scancel: ジョブの中止(例: `scancel -f ジョブID`)

- sinfo: クラスタ状態の参照(例: `sinfo -N -l`)

### pyxisによるslurmオプションの拡張
- [pyxisにより拡張されるオプション](https://github.com/NVIDIA/pyxis/wiki/Usage)

- `--container-mounts=.:/workspace`はカレントディレクトリをコンテナのカレントディレクトリにマウントするpyxisによる拡張オプションです。これにより、カレントディレクトリ配下にあるプログラムやデータをコンテナから参照できるようにします。

- `--container-mount-home`はホームディレクトリをコンテナにマウントするpyxisによる拡張オプションです。ホームを介してのデータのやり取りがある場合にのみ指定します。


---
## AIクラウドへのログイン方法
### 公開鍵の登録
- AIクラウドにログインするためには、SSHの公開鍵を登録する必要があります。

- (持っていなければ)RSA鍵を生成し、そのうち公開鍵(id_rsa.pub)だけをシステム管理者に渡して登録してもらって下さい。

- 秘密鍵を紛失した場合は、管理者に連絡して下さい。アカウント停止や公開鍵の再登録などの対応を行います。

### ログイン方法
- `ssh -p 22xxx yyy`
  - xxx: ヘッドサーバアドレスの最後の数字(192.168.105.217なら217の部分)
  - yyy: 外部IPアドレス

- 例: `ssh -p 22217 yamada.jo.sus.ac.jp`

- GPUサーバへは直接ログインせずにヘッドサーバ経由で使ってください。


### 外部IPアドレス
- tetsu1.silocal.sus.ac.jp: 学内LANからログインする場合

- yamda.jo.sus.ac.jp: インターネットからログインする場合


### ヘッドサーバアドレス
- 192.168.105.217: head(ヘッドサーバ1)

- 192.168.105.232: head2(ヘッドサーバ2)

- 192.168.105.243: head3(ヘッドサーバ3)


---
## 共有ディスク
### /data
- 「/data」がNFSによりクラスタサーバ間で共有されています。

### ホーム
- ホームディレクトリは、「/data」上に置かれています。

- 従って、ホームディレクトリ配下で作業をすれば、クラスタのどのサーバからでもファイルが見えることになります。

### 同期の制限事項
- 同一ファイルに対して1秒以内に複数サーバから更新を実施した場合に、まれに、ファイルの更新が同期されないことがあります。

- これは、NFSやキャッシュの問題ではなく、Linuxのファイルシステムのタイムスタンプの精度に関わる問題であり、抜本的対策は難しいです。

- 問題が起きた場合、最後に更新を行ったサーバにて、touchなどでファイルのタイムスタンプを再更新すれば同期されます。


---
## GPU計算用dockerイメージ
### 入手先
- GPU計算用のdockerイメージは、[NVIDIA GPU CLOUD](https://ngc.nvidia.com/)から入手できます。

- 例えば、TensorFlowの入ったイメージは、nvcr.io#nvidia/tensorflow:20.12-tf2-py3のように指定して入手できます。

- NVIDIA GPU CLOUDのアカウント取得は無料です。

- アカウント作成後、dockerでログインするためのAPI Keyを取得して下さい。

### NVIDIA GPU CLOUDへのログイン
- NVIDIA GPU CLOUDからdockerイメージをダウンロードする際は、API Keyによるログインが必要です。

- 毎回手動でログインを行うのは手間がかかるのと、バッチジョブ実行の際に都合が悪いため、`nvcrlogin`コマンドを実行し、API Keyを保存しておくと、自動ログインできるようになりま。

---
