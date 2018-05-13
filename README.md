# はじめに
本テキストはサーバレス開発の入門のようなものである。README.mdにしたがって作業することで次の知識が身につく。

- Git の簡単な使い方
- AWS Lambda の概要 (何をするか、関連するAWSサービス)
- Serverless Framework を使った簡単な Lambda のデプロイ

想定環境はmacOS端末だが、Shellが使えてGitがインストールされていれば問題ない。

# Gitで簡単バージョン管理
## Gitとは
バージョン管理システム。分散型と呼ばれ、複数人での開発に向いているとされている。

ユーザはコードの集まりをリポジトリという単位で管理する。ユーザであるアプリ開発者は、メンバーがアクセスできるところにあるリポジトリ (リモートリポジトリ) を手元の端末にコピーし(クローン)、それを編集した上でリモートリポジトリに適用する (プッシュ)。これを繰り返して開発を進めていく。

## Githubとは
[Github](https://github.com/)はGitのリモートリポジトリの置き場所を提供してくれるサービス(ホスティングサービス)である。公開リポジトリなら無料で作成できるが、非公開リポジトリは有料プランに加入しないと作成できない。超有名。
類似サービスには[bitbucket](https://bitbucket.org/)なんかもある。

## Gitを触ってみる
使い方はNulabさんの[サルでもわかるGit入門](https://backlog.com/ja/git-tutorial/)などを参考にしてもらうとして、ここでは最低限のコマンドを説明する。

### Gitをインストールする
macOS端末ならば[Homebrew](https://brew.sh/index_ja)経由でのインストールが楽なので、その方法を説明する。HomebrewはmacOS用のパッケージ管理ツールで、macOSにデフォルトで用意されていないコマンド群の導入・管理ができる。macOSで開発する人にとっては超有名なツール。インストール方法は公式ページにある通り、以下をターミナル(bash)に貼り付けて実行するだけで良い。

``` sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

GitのCLIコマンドである `git` はHomebrewなら次のコマンドを入力することで一発でインストールできる。

``` sh
brew install git
```

実際に `git` コマンドが使えるかどうかを確かめる。次のコマンドはインストールしたGitのバージョンを表示するもので、バージョンが表示されていればインストールは無事完了したことになる。(この例の `$` はターミナルのプロンプトという補助表示領域を表しているので実際に入力する必要はない)

``` sh
$ git --version
git version 2.14.3 (Apple Git-98)
```

一般にCLIコマンド (アプリケーション) がインストールされているかを確認するときには `(コマンド名) --version` のようにバージョン確認のオプションを利用することが多い。


### `git clone` でリモートリポジトリをローカルにコピーする
このリポジトリに保存しているコードをローカル端末にコピーする。以下のコマンドを入力する。

```
git clone https://github.com/Hikosaburou/intro_serverless.git ~/intro_serverless
```

`~/intro_serverless` には適宜コピー先のディレクトリ名に置き換えてほしい。成功すると、コピー先のディレクトリ内にファイルが追加されるはずである。

```
$ ls ~/intro_serverless
README.md
```

このリポジトリにはREADME.mdしか入ってないので上のような表示になる。以降はこのディレクトリ上で作業を行う。

### `git branch` でブランチを作成する
Gitでは単純な時系列によるコードの変更管理はもちろん、ブランチという機能を使った並行作業向けの変更管理もできる。

コードの変更履歴のことをGitではツリーと呼ぶことがあるが、ブランチはその名の通り変更履歴に分岐を作成する。ブランチを作成する(切るともいう)ことでコードの主流から分岐し、並行してコードを編集できる。もちろん、切ったブランチは主流に統合できる(マージすると言う)ため、例えばアプリの商用コードを管理する場合、ブランチを切ってそこで開発を行い、マージすることで商用コードに適用できる。

リモートリポジトリ上にあるブランチはリモートブランチという。手元の端末にあるブランチをローカルブランチという。基本的にローカルブランチはリモートブランチと対応づけられており、リモートブランチの内容とローカルブランチの内容を `git` コマンドで同期することができる。また、デフォルトではmasterブランチのみが用意されており、これが多くの場合変更管理の源流となる。もちろんブランチは開発者が自由に切れるので、チームによってブランチの切り方のルールが異なっていたりする。

現在のローカルブランチは次のコマンドで確認できる。

```
$ git branch
* master
```

`* master` の意味は「現在 master というローカルブランチが存在し、\* マークがついているのでこのブランチ上で作業を行なっている」である。

これからの作業用にブランチを作成する。ブランチは以下の書式で作成できる。

```
git branch <branch name>
```

例えば、hogehoge というブランチを作成した後にローカルブランチを確認すると、次のようになる。

```
$ git branch hogehoge
$ git branch
  hogehoge
* master
```

### `git checkout` でブランチを切り替える
作成したブランチを切り替えるには、次の書式でコマンドを実行すれば良い。

```
git checkout <branch name>
```

先ほど作成したブランチに切り替える場合の実行例は次の通り。

```
$ git checkout hogehoge
Switched to branch 'hogehoge'
$ git branch
* hogehoge
  master
```

`git branch` で、現在のブランチが切り替わっていることが確認できる。

### `git add` と `git commit` で変更差分を登録する
ブランチの中でコードを作成・変更したら、まずは `git add` で変更リストに加える。

```
git add <path to file>
```

`git add` したコードをバックアップ可能な点として登録する (コミットする) ために、 `git commit` を次の書式で実行する。

```
git commit -m `commit message`
```

`commit message` には通常、変更点を簡潔に記載する (xxを修正、ooを追加、など) 。

この時点ではまだローカルに変更点を登録しただけで、まだリモートには同期されていない。

### `git push` でリモートブランチに同期する
ローカルブランチでコミットした内容をリモートに同期するために、次の書式で `git push` を実行する。

```
git push origin <branch name>
```

これにより、ローカルブランチと同名のリモートブランチが作成され、ブランチの内容が同期される。ここまでくれば、手元の端末から誤ってファイルを消してしまってもリモートブランチからファイルを復旧することができる。

昨日追加のためにブランチを切り、そのブランチ上で作業し、それをプッシュするところまで説明した。最後にブランチをマージする作業が残っているが、これは最後に説明したい。

# AWS Lambda によるサーバレス開発超入門
Gitの簡単な使い方を知ったところで、本題に入る。ここでは、サーバレス開発の雰囲気を知ることを目標として、AWS Lambda と API Gateway を使った単純な祝日回答APIを作成する。

## サーバレスとは
開発者がサーバを準備することなくプログラムを直接実行させられるサービス一般もしくはその仕組みを用いて作成されたアプリケーション全般のこと。多くの場合は実行時間と利用したメモリサイズに基づく課金となるため、利用方法によっては仮想サーバ型インスタンスを利用するよりも安くアプリケーションを作成できる。

## AWS Lambda
AWSが提供するサーバレスコンピューティングサービスの一つ。AWSの代表的なサービスの一つである。

## API Gateway
APIとは Application Programming Interface の略で、あるアプリケーションを別のプログラムで利用するときの窓口のことである。例えばTwitterのAPIをプログラムから使うことでプログラム経由で自動的にツイートをすることができる (つまりbotなんかも作れる)。

API Gateway はそんなAPIをAWSで作成できるサービスである。API Gateway という名前の通り、APIを公開して、そのAPIと実際の処理を紐付ける役割を果たしている。

## 作るもの

日本の祝休日を返すAPIを作ってみる。

例えば、こんな感じでAPI

### AWS Lambda を無理矢理使ってみる

## Serverless Framework を使って Lambda function をデプロイする

# Gitを使う(再)
作成したファイルをGithubにプッシュするところまでは前の節で説明した。残る作業は、ブランチのマージである。

## プルリクエストを行う


## 参考文献
