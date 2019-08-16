## GitLab ＋ GitlabRunner構築  
### GitLab導入の大まかな流れ  
1. GitLabサーバを立てる
1. GitLabアップデート
1. 証明書配置（HTTPS化）
1. external_urlを変更 
1. メールサーバを立てる
1. GitLabのメール送信設定

#### GitLabサーバを立てる
AzureからGitLab入りのインスタンスを選択して立てる  。
GitLabはDockerイメージやインストーラから導入してもよい。[公式](https://about.gitlab.com/install/)を見ると、他にもいろいろある。
静的IPにするかドメイン名を取得する。

#### GitLabアップデート  
AzureのGitLabはバージョンが古いのでアップデートする。差分アップデートとなるので、[公式のパッケージ置き場](https://packages.gitlab.com/gitlab/gitlab-ce)を見て順番に適用する。

#### 証明書配置（HTTPS化）
証明書を入手する。オレオレならopensslで作成する。
[参考](https://blog.apar.jp/linux/3555/#SSL)

#### external_urlを変更  
Azureで建てた場合、これをしないと招待メールの認証がそのままでは通らない。
サイト内のURL表示もおかしくなる。下記にある設定ファイル内のexternal_urlを取得したドメイン名に変更。
- /etc/gitlab/gitlab.rb

#### メールサーバを立てる  
Azure上のインスタンスにsendmailを入れる場合、迷惑メールにさせないようにしなければならない（スパム対策）。
SaaS（SendGrid）を使ってもいい。

#### GitLabのメール送信設定  
標準だとsendmailを使う設定になっている。[参考](https://maku77.github.io/git/gitlab/email-settings.html)


### GitLabRunner 導入の大まかな流れ（と、自動テスト用のサンプルコード）  
1. ymlファイル作成（GitLabサーバ側）
1. Docker（Runner実行環境）をインストール
1. GitLabRunnerをインストール
1. 証明書配置
1. GitLabRunner設定

GitLab,GitLabRunnerを別サーバに構築し、テスト実行環境を毎回Dockerで作成する  
GitLab,GitLabRunner自体をそれぞれDocker内にインストールするスマートな方法もあるらしい

実行環境は下記から選べる
* Shell  
* Docker  
* Docker Machine and Docker Machine SSH (autoscaling)  
* Parallels  
* VirtualBox  
* SSH  
* Kubernetes  

#### ymlファイル作成  
GitLab上でGUIポチポチして発行  
中身は良しなに書き換える  
対象のレポジトリでパイプラインの設定もしておく

#### Docker（Runner実行環境）をインストール  
yumるか、aptする

##### Docker便利コマンドメモ
* コンテナ全部消す  

```  
docker rm $(docker ps -aq)
```  
* 複数のポートフォワードしつssh接続  

```  
docker run -p 8000:8000 -p 554:554 -it CONTAINER_ID /bin/bash
```

#### GitLabRunnerをインストール  
[ここを読む](https://docs.gitlab.com/runner/install/linux-manually.html)


#### 証明書配置
対象のGitLabサーバがHttpsの場合、サーバ証明書がないと通信に失敗する

opensslで取得するか、直接コピーする  
**ファイル名がGitLabサーバのドメイン名である必要がある**
```
$ openssl s_client -connect my.gitlab.domain:443 -showcerts < /dev/null | openssl x509 -outform PEM > /etc/gitlab-runner/certs/my.gitlab.domain.crt
```
#### GitLabRunner設定

```
$ gitlab-runner register
```

詳しくは[ここを読む](https://docs.gitlab.com/runner/register/)  
分からないことがあれば「GitLab Runner Commands」でググって出てくる公式ドキュメントを見ると良い

#### CDもしたい場合  
docker buildコマンドを実行し、  
作成したイメージをコンテナレポジトリや、WebApps等のPaaSにデプロイするよう、  
.ymlに書く
