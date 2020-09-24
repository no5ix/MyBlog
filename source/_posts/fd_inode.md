---
title: 文件描述符FD与Inode
date: 2018-08-06 08:08:06
tags:
- Linux
categories:
- Linux
---


# FD 文件描述符

　　Linux 系统中，把一切都看做是文件，当进程打开现有文件或创建新文件时，内核向进程返回一个文件描述符，文件描述符就是内核为了高效管理已被打开的文件所创建的索引，用来指向被打开的文件，所有执行 I/O 操作的系统调用都会通过文件描述符。


## 文件描述符、文件、进程间的关系

### 描述：

我们可以通过 linux 的几个基本的 I/O 操作函数来理解什么是文件操作符。

```
fd = open(pathname, flags, mode)
// 返回了该文件的fd
rlen = read(fd, buf, count)
// IO操作均需要传入该文件的fd值
wlen = write(fd, buf, count)
status = close(fd)


```

每当进程用`open（）`函数打开一个文件，内核便会返回该文件的文件操作符（一个非负的整形值），此后所有对该文件的操作，都会以返回的 fd 文件操作符为参数。

![](/img/fd_inode/fd_inode1.jpg)

**文件描述符**可以理解为进程文件描述表这个表的**索引**，或者把文件描述表看做一个数组的话，文件描述符可以看做是数组的下标。当需要进行 I/O 操作的时候，会传入 fd 作为参数，先从进程文件描述符表查找该 fd 对应的那个条目，取出对应的那个已经打开的文件的**句柄**，根据文件句柄指向，去系统 fd 表中查找到该文件指向的 **inode**，从而定位到该文件的真正位置，从而进行 I/O 操作。

我们仔细看这张图, 在进程A中，文件描述符1和30都指向了同一个打开的文件句柄（标号23）。这可能是通过调用dup()、dup2()、fcntl()或者对同一个文件多次调用了open()函数而形成的。

进程A的文件描述符2和进程B的文件描述符2都指向了同一个打开的文件句柄（标号73）。这种情形可能是在调用fork()后出现的（即，进程A、B是父子进程关系），或者当某进程通过UNIX域套接字将一个打开的文件描述符传递给另一个进程时，也会发生。再者是不同的进程独自去调用open函数打开了同一个文件，此时进程内部的描述符正好分配到与其他进程打开该文件的描述符一样。
此外，进程A的描述符0和进程B的描述符3分别指向不同的打开文件句柄，但这些句柄均指向i-node表的相同条目（1976），换言之，指向同一个文件。发生这种情况是因为每个进程各自对同一个文件发起了open()调用。同一个进程两次打开同一个文件，也会发生类似情况。

**小结:**  

* 由于进程级文件描述符表的存在，不同的进程中会出现相同的文件描述符，它们可能指向同一个文件，也可能指向不同的文件
* 两个不同的文件描述符，若指向同一个打开文件句柄，将共享同一文件偏移量。因此，如果通过其中一个文件描述符来修改文件偏移量（由调用read()、write()或lseek()所致），那么从另一个描述符中也会观察到变化，无论这两个文件描述符是否属于不同进程，还是同一个进程，情况都是如此。
* 要获取和修改打开的文件标志（例如：O_APPEND、O_NONBLOCK和O_ASYNC），可执行fcntl()的F_GETFL和F_SETFL操作，其对作用域的约束与上一条颇为类似。
* 文件描述符标志（即，close-on-exec）为进程和文件描述符所私有。对这一标志的修改将不会影响同一进程或不同进程中的其他文件描述符
*   每个文件描述符会与一个打开的文件相对应
*   不同的文件描述符也可能指向同一个文件
*   相同的文件可以被不同的进程打开，也可以在同一个进程被多次打开


### 系统为维护文件描述符，建立了三个表

*   进程级的文件描述符表
*   系统级的文件描述符表
*   文件系统的 i-node 表 (inode 见下文)

### 进程级别的文件描述表：

linux 内核会为每一个进程创建一个`task_truct`结构体来维护进程信息，称之为 进程描述符，`task_truct`结构体中的指针指向一个名称为`file_struct`的结构体，该结构体即 进程级别的文件描述表。

``` cpp
struct files_struct *files
```

它的每一个条目记录的是单个文件描述符的相关信息

1.  fd 控制标志，前内核仅定义了一个，即 close-on-exec
2.  文件描述符所打开的文件句柄的引用【注 2】

