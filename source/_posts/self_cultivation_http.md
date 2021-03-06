---
title: 服务器开发自我修养专栏-HTTP深入浅出
date: 2021-01-12 19:08:06
tags:
- Self-cultivation
categories:
- Self-cultivation
---


# HTTP与HTTPS

HTTP 协议考察 HTTP 协议的返回码、HTTP 的方法等。需要特别指出的是 HTTPS 加密的详细过程要非常透彻，不然容易产生一种感觉好像都清楚了，但是一问就有点说不清楚。

下面实例是一点典型的使用GET来传递数据的实例,  
客户端请求：
```
GET /hello.txt HTTP/1.1
User-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3
Host: www.example.com
Accept-Language: en, mi
```
服务端响应:
```
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
ETag: "34aa387-d-1568eb00"
Accept-Ranges: bytes
Content-Length: 51
Vary: Accept-Encoding
Content-Type: text/plain
```
输出结果：
```
Hello World! My payload includes a trailing CRLF.
```

## 客户端请求消息

客户端发送一个HTTP请求到服务器的请求消息包括以下格式:  
* 请求行（request line）
* 请求头部（header）
* 空行
* 请求数据

由四个部分组成，下图给出了请求报文的一般格式。
![](/img/noodle_plan/http/client_request_header.png)


## 服务器响应消息

HTTP响应也由四个部分组成，分别是:  
* 状态行
* 消息报头
* 空行
* 响应正文

![](/img/noodle_plan/http/server_response_header.jpg)


## https

HTTPS 协议（HyperText Transfer Protocol over Secure Socket Layer）：一般理解为HTTP+SSL/TLS，通过 SSL证书来验证服务器的身份，并为浏览器和服务器之间的通信进行加密。

那么SSL/TLS又是什么？
* SSL（Secure Socket Layer，安全套接字层）：1994年为 Netscape 所研发，SSL 协议位于 TCP/IP 协议与各种应用层协议之间，为数据通讯提供安全支持。
* TLS（Transport Layer Security，传输层安全）：其前身是 SSL，它最初的几个版本（SSL 1.0、SSL 2.0、SSL 3.0）由网景公司开发，1999年从 3.1 开始被 IETF 标准化并改名，发展至今已经有 TLS 1.0、TLS 1.1、TLS 1.2 三个版本。SSL3.0和TLS1.0由于存在安全漏洞，已经很少被使用到。TLS 1.3 改动会比较大，目前还在草案阶段，目前使用最广泛的是TLS 1.1、TLS 1.2。

https 不是一种新的协议，只是 http 的通信接口部分使用了 ssl 和 tsl 协议替代，加入了加密、证书、完整性保护的功能，下面解释一下加密和证书，如下图所示
![](/img/noodle_plan/http/https_ssl.png)


### 对称加密

也叫**共享密钥加密**, 加密和解密公用一套秘钥，这样就会产生问题，已共享秘钥加密方式必须将秘钥传送给对方，但如果通信被监听，那么秘钥可能会被泄漏产生危险。  
常见对称加密算法有des, aes

### 非对称加密

也叫**公开秘钥加密**, 使用一种非对称加密的算法，使用一对非对称的秘钥，一把叫做公有秘钥，一把叫做私有秘钥，在加密的时候，通信的一方使用公有秘钥进行加密，通信的另一方使用私有秘钥进行解密，利用这种方式不需要发送私有秘钥，也就不存在泄漏的风险了。  
常见非对称加密算法有rsa


### https 加密方式

因为公开秘钥加密的方式比共享秘钥加密的方式钥消耗 cpu 资源，https 采取了混合加密的方式，来结合两者的优点。

在秘钥交换阶段使用公开加密的方式，之后建立连接后使用共享秘钥加密方式进行加密，如下图。

![](/img/noodle_plan/http/https_proc.png)


### 为什么要使用证书

因为公开加密还存在一些问题就是无法证明公开秘钥的正确性(有可能被黑客中间替换成了黑客自己的公钥, 然后黑客伪装成服务器/客户端做中间转发)，为了解决这个问题，https 采取了有数字证实认证机构和其相关机构颁发的公开秘钥证书，通信过程如下图所示。

![](/img/noodle_plan/http/https_ca.png)

