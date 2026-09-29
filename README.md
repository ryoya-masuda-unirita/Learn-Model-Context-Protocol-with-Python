<p align='center'><a href='https://www.packtpub.com/en-us/unlock?step=1'><img src='https://static.packt-cdn.com/assets/images/packt+events/finalGH_design_redeem.png'/></a></p>

<h1 align="center">
Learn Model Context Protocol with Python, First Edition</h1>
<p align="center">Packt から出版された <a href ="https://www.packtpub.com/en-us/product/learn-model-context-protocol-with-python-first-edition/9781806103232"> Learn Model Context Protocol with Python, First Edition</a> のコードリポジトリです。
</p>

<h2 align="center">
AI 機能の新しい標準で、Python によるエージェントシステムを構築する
</h2>
<p align="center">
Christoffer Noring</p>

<p align="center">
  <a href="https://packt.link/free-ebook/9781806103232"><img width="32px" alt="Free PDF" title="Free PDF" src="https://cdn-icons-png.flaticon.com/512/4726/4726010.png"/></a>
 &#8287;&#8287;&#8287;&#8287;&#8287;
  <a href="https://packt.link/gbp/9781806103232"><img width="32px" alt="Graphic Bundle" title="Graphic Bundle" src="https://cdn-icons-png.flaticon.com/512/2659/2659360.png"/></a>
  &#8287;&#8287;&#8287;&#8287;&#8287;
   <a href="https://www.amazon.com/Learn-Model-Context-Protocol-Python/dp/1806103230/"><img width="32px" alt="Amazon" title="Get your copy" src="https://cdn-icons-png.flaticon.com/512/15466/15466027.png"/></a>
  &#8287;&#8287;&#8287;&#8287;&#8287;
</p>
## サンプルコードの実行環境

依存関係は [uv](https://docs.astral.sh/uv/) で管理しています。リポジトリ直下で次を実行すると、`.venv` に依存関係がインストールされます：

```bash
uv sync
```

各章のサンプルは、`uv run python client.py` のように `uv run` を付けて実行します（Python 3.10 以上が必要です）。

<details open> 
  <summary><h2>本書について</summary>
<a href="https://www.packtpub.com/product/unity-cookbook-fifth-edition/9781805123026">
<img src="https://content.packt.com/B34121/cover_image_small.jpg" alt="Unity Cookbook, Fifth Edition" height="256px" align="right">
</a>

_Learn Model Context Protocol with Python_ は、開発者、アーキテクト、AI 実務者に向けて、Model Context Protocol (MCP) がもたらす変革的な機能を紹介します。MCP は、AI を活用したアプリケーションを標準化し、分散させ、スケールさせるために設計された新しいプロトコルです。本書は実践的なプロジェクトを通じて、リソース管理、クライアントとサーバーのやり取り、大規模なデプロイといった現代的な課題に取り組みます。</br>
著書を持ち、オックスフォード大学のチューターでもある Christoffer の知見をもとに、MCP の構成要素と、それらがサーバーとクライアントの開発をどう効率化するかを学びます。続いて、堅牢なバックエンドの構築や、LLM を組み込んだ賢いクライアントの作成から、Claude for desktop や Visual Studio Code のエージェントといったツールを使ったサーバーとのやり取りへと進みます。各章を通じて、ホスト・クライアント・サーバーの機能をどう記述するかを理解でき、相互運用性の向上、統合の容易化、各コンポーネント間の明確なやり取りにつながります。</br>
セキュリティのベストプラクティスやクラウド向けの構築も扱っているので、MCP ベースのアプリをデプロイする準備が整います。各章で、MCP ベースのエージェントアプリを構築・運用する実践的なスキルが身につきます。巻末の Python 入門で実践的なツールキットが完成し、AI ネイティブなアプリケーションを構築するすべてのチームにとって必携の一冊となっています。</details>
<details open> 
  <summary><h2>本書で学べること</summary>
<ul>

<li>MCP プロトコルとその中核となる構成要素を理解する</li>

<li>さまざまなクライアントに tools と resources を公開する MCP サーバーを構築する</li>

<li>対話型の Inspector ツールでサーバーをテスト・デバッグする</li>

<li>Claude Desktop や Visual Studio Code のエージェントからサーバーを利用する</li>

<li>MCP アプリを保護し、よくある脅威を管理・軽減する</li>

<li>クラウドを活用した方法で MCP アプリを構築・デプロイする</li>

</ul>

  </details>

<details open> 
  <summary><h2>目次</summary>
     <img src="https://cliply.co/wp-content/uploads/2020/02/372002150_DOCUMENTS_400px.gif" alt="Unity Cookbook, Fifth Edition" height="556px" align="right">
<ol>

  <li>Model Context Protocol 入門</li>

  <li>Model Context Protocol の解説</li>

  <li>サーバーの構築とテスト</li>

  <li>SSE サーバーの構築</li>

  <li>Streamable HTTP</li>

  <li>高度なサーバー</li>

  <li>クライアントの構築</li>

  <li>サーバーの利用</li>

  <li>サンプリング</li>

  <li>Elicitation</li>

  <li>アプリケーションの保護</li>

  <li>MCP アプリを本番環境へ</li>

  <li付録：モダン Python による Web 開発</li>

</ol>

</details>


<details open> 
  <summary><h2>本書に必要なもの</summary>
本書の例や演習を進めるには、次のものが必要です：
<ul>
  <li>Python 3.8 以降がインストールされたシステム</li>
  <li>コードエディターまたは IDE（VS Code を推奨）</li>
  <li>コマンドラインの基本的な操作</li>
  <li>HTTP、JSON、ネットワークの基本的な概念の理解</li>
  <li>例を試すための、Claude や ChatGPT などの最新 AI ツールへのアクセス</li>
</ul>
    すべてのコード例は Windows、macOS、Linux で動くように作られています。主要なプラットフォームごとに、具体的なインストール手順とセットアップの案内を載せています。
  </details>
    


<details> 
  <summary><h2>著者について</h2></summary>

_Christoffer Noring_ は、モダンな Web 技術と AI の統合を専門とする情熱的な開発者・教育者で、Microsoft でエンジニアとして働いています。オックスフォード大学のチューターでもあり、Angular、RxJs、生成 AI、そして今回の MCP に関する著書があります。ソフトウェア開発の経験は20年近くにおよび、世界各地の技術カンファレンスで頻繁に登壇しています。上司いわく、彼の一番の長所は、複雑な技術的概念をシンプルで分かりやすい言葉に分解できることだそうです。あなたもそう感じてくれることを願っています！ ;)
コードを書いたり執筆したりしていないときは、新しいユーザーコミュニティを育てたり、開発者のメンターをしたり、家族と過ごしたりしているはずです。


</details>
<details> 
  <summary><h2>関連書籍</h2></summary>
<ul>

  <li><a href="https://www.packtpub.com/en-us/product/nodejs-design-patterns-fourth-edition/9781803238944">Node.js Design Patterns, Fourth Edition</a></li>

  <li><a href="https://www.packtpub.com/en-us/product/responsive-web-design-with-html5-and-css-fifth-edition/9781837028238">Responsive Web Design with HTML5 and CSS, Fifth Edition</a></li>
 
</ul>

</details>