> \[注释 2\]：文件句柄这里可以理解为文件名，或者文件的全路径名，因为 linux 文件系统文件名和文件是独立的，以此与 inode 区分

### 系统级别的文件描述符表

内核对系统中所有打开的文件维护了一个描述符表，也被称之为 【**打开文件表**】，表格中的每一项被称之为 【**打开文件句柄**】，一个【**打开文件句柄**】 描述了一个打开文件的全部信息。  
主要包括：

1.  当前文件偏移量（调用 read() 和 write() 时更新，或使用 lseek() 直接修改）
2.  打开文件时所使用的状态标识（即，open() 的 flags 参数）
3.  文件访问模式（如调用 open() 时所设置的只读模式、只写模式或读写模式）
4.  与信号驱动相关的设置
5.  对该文件 i-node 对象的引用
6.  文件类型（例如：常规文件、套接字或 FIFO）和访问权限
7.  一个指针，指向该文件所持有的锁列表
8.  文件的各种属性，包括文件大小以及与不同类型操作相关的时间戳


### Inode表

每个文件系统会为存储于其上的所有文件 (包括目录) 维护一个 i-node 表，单个 i-node 包含以下信息：

1.  文件类型 (file type)，可以是常规文件、目录、套接字或 FIFO
2.  访问权限
3.  文件锁列表 (file locks)
4.  文件大小  
5.  ...

i-node 存储在磁盘设备上，内核在内存中维护了一个副本，这里的 i-node 表为后者。副本除了原有信息，还包括：引用计数 (从打开文件描述体)、所在设备号以及一些临时属性，例如文件锁。

> 注：进程 A 的 fd 表中，左边 fd0，fd1，fd2… 就是各个文件描述符，它是 fd 表的索引，fd 不是表里那个 fd flags！这里不要搞混淆了，fd flags 目前只有一个取值。

在进程 A 中，文件描述符 1 和 30 都指向了同一个打开的文件句柄（标号 23）。这可能是通过调用 dup()、dup2()、fcntl() 或者对同一个文件多次调用了 open() 函数而形成的。  
**dup（）**，也称之为**文件描述符复制函数**，在某些场景下非常有用，比如：标准输入 / 输出重定向。在 shell 下，完成这个操作非常简单，大部分人都会，但是极少人思考过背后的原理。

大概描述一下需要的几个步骤，以标准输出 (文件描述符为 1) 重定向为例：

1.  打开目标文件，返回文件描述符 n；
2.  关闭文件描述符 1；
3.  调用 dup 将文件描述符 n 复制到 1；
4.  关闭文件描述符 n；

进程 A 的文件描述符 2 和进程 B 的文件描述符 2 都指向了同一个打开的文件句柄（标号 73）。这种情形可能是在调用 fork() 后出现的（即，进程 A、B 是父子进程关系）【注 3】，或者当某进程通过 UNIX 域套接字将一个打开的文件描述符传递给另一个进程时，也会发生。再者是不同的进程独自去调用 open 函数打开了同一个文件，此时进程内部的描述符正好分配到与其他进程打开该文件的描述符一样。

> 注 3： 子进程会继承父进程的文件描述符表，也就是子进程继承父进程打开的文件 这句话的由来。

此外，进程 A 的描述符 0 和进程 B 的描述符 3 分别指向不同的打开文件句柄，但这些句柄均指向 i-node 表的相同条目（1976），换言之，指向同一个文件。发生这种情况是因为每个进程各自对同一个文件发起了 open() 调用。同一个进程两次打开同一个文件，也会发生类似情况。


### 文件描述符限制

　　有资源的地方就有战争，“文件描述符”也是一种资源，系统中的每个进程都需要有 “文件描述符” 才能进行改变世界的宏图霸业。世界需要秩序，于是就有了 “文件描述符限制” 的规定。

如下表：  
![](/img/fd_inode/fd_inode2.jpg)

永久修改用户级限制时有三种设置类型：

*   soft 指的是当前系统生效的设置值
*   hard 指的是系统中所能设定的最大值
*   “-” 指的是同时设置了 soft 和 hard 的值


# Inode文件节点

inode 是什么？

理解 inode，要从文件储存说起。

文件储存在硬盘上，硬盘的最小存储单位叫做” 扇区”（Sector）。每个扇区储存 512 字节（相当于 0.5KB）。