解释一下上图的步骤：  
1. 服务器将自己的公开秘钥传到数字证书认证机构  
2. 数字证书认证机构使用自己的秘钥来对传来的服务器公钥进行加密，并颁发数字证书  
3. 服务器将传回的公钥证书发送给客户端，客户端使用数字机构颁发的公开秘钥来验证证书的有效性，以及公开秘钥的真实性
    * ![](/img/noodle_plan/linux/https_pub_key_credential_verify.jpg)
    * 证书签名是先将证书信息（证书机构名称、有效期、拥有者、拥有者公钥）进行hash，再用CA的私有密钥对hash值加密而生成的。
    * 所以拦截者虽然可以拦截并篡改证书信息（主要是拥有者和拥有者的公钥），但是由于拦截者没有CA的私钥，所以无法生成正确的签名，从而导致客户端拿到签名后，用CA公有密钥对证书签名解密后值与用证书计算出来的实际hash值不一样，从而得不到客户端信任。(其实这个ca公钥和私钥也就是非对称加密的思想了)
1. 客户端使用服务器的公开秘钥进行消息加密，后发送给服务器。  
2. 服务器使用私有秘钥进行解密。

浏览器在安装的时候会内置可信的数字证书机构的公开秘钥，如下图所示。

![](/img/noodle_plan/http/https_browser_ca.png)

这就是为什么我们使用自己生成的证书的时候会产生安全警告的原因。

再附一张 https 的具体通信步骤和图解。

![](/img/noodle_plan/http/https_hand_shake2.png)


## cookie

服务器发送的响应报文包含 Set-Cookie 首部字段，客户端得到响应报文后把 Cookie 内容保存到浏览器中。
```
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: yummy_cookie=choco
Set-Cookie: tasty_cookie=strawberry
```
客户端之后对同一个服务器发送请求时，会从浏览器中取出 Cookie 信息并通过 Cookie 请求首部字段发送给服务器。
```
GET /sample_page.html HTTP/1.1
Host: www.example.org
Cookie: yummy_cookie=choco; tasty_cookie=strawberry
```

Domain 标识指定了哪些主机可以接受 Cookie。如果不指定，默认为当前文档的主机（不包含子域名）。如果指定了 Domain，则一般包含子域名。例如，如果设置 Domain=mozilla.org，则 Cookie 也包含在子域名中（如 developer.mozilla.org）。

Path 标识指定了主机下的哪些路径可以接受 Cookie（该 URL 路径必须存在于请求 URL 中）。以字符 %x2F ("/") 作为路径分隔符，子路径也会被匹配。例如，设置 Path=/docs，则以下地址都会匹配：

* `/docs`
* `/docs/Web/`
* `/docs/Web/HTTP`


## session如何保存较好

![](/img/noodle_plan/http/session_server.jpg)

一个用户的 Session 信息如果存储在一个服务器上，那么当负载均衡器把用户的下一个请求转发到另一个服务器，由于服务器没有用户的 Session 信息，那么该用户就需要重新进行登录等操作..有什么好的解决方案呢?  
Session Server使用一个单独的服务器存储 Session 数据，可以使用传统的 MySQL，也使用 Redis 或者 Memcached 这种内存型数据库。  
* 优点：
    为了使得大型网站具有伸缩性，集群中的应用服务器通常需要保持无状态，那么应用服务器不能存储用户的会话信息。Session Server 将用户的会话信息单独进行存储，从而保证了应用服务器的无状态。
* 缺点：
    需要去实现存取 Session 的代码


## cookie和session和token的区别

![](/img/noodle_plan/http/cookie_session.png)

* **由于HTTP协议是无状态的协议，所以服务端需要记录用户的状态时，就需要用某种机制来识具体的用户，这个机制就是Session**.典型的场景比如购物车，当你点击下单按钮时，由于HTTP协议无状态，所以并不知道是哪个用户操作的，所以服务端要为特定的用户创建了特定的Session，用用于标识这个用户，并且跟踪用户，这样才知道购物车里面有几本书。这个Session是保存在服务端的，有一个唯一标识。在服务端保存Session的方法很多，内存、数据库、文件都有。集群的时候也要考虑Session的转移，在大型的网站，一般会有专门的Session服务器集群，用来保存用户会话，这个时候 Session 信息都是放在内存的，使用一些缓存服务比如Memcached之类的来放 Session。
* **思考一下服务端如何识别特定的客户？这个时候Cookie就登场了**。每次HTTP请求的时候，客户端都会发送相应的Cookie信息到服务端。实际上大多数的应用都是用 Cookie 来实现Session跟踪的，第一次创建Session的时候，服务端会在HTTP协议中告诉客户端，需要在 Cookie 里面记录一个Session ID，以后每次请求把这个会话ID发送到服务器，我就知道你是谁了。有人问，如果客户端的浏览器禁用了 Cookie 怎么办？一般这种情况下，会使用一种叫做URL重写的技术来进行会话跟踪，即每次HTTP交互，URL后面都会被附加上一个诸如 sid=xxxxx 这样的参数，服务端据此来识别用户。
* **Cookie其实还可以用在一些方便用户的场景下**，设想你某次登陆过一个网站，下次登录的时候不想再次输入账号了，怎么办？这个信息可以写到Cookie里面，访问网站的时候，网站页面的脚本可以读取这个信息，就自动帮你把用户名给填了，能够方便一下用户。这也是Cookie名称的由来，给用户的一点甜头。所以，总结一下：Session是在服务端保存的一个数据结构，用来跟踪用户的状态，这个数据可以保存在集群、数据库、文件中；Cookie是客户端保存用户信息的一种机制，用来记录用户的一些信息，也是实现Session的一种方式。
* **为什么需要token来替代session机制? 因为session的存储对服务器说是一个巨大的开销**， 严重的限制了服务器扩展能力， 比如说我用两个机器组成了一个集群， 小 F 通过机器 A 登录了系统， 那 session id 会保存在机器 A 上， 假设小 F 的下一次请求被转发到机器 B 怎么办？ 机器 B 可没有小 F 的 session id 啊。有时候会采用一点小伎俩： session sticky ， 就是让小 F 的请求一直粘连在机器 A 上， 但是这也不管用， 要是机器 A 挂掉了， 还得转到机器 B 去。 
 
