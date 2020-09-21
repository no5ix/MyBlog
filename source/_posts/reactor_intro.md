---
title: Reactor模式讲解
date: 2016-08-07 23:01:00
tags:
- NP
- DesignPattern
categories:
- NP
---


关于服务器模型总结请转 {% post_link server_model_summary 此文 %}
, 文中也有Reactor的讲解.

对于 IO 来说，我们听得比较多的是:

*   BIO: 阻塞 IO
*   NIO: 非阻塞 IO
*   同步 IO
*   异步 IO

以及其组合:

*   同步阻塞 IO
*   同步非阻塞 IO
*   异步阻塞 IO
*   异步非阻塞 IO

. . . <!-- more -->

**那么什么是阻塞 IO、非阻塞 IO、同步 IO、异步 IO 呢？**

*   一个 IO 操作其实分成了两个步骤：发起 IO 请求和实际的 IO 操作
*   阻塞 IO 和非阻塞 IO 的区别在于第一步：发起 IO 请求是否会被阻塞，如果阻塞直到完成那么就是传统的阻塞 IO; 如果不阻塞，那么就是非阻塞 IO
*   同步 IO 和异步 IO 的区别就在于第二个步骤是否阻塞，如果实际的 IO 读写阻塞请求进程，那么就是同步 IO，因此阻塞 IO、非阻塞 IO、IO 复用、信号驱动 IO 都是同步 IO; 如果不阻塞，而是操作系统帮你做完 IO 操作再将结果返回给你，那么就是异步 IO

举个不太恰当的例子 ：比如你家网络断了，你打电话去中国电信报修！

*   你拨号 --- 客户端连接服务器
*   电话通了 --- 连接建立
*   你说：“我家网断了, 帮我修下”--- 发送消息
*   说完你就在那里等，那么就是阻塞 IO
*   如果正好你有事，你放下带电话，然后处理其他事情了，过一会你来问下，修好了没 --- 那就是非阻塞 IO
*   如果客服说：“马上帮你处理，你稍等”--- 同步 IO
*   如果客服说：“马上帮你处理，好了通知你”，然后挂了电话 --- 异步 IO

本文只讨论 BIO 和 NIO,AIO 使用度没有前两者普及，暂不讨论！

下面从代码层面看看 BIO 与 NIO 的流程!

# BIO


模型图如下所示：

![](/img/reactor_intro/1100082-66c781ba3d47fa40.png)

## BIO 优缺点

*   优点
    *   模型简单
    *   编码简单
*   缺点
    *   性能瓶颈低

优缺点很明显。这里主要说下缺点：主要瓶颈在线程上。每个连接都会建立一个线程。虽然线程消耗比进程小，但是一台机器实际上能建立的有效线程有限，以 Java 来说，1.5 以后，一个线程大致消耗 1M 内存！且随着线程数量的增加，CPU 切换线程上下文的消耗也随之增加，在高过某个阀值后，继续增加线程，性能不增反降！而同样因为一个连接就新建一个线程，所以编码模型很简单！

就性能瓶颈这一点，就确定了 BIO 并不适合进行高性能服务器的开发！像 Tomcat 这样的 Web 服务器，从 7 开始就从 BIO 改成了 NIO，来提高服务器性能！

# NIO


NIO 模型示例如下：

![](/img/reactor_intro/1100082-8d8ec4d8b63f6d72.png)

*   Acceptor 注册 Selector，监听 accept 事件
*   当客户端连接后，触发 accept 事件
*   服务器构建对应的 Channel，并在其上注册 Selector，监听读写事件
*   当发生读写事件后，进行相应的读写处理

## NIO 优缺点

*   优点
    *   性能瓶颈高
*   缺点
    *   模型复杂
    *   编码复杂
    *   需处理半包问题

NIO 的优缺点和 BIO 就完全相反了! 性能高，不用一个连接就建一个线程，可以一个线程处理所有的连接！相应的，编码就复杂很多，从上面的代码就可以明显体会到了。还有一个问题，由于是非阻塞的，应用无法知道什么时候消息读完了，就存在了半包问题！

### 半包问题

简单看一下下面的图就能理解半包问题了！

![](/img/reactor_intro/1100082-bf61aee347d92676.png) ![](/img/reactor_intro/1100082-4da274ccb55084d9.png)