操作系统读取硬盘的时候，不会一个个扇区地读取，这样效率太低，而是一次性连续读取多个扇区，即一次性读取一个” 块”（block）。这种由多个扇区组成的” 块”，是文件存取的最小单位。” 块” 的大小，最常见的是 4KB，即连续八个 sector 组成一个 block。

文件数据都储存在” 块” 中，那么很显然，我们还必须找到一个地方储存文件的元信息，比如文件的创建者、文件的创建日期、文件的大小等等。这种储存文件元信息的区域就叫做 inode，中文译名为” 索引节点”。

每一个文件都有对应的 inode，里面包含了与该文件有关的一些信息。



## inode 的内容

inode 包含文件的元信息，具体来说有以下内容：

*   文件的字节数
*   文件拥有者的 User ID
*   文件的 Group ID
*   文件的读、写、执行权限
*   文件的时间戳，共有三个：ctime 指 inode 上一次变动的时间，mtime 指文件内容上一次变动的时间，atime 指文件上一次打开的时间。
*   链接数，即有多少文件名指向这个 inode
*   文件数据 block 的位置

可以用`stat`命令，查看某个文件的 inode 信息：  
`stat 233.txt`  

![](/img/fd_inode/fd_inode3.jpg)

总之，除了文件名以外的所有文件信息，都存在 inode 之中。至于为什么没有文件名，下文会有详细解释。


## inode 的大小

inode 也会消耗硬盘空间，所以硬盘格式化的时候，操作系统自动将硬盘分成两个区域。一个是数据区，存放文件数据；另一个是 inode 区（inode table），存放 inode 所包含的信息。

每个 inode 节点的大小，一般是 128 字节或 256 字节。inode 节点的总数，在格式化时就给定，一般是每 1KB 或每 2KB 就设置一个 inode。假定在一块 1GB 的硬盘中，每个 inode 节点的大小为 128 字节，每 1KB 就设置一个 inode，那么 inode table 的大小就会达到 128MB，占整块硬盘的 12.8%。

查看每个硬盘分区的 inode 总数和已经使用的数量，可以使用 df 命令。

`df -i`  

![](/img/fd_inode/fd_inode4.jpg)

查看每个 inode 节点的大小，可以用如下命令：

`sudo dumpe2fs -h /dev/hda | grep "Inode size"`

由于每个文件都必须有一个 inode，因此有可能发生 inode 已经用光，但是硬盘还未存满的情况。这时，就无法在硬盘上创建新文件。


## inode 号码


每个 inode 都有一个号码，操作系统用 inode 号码来识别不同的文件。

这里值得重复一遍，**Unix/Linux 系统内部不使用文件名，而使用 inode 号码来识别文件**。对于系统来说，文件名只是 inode 号码便于识别的别称或者绰号。

表面上，用户通过文件名，打开文件。实际上，系统内部这个过程分成三步：首先，系统找到这个文件名对应的 inode 号码；其次，通过 inode 号码，获取 inode 信息；最后，根据 inode 信息，找到文件数据所在的 block，读出数据。

使用 ls -i 命令，可以看到文件名对应的 inode 号码：

`ls -i 233.txt`

![](/img/fd_inode/fd_inode5.jpg)


## 目录文件

Unix/Linux 系统中，目录（directory）也是一种文件。打开目录，实际上就是打开目录文件。

目录文件的结构非常简单，就是一系列目录项（dirent）的列表。每个目录项，由两部分组成：  
* 所包含文件的文件名，
* 该文件名对应的 inode 号码。

ls 命令只列出目录文件中的所有文件名：

`ls /etc`

ls -i 命令列出整个目录文件，即文件名和 inode 号码：

`ls -i /etc`

如果要查看文件的详细信息，就必须根据 inode 号码，访问 inode 节点，读取信息。ls -l 命令列出文件的详细信息。

`ls -l /etc`

理解了上面这些知识，就能理解目录的权限。目录文件的读权限（r）和写权限（w），都是针对目录文件本身。由于目录文件内只有文件名和 inode 号码，所以如果只有读权限，只能获取文件名，无法获取其他信息，因为其他信息都储存在 inode 节点中，而读取 inode 节点内的信息需要目录文件的执行权限（x）。

## 链接

![](/img/noodle_plan/linux/hard_link_soft_link.jpg)

### 硬链接


一般情况下，文件名和 inode 号码是” 一一对应” 关系，每个 inode 号码对应一个文件名。但是，**Unix/Linux 系统允许，多个文件名指向同一个 inode 号码。**