接下来我们介绍事实上的token标准[JWT](#JWT)


### JWT

sessionId 的方式本质是把用户状态信息维护在 server 端，token 的方式就是把用户的状态信息加密成一串 token 传给前端，然后每次发请求时把 token 带上，传回给服务器端；服务器端收到请求之后，解析 token 并且验证相关信息(用jwt的header里的加密方式然后根据自己的不公开的密钥把jwt中的payload用加密一下得到一个签名 s, 然后用s对比看看是不是跟jwt里的signature相等, 相等则说明token对了)；

备注: 对于数据校验，专门的消息认证码生成算法, HMAC - 一种使用单向散列函数构造消息认证码的方法，其过程是不可逆的、唯一确定的，并且使用密钥来生成认证码，其目的是防止数据在传输过程中被篡改或伪造。将原始数据与认证码一起传输，数据接收端将原始数据使用相同密钥和相同算法再次生成认证码，与原有认证码进行比对，校验数据的合法性。

所以跟第一种登录方式最本质的区别是：通过解析 token 的计算时间换取了 session 的存储空间

业界通用的加密方式是 jwt, jwt 的具体格式如图：  
![](/img/noodle_plan/http/jwt1.png)
简单的介绍一下 jwt，它主要由 3 部分组成：
```
header 头部
{
  "alg": "HS256",
  "typ": "JWT"
}
payload 负载
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1555341649998
}
signature 签名
{
  HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  your-256-bit-secret
  ) secret base64 encoded
}
```

* header  
    header 里面描述加密算法和 token 的类型，类型一般都是 JWT；
* payload
    里面放的是用户的信息，也就是第一种登录方式中需要维护在服务器端 session 中的信息；
* signature
    是对前两部分的签名，也可以理解为加密；实现需要一个密钥（secret），这个 secret 只有服务器才知道，然后使用 header 里面的算法按照如下方法来加密：
    ``` python
    HMACSHA256(
    base64UrlEncode(header) + "." +
    base64UrlEncode(payload),
    secret)
    ```

总之，最后的 `jwt = base64url(header) + "." + base64url(payload) + "." + signature`  
jwt 可以放在 response 中返回，也可以放在 cookie 中返回，这都是具体的返回方式，并不重要。  
客户端发起请求时，官方推荐放在 HTTP header 中：
```
Authorization: Bearer <token>
```
这样子确实也可以解决 cookie 跨域(比如移动平台上对cookie支持不好)的问题，不过具体放在哪儿还是根据业务场景来定，并没有一定之规。


#### jwt过期了如何刷新

**前面讲的 Token，都是 Access Token，也就是访问资源接口时所需要的 Token，还有另外一种 Token，Refresh Token，**通常情况下，Refresh Token 的有效期会比较长，而 Access Token 的有效期比较短，当 Access Token 由于过期而失效时，使用 Refresh Token 就可以获取到新的 Access Token，如果 Refresh Token 也失效了，用户就只能重新登录了。

在 JWT 的实践中，引入 Refresh Token，将会话管理流程改进如下:
1. 客户端使用用户名密码进行认证
2. 服务端生成有效时间较短的 Access Token（例如 10 分钟），和有效时间较长的 Refresh Token（例如 7 天）
3. 客户端访问需要认证的接口时，携带 Access Token
4. 如果 Access Token 没有过期，服务端鉴权后返回给客户端需要的数据
5. 如果携带 Access Token 访问需要认证的接口时鉴权失败（例如返回 401 错误），则客户端使用 Refresh Token 向刷新接口申请新的 Access Token
6. 如果 Refresh Token 没有过期，服务端向客户端下发新的 Access Token
7. 客户端使用新的 Access Token 访问需要认证的接口


## 常见的HTTP相应状态码

总之：(一般标准用法是这样用哈, 但是真的写代码的时候其实跟get/post/put一样, 想怎么用全看自己, 前后端开发人员协商好就行)

* 1XX：消息
* 2XX：成功
* 3XX：重定向
* 4XX：请求错误
* 5XX、6XX：服务器错误

常见状态代码、状态描述的说明如下:

* 200 OK:
请求已成功，请求所希望的响应头或数据体将随此响应返回。实际的响应将取决于所使用的请求方法。在GET请求中，响应将包含与请求的资源相对应的实体。在POST请求中，响应将包含描述或操作结果的实体。[7]
* 301 Moved Permanently:
被请求的资源已永久移动到新位置，并且将来任何对此资源的引用都应该使用本响应返回的若干个URI之一。如果可能，拥有链接编辑功能的客户端应当自动把请求的地址修改为从服务器反馈回来的地址。[19]除非额外指定，否则这个响应也是可缓存的。
新的永久性的URI应当在响应的Location域中返回。除非这是一个HEAD请求，否则响应的实体中应当包含指向新的URI的超链接及简短说明。
如果这不是一个GET或者HEAD请求，那么浏览器禁止自动进行重定向，除非得到用户的确认，因为请求的条件可能因此发生变化。
注意：对于某些使用HTTP/1.0协议的浏览器，当它们发送的POST请求得到了一个301响应的话，接下来的重定向请求将会变成GET方式。
* 400 Bad Request
由于明显的客户端错误（例如，格式错误的请求语法，太大的大小，无效的请求消息或欺骗性路由请求），服务器不能或不会处理该请求。[31]
* 401 Unauthorized（RFC 7235）
参见：HTTP基本认证、HTTP摘要认证
类似于403 Forbidden，401语义即“未认证”，即用户没有必要的凭据。[32]该状态码表示当前请求需要用户验证。该响应必须包含一个适用于被请求资源的WWW-Authenticate信息头用以询问用户信息。客户端可以重复提交一个包含恰当的Authorization头信息的请求。[33]如果当前请求已经包含了Authorization证书，那么401响应代表着服务器验证已经拒绝了那些证书。如果401响应包含了与前一个响应相同的身份验证询问，且浏览器已经至少尝试了一次验证，那么浏览器应当向用户展示响应中包含的实体信息，因为这个实体信息中可能包含了相关诊断信息。
注意：当网站（通常是网站域名）禁止IP地址时，有些网站状态码显示的401，表示该特定地址被拒绝访问网站。
* 403 Forbidden
主条目：HTTP 403
服务器已经理解请求，但是拒绝执行它。与401响应不同的是，身份验证并不能提供任何帮助，而且这个请求也不应该被重复提交。如果这不是一个HEAD请求，而且服务器希望能够讲清楚为何请求不能被执行，那么就应该在实体内描述拒绝的原因。当然服务器也可以返回一个404响应，假如它不希望让客户端获得任何信息。
* 404 Not Found
主条目：HTTP 404
请求失败，请求所希望得到的资源未被在服务器上发现，但允许用户的后续请求。[35]没有信息能够告诉用户这个状况到底是暂时的还是永久的。假如服务器知道情况的话，应当使用410状态码来告知旧资源因为某些内部的配置机制问题，已经永久的不可用，而且没有任何可以跳转的地址。404这个状态码被广泛应用于当服务器不想揭示到底为何请求被拒绝或者没有其他适合的响应可用的情况下。
* 500 Internal Server Error
通用错误消息，服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。没有给出具体错误信息。[59]
* 503 Service Unavailable
由于临时的服务器维护或者过载，服务器当前无法处理请求。这个状况是暂时的，并且将在一段时间以后恢复。[62]如果能够预计延迟时间，那么响应中可以包含一个Retry-After头用以标明这个延迟时间。如果没有给出这个Retry-After信息，那么客户端应当以处理500响应的方式处理它。


## get和post的本质区别

从设计初衷上来说，GET 用来实现从服务端取数据，POST 用来实现向服务端提出请求对数据做某些修改，也因此如果你向nginx用post请求静态文件，nginx会直接返回 405 not allowed，但是服务端毕竟是人实现的，你可以让 POST 做 GET 相同的事情

get请求的参数一般放在url中，但是浏览器和服务器程序对url长度还是有限制的。
post请求的参数一般放在body，你硬要放到url中也可以。

在RESTful风格中，get用于从服务器获获取数据，而post用于创建数据


## Connection: keep-alive

在早期的HTTP/1.0中，每次http请求都要创建一个连接，而创建连接的过程需要消耗资源和时间，为了减少资源消耗，缩短响应时间，就需要重用连接。在后来的HTTP/1.0中以及HTTP/1.1中，引入了重用连接的机制，就是在http请求头中加入Connection: keep-alive来告诉对方这个请求响应完成后不要关闭，下一次咱们还用这个请求继续交流。协议规定HTTP/1.0如果想要保持长连接，需要在请求头中加上Connection: keep-alive，而HTTP/1.1默认是支持长连接的，有没有这个请求头都行。

要实现长连接很简单，只要客户端和服务端都保持这个http长连接即可。但问题的关键在于保持长连接后，浏览器如何知道服务器已经响应完成？在使用短连接的时候，服务器完成响应后即关闭http连接，这样浏览器就能知道已接收到全部的响应，同时也关闭连接（TCP连接是双向的）。

在使用长连接的时候，响应完成后服务器是不能关闭连接的，那么它就要在响应头中加上特殊标志告诉浏览器已响应完成。一般情况下这个特殊标志就是Content-Length，来指明响应体的数据大小，比如Content-Length: 120表示响应体内容有120个字节，这样浏览器接收到120个字节的响应体后就知道了已经响应完成。

由于Content-Length字段必须真实反映响应体长度，但实际应用中，有些时候响应体长度并没那么好获得，例如响应体来自于网络文件，或者由动态语言生成。这时候要想准确获取长度，只能先开一个足够大的内存空间，等内容全部生成好再计算。但这样做一方面需要更大的内存开销，另一方面也会让客户端等更久。这时候Transfer-Encoding: chunked响应头就派上用场了，该响应头表示响应体内容用的是分块传输，此时服务器可以将数据一块一块地分块响应给浏览器而不必一次性全部响应，待浏览器接收到全部分块后就表示响应结束。

以分块传输一段文本内容：“人的一生总是在追求自由的一生 So easy”来说明分块传输的过程，如下图所示:
![](/img/noodle_plan/http/http_alive.png)


## url编码urlencode是什么

RFC3986文档规定，Url中只允许包含英文字母（a-zA-Z）、数字（0-9）、-_.~4个特殊字符以及所有保留字符。  
那如何对Url中的非法字符进行编码呢? 
  
**Url编码通常也被称为百分号编码（Url Encoding，also known as percent-encoding），是因为它的编码方式非常简单，使用%百分号加上两位的字符——0123456789ABCDEF——代表一个字节的十六进制形式**。Url编码默认使用的字符集是US-ASCII。例如a在US-ASCII码中对应的字节是0x61，那么Url编码之后得到的就是%61，我们在地址栏上输入http://g.cn/search?q=%61%62%63，

实际上就等同于在google上搜索abc了。又如@符号在ASCII字符集中对应的字节为0x40，经过Url编码之后得到的是%40。
  
  对于非ASCII字符，需要使用ASCII字符集的超集进行编码得到相应的字节，然后对每个字节执行百分号编码。对于Unicode字符，RFC文档建议使用utf-8对其进行编码得到相应的字节，然后对每个字节执行百分号编码。如"中文"使用UTF-8字符集得到的字节为0xE4 0xB8 0xAD 0xE6 0x96 0x87，经过Url编码之后得到"%E4%B8%AD%E6%96%87"。
  
  如果某个字节对应着ASCII字符集中的某个非保留字符，则此字节无需使用百分号表示。例如"Url编码"，使用UTF-8编码得到的字节是0x55 0x72 0x6C 0xE7 0xBC 0x96 0xE7 0xA0 0x81，由于前三个字节对应着ASCII中的非保留字符"Url"，因此这三个字节可以用非保留字符"Url"表示。最终的Url编码可以简化成"Url%E7%BC%96%E7%A0%81" ，当然，如果你用"%55%72%6C%E7%BC%96%E7%A0%81"也是可以的。

很多HTTP监视工具或者浏览器地址栏等在显示Url的时候会自动将Url进行一次解码（使用UTF-8字符集），这就是为什么当你在Firefox中访问Google搜索中文的时候，地址栏显示的Url包含中文的缘故。但实际上发送给服务端的原始Url还是经过编码的。