我们知道 TCP/IP 在发送消息的时候，可能会拆包 (如上图 1)！这就导致接收端无法知道什么时候收到的数据是一个完整的数据。例如: 发送端分别发送了 ABC,DEF,GHI 三条信息，发送时被拆成了 AB,CDRFG,H,I 这四个包进行发送，接受端如何将其进行还原呢？在 BIO 模型中，当读不到数据后会阻塞，而 NIO 中不会! 所以需要自行进行处理! 例如，以换行符作为判断依据，或者定长消息发生，或者自定义协议！

NIO 虽然性能高，但是编码复杂，且需要处理半包问题！为了方便的进行 NIO 开发，就有了 Reactor 模型!

# Reactor 模型

*   AWT Events

![](/img/reactor_intro/1100082-e108abfcd9382eef.jpg)

Reactor 模型和 AWT 事件模型很像，就是将消息放到了一个队列中，通过异步线程池对其进行消费！

## Reactor 中的组件

*   Reactor:Reactor 是 IO 事件的派发者。
*   Acceptor:Acceptor 接受 client 连接，建立对应 client 的 Handler，并向 Reactor 注册此 Handler。
*   Handler: 和一个 client 通讯的实体，按这样的过程实现业务的处理。一般在基本的 Handler 基础上还会有更进一步的层次划分， 用来抽象诸如 decode，process 和 encoder 这些过程。比如对 Web Server 而言，decode 通常是 HTTP 请求的解析， process 的过程会进一步涉及到 Listener 和 Servlet 的调用。业务逻辑的处理在 Reactor 模式里被分散的 IO 事件所打破， 所以 Handler 需要有适当的机制在所需的信息还不全（读到一半）的时候保存上下文，并在下一次 IO 事件到来的时候（另一半可读了）能继续中断的处理。为了简化设计，Handler 通常被设计成状态机，按 GoF 的 state pattern 来实现。

对应上面的 NIO 代码来看:

*   Reactor：相当于有分发功能的 Selector
*   Acceptor：NIO 中建立连接的那个判断分支
*   Handler：消息读写处理等操作类

Reactor 从线程池和 Reactor 的选择上可以细分为如下几种：

## Reactor 单线程模型

![](/img/reactor_intro/1100082-931396ffc90437ef.png)

如果上图表达得不够明白, 还可以看看下图

![](/img/reactor_intro/basic_reactor_design.jpg)

如果上图还是表达得不够明白, 还可以看看下图

![](/img/reactor_intro/5.jpg)


这个模型和上面的 NIO 流程很类似，只是将消息相关处理独立到了 Handler 中去了！

虽然上面说到 NIO 一个线程就可以支持所有的 IO 处理。但是瓶颈也是显而易见的！我们看一个客户端的情况，如果这个客户端多次进行请求，如果在 Handler 中的处理速度较慢，那么后续的客户端请求都会被积压，导致响应变慢！所以引入了 Reactor 多线程模型!

## Reactor 多线程模型

![](/img/reactor_intro/1100082-b21e4c2555478155.png)

如果上图表达得不够明白, 还可以看看下图

![](/img/reactor_intro/worker_thread_pools.jpg)

如果上图还是表达得不够明白, 还可以看看下图

![](/img/reactor_intro/8.jpg)

Reactor 多线程模型就是将 Handler 中的 IO 操作和非 IO 操作分开，操作 IO 的线程称为 IO 线程，非 IO 操作的线程称为工作线程! 这样的话，客户端的请求会直接被丢到线程池中，客户端发送请求就不会堵塞！

但是当用户进一步增加的时候，Reactor 会出现瓶颈！因为 Reactor 既要处理 IO 操作请求，又要响应连接请求！为了分担 Reactor 的负担，所以引入了主从 Reactor 模型!


## 主从 Reactor 模型

![](/img/reactor_intro/1100082-794d7f69b6e2409a.png)

如果上图表达得不够明白, 还可以看看下图

![](/img/reactor_intro/using_multiple_reactors_with_thread_pool.jpg)

如果上图还是表达得不够明白, 还可以看看下图

![](/img/server_model_summary/11.jpg)

主 Reactor 用于响应连接请求，从 Reactor 用于处理 IO 操作请求！