这意味着，可以用不同的文件名访问同样的内容；对文件内容进行修改，会影响到所有文件名；但是，删除一个文件名，不影响另一个文件名的访问。这种情况就被称为” 硬链接”（hard link）。

ln 命令可以创建硬链接：

`ln 源文件 目标文件`

运行上面这条命令以后，源文件与目标文件的 inode 号码相同，都指向同一个 inode。

**inode 信息中有一项叫做`i_nlink`”链接数”，记录指向该 inode 的文件名总数，这时就会增加 1。**

**反过来，删除一个文件名，就会使得 inode 节点中的`i_nlink`”链接数” 减 1。当这个值减到 0，表明没有文件名指向这个 inode，系统就会回收这个 inode 号码，以及其所对应 block 区域。**

这里顺便说一下目录文件的`i_nlink`”链接数”。创建目录时，默认会生成两个目录项：”.” 和”..”。前者的 inode 号码就是当前目录的 inode 号码，等同于当前目录的” 硬链接”；后者的 inode 号码就是当前目录的父目录的 inode 号码，等同于父目录的” 硬链接”。所以，任何一个目录的” 硬链接” 总数，总是等于 2 加上它的子目录总数（含隐藏目录）。


简单说，硬链接就是一个 inode 号对应多个文件名。就是同一个文件使用了多个别名（上图中 hard link 就是 file 的一个别名，他们有共同的 inode）。

由于硬链接是有着相同 inode 号仅文件名不同的文件，因此硬链接存在以下几点特性：

* 文件有相同的 inode 及 data block；
* 只能对已存在的文件进行创建；
* 不能交叉文件系统进行硬链接的创建；
* 不能对目录进行创建，只可对文件创建；
* 删除一个硬链接文件并不影响其他有相同 inode 号的文件, 只是相应的链接计数器（link count)减1


### 软链接

(又称符号链接，即 soft link 或 symbolic link） 软链接与硬链接不同，若文件用户数据块中存放的内容是另一文件的路径名的指向，则该文件就是软连接。软链接就是一个普通文件，只是数据块内容有点特殊。软链接有着自己的 inode 号以及用户数据块。（见图2）软连接可以指向目录，而且软连接所指向的目录可以位于不同的文件系统中。

**ln -s 命令可以创建软链接**。

`ln -s 源文文件或目录 目标文件或目录`

软链接特性：

* 软链接有自己的文件属性及权限等；
* 可对不存在的文件或目录创建软链接；
* 软链接可交叉文件系统；
* 软链接可对文件或目录创建；
* 创建软链接时，链接计数 i_nlink 不会增加；
* 删除软链接并不影响被指向的文件，但若被指向的原文件被删除，则相关软连接被称为死链接或悬挂的软链接（即 dangling link，若被指向路径文件被重新创建，死链接可恢复为正常的软链接）。


文件 A 和文件 B 的 inode 号码虽然不一样，但是文件 A 的内容是文件 B 的路径。读取文件 A 时，系统会自动将访问者导向文件 B。因此，无论打开哪一个文件，最终读取的都是文件 B。这时，文件 A 就称为文件 B 的” 软链接”（soft link）或者” 符号链接（symbolic link）。

这意味着，文件 A 依赖于文件 B 而存在，如果删除了文件 B，打开文件 A 就会报错：”No such file or directory”。这是软链接与硬链接最大的不同：文件 A 指向文件 B 的文件名，而不是文件 B 的 inode 号码，文件 B 的 inode” 链接数” 不会因此发生变化。


## inode 的特殊作用

由于 inode 号码与文件名分离，这种机制导致了一些 Unix/Linux 系统特有的现象。

*   有时，文件名包含特殊字符，无法正常删除。这时，直接删除 inode 节点，就能起到删除文件的作用。
*   移动文件或重命名文件，只是改变文件名，不影响 inode 号码。
*   打开一个文件以后，系统就以 inode 号码来识别这个文件，不再考虑文件名。因此，通常来说，系统无法从 inode 号码得知文件名。

第 3 点使得软件更新变得简单，可以在不关闭软件的情况下进行更新，不需要重启。因为系统通过 inode 号码，识别运行中的文件，不通过文件名。更新的时候，新版文件以同样的文件名，生成一个新的 inode，不会影响到运行中的文件。等到下一次运行这个软件的时候，文件名就自动指向新版文件，旧版文件的 inode 则被回收。