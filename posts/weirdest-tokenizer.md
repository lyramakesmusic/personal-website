
# Finding the weirdest tokenizer

Tokenizers are the first layer of language modeling in the LLM stack. They compress common byte patterns, such as words, stems, or punctuation, into single tokens to save the transformer the effort of assembling each word character by character. The most compressible data in the corpus hits the tokenizer first, meaning the tokenizer itself is already a lossy model of its training data. They capture whatever is common enough to merge, whatever co-occurs, whatever gets repeated enough to get fused, etc etc. The internet is full of enough spam and repeated phrases that surely some tokenizers would compress the entire things as single tokens. So which tokenizer has the strangest single tokens? Do any encode whole copypastas? Is it code patterns or SEO spam?

---

The now-famous glitch tokens from GPT-2 / OPT / Phi-2 (`SolidGoldMagikarp`, `BuyableInstoreAndOnline`, `rawdownloadcloneembedreportprint`, `petertodd`, etc) inspired me to search for other oddities in tokenizers, things that have no right to have a dedicated token but made it in anyways. So I crawled around on huggingface, downloading as many unique tokenizers as I could find, and with the help of Claude, filtered for interesting ones.

There were fewer interesting tokenizers than I expected, for two reasons - there is a lot of tokenizer re-use, so the candidate pool started out narrow, and modern tokenizers use better filtering and grouping algorithms, eliminating the weird stuff before it can calcify into single tokens. 

However, we found some gems anyways, in particular one 2023-era chinese model with the longest, strangest tokens of anything. 

## long tokens (not quite weird yet)

GLM-4 has a 512-character whitespace token (and a 256-char one) - 112972 & 105313

cl100k_base, used by GPT-4 (extended by Llama 3 and Qwen), has several long strings, mostly coding related:

> `.translatesAutoresizingMaskIntoConstraints` - iOS Swift/UIKit stuff. This is the longest coherent english token I found across major tokenizers.
> 
> `.DataGridViewColumnHeadersHeightSizeMode` - C# WinForms stuff
> 
> `dequeueReusableCellWithIdentifier` - iOS UITableView method

BLOOM has several more:

> `{\fnZhunYuan\fs23\bord2\shad3\1cH0080FF\3cHFFFFFF}` - ASS subtitle string
> 
> `android:layout_height="match_parent"` - apparently enough android code contains this to deserve its own token
> 
> `&rcy;&ucy;&scy;&scy;&kcy;&icy;&jcy;` - "русский" ("Russian") spelled out in HTML entities

MiniCPM has a lot of legal boilerplate as single tokens:

> `至今未履行生效法律文书确定的义务` ("has not fulfilled obligations determined by effective legal documents")
>
> `经本院合法传唤无正当理由拒不到庭` ("after lawful summons by this court, refused to appear without valid reason")
>
> `但债权的实现取决于被执行人是否有` ("but realization of the claim depends on whether the person subject to execution has...")

## o200k_base (getting weird)

The GPT-4o tokenizer famously is packed full of porn and gambling SEO strings encoded as single tokens. This one has been reported on extensively already, so I won't show all its highlights, read the paper if you want to see the full extent of the spam:

[Speculating LLMs’ Chinese Training Data Pollution from Their Tokens (Zhang et al.)](https://arxiv.org/pdf/2508.17771v1)

A couple examples to get a vibe for it

> **185118:** `_日本毛片免费视频观看` ("free Japanese porn video viewing")
> 
> **8089:** `天天中彩票` ("Daily Lottery Win" - various combinations/repetitions of this show up in ~80 other tokens as well)
> 
> **3847:** `彩神争霸` ("God of Lottery" or "Lottery God Battle")

... and many many more. 

Not satisfied with the o200k_base porn and gambling spam, I looked into more obscure older models. I figured that earlier models would use more unfiltered data and put fewer restrictions on what kinds of tokens could be created. 

Which led me to find:

---

# Baichuan2.

[baichuan-inc/Baichuan2-7B-Chat (*2023*)](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat)

Apparently they fed this poor thing unfiltered WeChat. It inhaled the whole corpus, spam and all, and aggressively chunked it with seemingly no restrictions on what could become a token, resulting in some of the longest, spammiest single tokens out of anything.

The cultural strata compressed here is fascinating - for something to get chunked into a single token it must be seen frequently enough for whatever BPE algo they use to merge it together. More discussion on this at the end.

To properly appreciate the breadth of this thing, I separated them into categories: single tokens that are clearly someone mashing a chinese predictive keyboard, merge ladders (the same string repeated 1x, 2x, 4x, 8x, each getting a single token), WeChat follow-bait template spam, complete sentences from essays/articles, political templates, and other oddities.

## Keymashing / word salad

> **74899:** `哈酒圣诞节后视镜爱护动物和东方红届时将会找机会撒啊啊啊啊啊撒的发` ("drinking / Christmas / rearview mirror / animal protection / East is Red / aaaaaah")
> 
> **74757:** `加胡椒粉和骄傲善举和积分卡技术放假时间繁花似锦胡椒粉和说句话家具` ("add pepper powder / pride / charity / loyalty card / holiday time / splendid flowers / pepper powder / say something / furniture")
> 
> **74792:** `健身房就撒娇背景下长时间粉红色就像你这么说就回房间杀菌和` ("gym / acting cute / background / long time / pink / just like you said / go back to room / sterilize")
> 
> **74721:** `服务法师事实上事实上事实上发反反复复飞放不下就带回家` ("service mage / actually actually actually / back and forth / fly / can't let go / bring home")
> 
> **74768:** `骄傲和武汉分手机话费交换机和福建省` ("pride and Wuhan / phone bill / switchboard / Fujian Province")

## Merge ladders

> **11923/11956/19782/33165:** `詹飘飘` x1, x2, x4, and x8
("Zhan Piaopiao" - someone's name repeated)
> 
> **4846/4974/8154/13615:** `网络配图` x1, x2, x4, and x8 ("Stock Photo" / "image from internet")
> 
> **24543/24659/41521/69672:** `灵异吧` x1, x2, x4, and x8 ("Paranormal forum" - Baidu Tieba subforum)
> 
> **10939/12844/21876/38904:** `反反复复` x1, x2, x4, and x8 ("back and forth" / "repeatedly")
>
> **29337/49447/83098:** `禄劝` x2, x4, and x8 ("Luquan" - a county in Yunnan)
>
> **33676/75528:** `哈` x8 and x16 ("hahaha" - `哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈` is a single token)
> 
> **22399/22407/22459/22973:** `让人心痛的话欢迎各位朋友回家感谢你们的鼎力支持...`  ("Heartbreaking words, welcome friends home, thank you for your support..." split at 12, 23, 28, and 32 characters - viral post eaten by BPE chunking)
> 
> **22623/26671/74690/74901:** `大幅度发` x1, x2, x4, and x5 ("largely send")

That last one breaks the powers-of-2 pattern with a 5x repetition. Token 74930 (`大幅度发大幅度发大幅度发大幅度发大幅度发基本圣诞节氨甲环酸` - `大幅度发` x5 followed by "basic Christmas tranexamic acid") also has a 5-repetition.

## WeChat spam / follow bait

> **75600:** `微信关注博野在线微信关注博野在线微信关注博野在线微信关注博野在线` ("Follow Boye Online on WeChat" repeated x4)
> 
> **75535:** `微信公众号微信公众号微信公众号微信公众号` ("WeChat public account" repeated x4)
> 
> **38717:** `这样您就可以继续免费收到最新文章了` ("This way you can keep receiving the latest articles for free!")
> 
> **33439:** `请您先点击上面的蓝色字体` ("Please click the blue text above first")
> 
> **19280:** `长按上方二维码识别关注` ("Long press the QR code above to scan and follow")
> 
> **37548:** `分享给身边的朋友一起关注吧` ("Share with friends around you and follow together!")
> 
> **71412:** `你们是小编前进的动力哦` ("You guys are what keeps this little editor going!")
> 
> **37210:** `我都会在这里陪伴着你` ("I'll always be here with you")
> 
> **83045:** `不要盲目的去追求她如果你想追一个女孩的话` ("Don't blindly chase her, if you want to pursue a girl..." - dating advice copypasta fragment)
>
> **17378:** `这世间凡事都能说个明白唯有人和人之间的感情例外` ("Everything in this world can be explained, except for feelings between people")

## Copyright disclaimers

> **75591:** `版权归原作者及原出处所有` ("copyright belongs to original author and source")
> 
> **18934:** `若有来源标注错误或侵犯了您的合法权益` ("if source attribution is wrong or infringes on your legal rights")
> 
> **89667:** `本平台将更正来源及作者或依据著作权人意见` ("this platform will correct source and author per copyright holder's wishes")
> 
> **33298:** `请在后台留言联系我们进行删除` ("please leave a backend message to contact us for deletion")
> 
> **21239:** `转载此文是出于传递更多信息之目的` ("reposting this article is for the purpose of conveying more information")

## Essays, posts, etc

An entire parable about humility got tokenized into about 20 total tokens. A few of them:

> **39242:** `高高的堂叔到我家串门的时候` ("When my tall uncle came to visit my home")
> 
> **37971:** `说着就低着头迈进了门槛` ("saying this, he ducked his head and stepped through the doorframe")
> 
> **35262:** `就会被碰头甚而被碰得头破血流` ("you'll bump your head, even crack it open and bleed")
> 
> **34190:** `有时需要我们昂首阔步` ("sometimes we need to stride forward with heads held high")
> 
> **34188:** `有时需要我们低头弯腰` ("sometimes we need to bow our heads and bend down")
> 
> **34152:** `才能跨过这道关键的门槛` ("in order to cross this crucial threshold")

Another post about the epiphyllum got tokenized in full:

> **79270:** `未开放时绛紫色的花苞象小家碧玉` ("Before blooming, the crimson-purple buds are like a modest beauty")
> 
> **78696:** `一点一点地展现它的秀色` ("bit by bit revealing its beauty")
> 
> **79258:** `它有着别的花所不及的气度` ("it has a grace that no other flower can match")
> 
> **76284:** `闭谢的姿势也刚烈异常` ("even its closing posture is fierce and resolute")

The Heart Sutra as well:

> **85397:** `得阿耨多罗三藐三菩提` ("attain Anuttara Samyak Sambodhi")
> 
> **87754:** `故说般若波罗蜜多咒` ("therefore proclaim the Prajnaparamita mantra")
> 
> **76174:** `行深般若波罗蜜多时` ("practicing deep Prajnaparamita")

And a copypasta about "How many times...":

> **36703:** `有多少句我爱你` ("how many 'I love you's")
> 
> **37065:** `有多少句对不起` ("how many 'I'm sorry's")
> 
> **37068:** `有多少句没关系` ("how many 'it's okay's")
> 
> **38741:** `最后说了谢谢你有多少句我爱你` ("finally said thank you, how many 'I love you's")

## Political etc

> **80354:** `新型冠状病毒感染的肺炎疫情防控指挥部` ("Novel Coronavirus Pneumonia Epidemic Prevention and Control Command Center")

Multiple variations of this appeared, this same phrase got trimmed at different lengths and each one got a unique token.

> **82867:** `坚持以习近平新时代中国特色社会主义思想为指导` ("Uphold Xi Jinping Thought on Socialism with Chinese Characteristics for a New Era as guidance")

Again, multiple variations of this with different lengths/cutoffs exist as unique tokens.

## Other oddities

> **90759:** `ۥۛۛ۟ۙۙۚۥۚۙۙۙۚۥۛۛۚۚۛ۟ۡۥۛ۟ۡۗۡ` (Urdu diacritical marks - Quranic annotation signs!! Recitation markup with the letters stripped out)
> 
> **26431:** `iongmaoqiongmaoqiongmaoqiongmaoq` (repeated garbled pinyin of "穷猫"/"poor cat", sliced *after* the leading Q for some reason)
> 
> **74569:** `dingxingshenghuoquan` (pinyin of "定兴生活圈"/"Dingxing Life Circle", seemingly a local WeChat public account name. Apparently it's from the same region as the Boye Online spam - what is going on in Héběi?)
> 
> **85217:** `邓州论坛邓州论邓州论坛邓州论坛邓州` ("Dengzhou Forum" repeated, but with truncation artifacts. "Dengzhou Forum Dengzhou For Dengzhou Forum Dengzhou Forum Dengzhou")
> 
> **64924:** `城市网邓州城市网邓州城市网邓州城市网邓州` ("City Net Dengzhou" repeated 4x)

---

# what if there was a markov chain on merges

After poking around for long weird tokens, I thought since the tokenizer comes with a merge list, and the order of the merge list is roughly correlated with frequency, it should be possible to construct a really awkward markov chain to do tokenizer-only language modeling. Naturally, it's going to devolve instantly into word soup, with little to no grammatical structure gluing it together. However, I was interested in finding out what vibe-corners each chain would land in via free-association, and whether the full sentences so prevalent in baichuan would produce anything interesting.

When I tried the naive merge-list order weighting, every chain devolved into english bigram soup. `a` had score -1 and `疫情防控` has score -2328 (negative merge rank), so english subwords vastly outweighed chinese tokens. 

To create more interesting chains, I tried ignoring the merge order weights entirely, instead setting the weight of each bigram to how many different tokens in the vocab contain it. For instance, `工→作` is weighted highly because it appears in `工作`, `工作人员`, `工作者`, `工作组`, `工作中`, `工作日`, etc, while a rare bigram like `菩→提` might only appear in a couple tokens.

Trying this method, every random start converged within ~5 tokens to:

> `一个` → `人员` → `工作` → `为了` → `一个` → `人员` → `工作` → `为了` → ...
> 
> "A personnel worker for the sake of a personnel worker for the sake of..."

Some other attractors that raw markov sampling fell into:

> `要求职业务院校园区域...` ("require employment business academy campus area")
> 
> `等等等等等等等...` ("etcetera" maps to itself)
> 
> `啦啦啦啦啦啦啦...` 

The most common functional bigrams became an intense attractor state. So, I needed some auxiliary weighting / sampling methods. Like any other markov chain, I tried using ngram blocking, temperature, and length weighting. Combinations of these settings led to some crazy sequences. 

The best settings for getting semicoherent vibe word soup were something like:

- ngram-blocking 20 - can only repeat after sampling 20 other tokens first.
- log-length bias - weighting each token by `log(1 + len(token))` prefers longer tokens while still allowing shorter functional tokens (的, 了, 一) as glue. 
- temp 1.2

They led to walks like these:

**Seed 42, ngram-block 50, starting with 3079 `各位朋友` ("friends"):**

> 各位朋友回家后成型的其他的事儿的人生前些年了一下水瓶座的重要的用户的需求的问候就不知里面有什么不争中央党校的伟大战机的意思是孩子课后的很重要讲话精神的话题的对象的计划和学习的一般的公众号的一点这也是一寸含量安全风险公证的方式进行一个好的想看一觉上班车上的政策的家中大的父亲属羊肉眼的主要不锈钢结石油菜单个...
> 
> Friends, after coming home, the molded other things of life, years ago, a splash, Aquarius, the important user's needs, greetings — not knowing what's inside, no contest, the Central Party School's great fighter jet's meaning is children after class, the very important speech spirit, the topic's object, the plan and study, the general public account, a little, this is also one inch, content, safety risk, notarization, the way to proceed, a good one, want to watch, one nap, commuting, on the bus, the policy, at home, middle-large, the father, year of the sheep, naked eye, the main, stainless steel, kidney stones, rapeseed, individually...

**Seed 99999, ngram-block 20, log length bias, and T=1.2, starting with 14683 `这世间` ("in this world"):**

> 这世间凡事都能说个明白唯有人和人之间的感情例外教育行政部门的密切接触者在这种情况下图片来源于网络安全生产工作中级人民法院联防联控机制中国疾控中心全员核酸检测定点医疗机构和人之间的感情例外在我们实现美好理想和远大目标的征途上进口冷链食品有时还会留下遗憾的重要组成部分公务员录用体检疫情防控工作的唯有人和人之间的感情例外人民代表大会说着就低着头迈进了我都会在这里有多少句对不起关于进一步加强 [... middle omitted ...] 都低下了昂贵的头发热门诊就诊就不知里面有什么风景和奇特的构造假如进洞口时不低头市场监管总局长按上方二维码识别关注微信公众平台市场监管部门市人大常委会和新疆生产建设兵团
> 
> "Everything in this world can be explained, except for feelings between people." Education administrative department. Close contacts. Under these circumstances. Image sourced from the internet. Workplace safety work. Intermediate people's court. Joint prevention and control mechanism. China CDC. Full-staff nucleic acid testing. Designated medical institutions. "Except for feelings between people." On our journey to realize beautiful ideals and grand goals. Imported cold-chain food products. Sometimes you'll even leave behind regrets. An important component of. Civil servant recruitment physical examination. COVID prevention and control work. "Only feelings between people are the exception." People's congress. Saying this, he ducked his head and stepped through. I'll always be here. How many "I'm sorry"s. Regarding further strengthening. [...] Everyone lowered their expensively-coiffed heads. Visit the fever clinic. Not knowing what scenery and strange formations lie inside. If you don't duck at the cave entrance. State Administration for Market Regulation. Long press the QR code above to scan and follow. WeChat public platform. Market supervision department. Municipal people's congress standing committee. And the Xinjiang Production and Construction Corps.

I tried this same method on other tokenizers - Deepseek v3, GPT-4o, Mistral (32k) - with mixed results. None were as interesting as Baichuan2, although their individual failure modes were revealing. Filtering out the english bigram-soup walks:

Deepseek stayed in coherent chinese for 50+ tokens. Its tokenizer is too clean to produce anything but clean word soup.

o200k_base wrote ~5 tokens of chinese and then fell into porn SEO tokens. Another run devolved into pirated software download phrase spam. (to be fair I was weighting up the haha funny tokens on purpose)

Mistral *immediately* switched to russian: `тре|лок|уче|лось|свои...`. Mistral has no chinese tokens for `作`, so the byte representation immediately dragged it into cyrillic. 

---

## Why are so many of these odd tokens in Mandarin?

Chinese tokens are uniquely readable. Unlike English BPE fragments (or many other languages), each character is a morpheme, so each token makes sense on its own. `灵异吧|灵异吧|灵异吧|灵活性` is fully parseable, while english subword fragments (`ierra|respective|type|les|ice`) combine to noise. Weirdness scales with length and readability, and chinese tokens compress much more information per token than english (or other latin-ish scripts). 

Chinese also has the specific structural property of short semantic units concatenated without spaces, which means BPE merges produce meaningful compound tokens much more readily. English BPE tends to merge morphological pieces (suffix-prefix patterns, common word stems) that don't read as content; chinese BPE merges phrase-fragments that do. `公务员录用体检通用标准` is legible as a phrase ("civil service recruitment physical examination general standard") in a way that no equivalent english BPE merge would be. English would give you `ployment|procedure|candidates` as separate tokens rather than the whole phrase at once.

The equivalent english version with a tokenizer greedy enough to capture full phrases, would probably contain phrases like "Edit: thanks for the gold", "Subscribe and hit the bell", etc. They would be understandable but flatter than the chinese versions, because english spam is flatter than the chinese equivalent. The particular brand of parasocial engagement bait, bureaucratic-personal register collisions, the aspirational-poetic flourishes tacked onto advertorials are cultural fossils currently not really present in english. 

Japanese would be interesting for similar reasons - whole morphemes, multiple writing systems, dense register markers, etc. However, the content ecosystem would be completely different. The usual suspects would be manga, light novel boilerplate, politeness-level markers, and so on. 

In each case, a greedy tokenizer is inadvertently an ethnography of the underlying data it inhaled. Baichuan2 ate unfiltered WeChat and compressed an entire cultural strata in the process. o200k_base reveals how dense the gambling and porn spam is, archived by an indiscriminate BPE. Mistral compressed clean code and documentation, filtering the spam, and the sanitation shows in its markov walks.

