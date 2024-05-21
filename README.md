<h1 align="center">openctp-ctp </h1>
<img src="openctp.jpg" align="right" height="130"/>

<div>
    <a href="#"><img src="https://flat.badgen.net/badge/os/windows-x86/cyan?icon=windows" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/windows-x86_64/cyan?icon=windows" /></a>
    <a href="#"><img src="https://img.shields.io/badge/os-linux_x86_64-white?style=flat-square&logo=linux&logoColor=white&color=rgb(35%2C189%2C204)" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/macos-x86_64/cyan?icon=apple" /></a>
    <a href="#"><img src="https://flat.badgen.net/badge/os/macos-arm64/cyan?icon=apple" /></a>
</div>
<div>
    <a href="#"><img src="https://flat.badgen.net/badge/python/3.7|3.8|3.9|3.10|3.11|3.12/blue" /></a>
    <a href="https://pepy.tech/project/openctp-ctp" ><img src="https://static.pepy.tech/badge/openctp-ctp" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/license/BSD-3/blue?" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/test/pass/green?icon=github" /></a>
    <a href="#" ><img src="https://flat.badgen.net/badge/CI/success/green?icon=github" /></a>
</div>
<br>

由 [**openctp**](https://github.com/openctp) 团队提供, 使用Swig制作的Python版CTPAPI。

简化对接CTPAPI的过程，节省精力，快速上手 :rocket:

---

* [支持版本](#支持版本)
  * [生产版](#生产版)
  * [评测版](#评测版)
* [快速使用](#快速使用)
    * [方式一 pip](#方式一-pip)
    * [方式二 手动配置](#方式二-手动配置)
* [代码示例](#代码示例)
* [编码增强](#编码增强)
* [字符集问题](#字符集问题)
* [说明](#说明)

---

## 支持版本

### 生产版

| openctp-ctp | win x86            | win x64            | linux x64          | mac x64            | mac arm64          |
|-------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 6.3.15.*    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.3.19.*    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.5.1.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.6.1.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.6.7.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.6.9.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.7.0.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.7.1.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.7.2.*     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

### 评测版

| openctp-ctp-cp | win x86            | win x64            | linux x64          | mac x64                  | mac arm64                |
|----------------|--------------------|--------------------|--------------------|--------------------------|--------------------------|
| 6.3.19.*       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                      | :x:                      |
| 6.5.1.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                      | :x:                      |
| 6.6.1.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                      | :x:                      |
| 6.6.7.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                      | :x:                      |
| 6.6.9.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_multiplication_x: | :heavy_multiplication_x: |
| 6.7.0.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_multiplication_x: | :heavy_multiplication_x: |
| 6.7.2.*        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_multiplication_x: | :heavy_multiplication_x: |

> 📌 :x:是因为CTP官方没有提供相应平台的库。:heavy_multiplication_x:是openctp还未提供支持

## 快速使用

openctp-ctp提供了两种安装使用方式: 通过pip安装、手动下载配置。
openctp-ctp-ctp 只提供了pip安装的方式

> 需要自行提前准备好 Python 环境。

### 方式一 pip

选择一个版本，如 6.7.2

```shell
pip install openctp-ctp==6.7.2.* -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
```

`zsh`安装:

```shell
pip install openctp-ctp==6.7.2.\* -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host=pypi.tuna.tsinghua.edu.cn
```

引用方法:

```python 
from openctp_ctp import tdapi, mdapi
```

更多的接口使用方法参考 [代码示例](#代码示例)

> 以上流程, 将 **openctp-ctp** 更换为 **openctp-ctp-ctp** 就是评测版的安装使用方式

### 方式二 手动配置

手动下载指定版本的动态库文件，并配置库路径。

- Windows

  因为 windows 下，不同的 python 版本编译的动态库之间不可共用，所以不同的 python 版本需要下载指定版本对应的动态库。

  swig 转换时使用 C++ 内置方式进行 GBK 和 UTF8 的编码转换。

  如: 6.6.9-x64, python 3.10  
  从目录 `6.6.9_20220820/win64` 和 `6.6.9_20220820/win64/py310` 下载库文件  
  将下载的文件放在本地同一个目录下
  ```PowerShell 
  # 下载文件
  _thosttraderapi.pyd
  _thostmduserapi.pyd
  thosttraderapi.py
  thostmduserapi.py
  thosttraderapi_se.dll
  thostmduserapi_se.dll 
  ```

- Linux  
  选择一个版本，如: 6.7.2
  从目录`6.7.2_20230913/linux64`下载所有的文件  
  将下载的文件放在同一目录下
  ```bash
  _thosttraderapi.so
  _thostmduserapi.so
  thosttraderapi.py
  thostmduserapi.py
  libthosttraderapi_se.so
  libthostmduserapi_se.so
  ```
  将文件所在路径加入到到库路径(<specify_path>填写当前路径)
  ```bash
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<specify_path>
  ```
- MacOS(在路上...)

为了测试是否配置成功，可以使用测试文件 demo_td.py/md_demo.py，和上面的文件放在同一个目录下即可。

- 测试行情接口

  注意选取有效的行情前置地址, 参考[openctp监控Simnow](http://openctp.cn)  
  注意选取有效的合约, 可通过交易接口查询合约
    ```PowerShell 
    python md_demo.py
    ```

- 测试交易接口

  需要在 [simnow官网](http://www.simnow.com.cn) 注册账号  
  注意选取有效的交易前置地址, 参考[openctp监控Simnow](http://openctp.cn)

    ```PowerShell 
    python demo_td.py tcp://180.168.146.187:10130 <userid> <password>
    ```

## 代码示例

参考 md_demo.py/demo_td.py/tdapi.py

## 编码增强

在高级编辑器或IDE中，可以方便的查看接口说明及各字段含义。如下(Pycharm)
<div align="center"><img width="850" alt="" align="center" src="https://github.com/openctp/openctp-ctp-python/assets/17944025/e59a12c1-e5b5-40dd-a3e2-1d274c63bd69" /></div>
.
<div align="center"><img width="850" alt="" align="center" src="https://github.com/openctp/openctp-ctp-python/assets/17944025/1b06e371-3974-4e39-8328-34c12a1b0ae0" /></div>
.
<div align="center"><img width="850" alt="" align="center" src="https://github.com/openctp/openctp-ctp-python/assets/17944025/84e9e87c-1a8b-42f7-82d7-7e20829d2520" /></div>

## 字符集问题

- Linux下安装后，需要安装中文字符集，否则导入时报错：

    ```text
    >>> import openctp_ctp
    terminate called after throwing an instance of 'std::runtime_error'
    what():  locale::facet::_S_create_c_locale name not valid
    Aborted
    ```
    
    或
    
    ```text
    >>> import openctp_ctp
    Aborted
    ```
    
    需要安装 `GB18030` 字符集，这里提供 ubuntu/debian/centos 的方案：
    
    ```bash
    # Ubuntu (20.04)
    sudo apt-get install -y locales
    sudo locale-gen zh_CN.GB18030
    
    # Debian (11)
    sudo apt install locales-all
    sudo localedef -c -f GB18030 -i zh_CN zh_CN.GB18030
    
    # CentOS (7)
    sudo yum install -y kde-l10n-Chinese
    sudo yum reinstall -y glibc-common
    ```

- Mac下报错
    ```text
    Fatal Python error: config_get_locale_encoding: failed to get the locale encoding: nl_langinfo(CODESET) failed
    Python runtime state: preinitialized
    ```
    设置 `export LANG="en_US.UTF-8"` 并使之生效

## 说明

- 通过openctp-ctp库只能连接支持CTPAPI**官方实现**的柜台，如:simnow;不支持连接兼容CTPAPI接口但**非官方实现**的柜台，如:
  openctp(由TTS支持)
- 限于时间/精力有限，只是在 SimNow 模拟平台进行了测试，若要通过openctp-ctp使用CTPAPI所有的接口或用于生产环境，请自行进行充分测试。
- 由于许多用户只要使用Python版CTPAPI即可，并不需要自己进行繁琐的编译工作(适配各种编译环境)
  ，且大量跨平台夸版本的编译分发相对麻烦，仅提供了编译好的pip包和pyd/so动态库。需要自行编译的用户可参考 [swig转换CTPAPI为Python攻略](https://www.jedore.top/blog/post/ctpapi-swig-python/),
  也可参考[景色的Python-CTPAPI](https://github.com/nicai0609/Python-CTPAPI)
- [更新日志](CHANGELOG.md)

**使用 openctp-ctp 进行实盘交易的后果完全由使用者自己承担！！！**
