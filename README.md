<h1 align="center">openctp-ctp</h1>

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
:rocket:以 Python 的方式，简化对接 CTPAPI 的过程，节省精力，快速上手。

**openctp-ctp**是由[openctp](https://github.com/openctp)团队提供的官方ctpapi(c++)的python版本，
使用**swig**转换ctpapi(c++)生成。

* [支持版本](#支持版本)
* [使用方式](#使用方式)
    * [通过pip安装](#通过pip安装)
    * [手动下载配置](#手动下载配置)
* [代码示例](#代码示例)
* [字符集问题](#字符集问题)
* [说明](#说明)

## 支持版本

| CTPAPI(C++) | openctp-ctp(python) | win x86            | win x64            | linux x64          | mac x64            | mac arm64          |
|-------------|---------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| 6.3.15      | 6.3.15.*            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.3.19_P1   | 6.3.19.*            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.5.1       | 6.5.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.6.1_P1    | 6.6.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.6.7       | 6.6.7.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.6.9       | 6.6.9.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.7.0       | 6.7.0.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 6.7.1       | 6.7.1.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                |
| 6.7.2       | 6.7.2.*             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

## 使用方式

需要自行提前准备好 Python 环境

### 通过pip安装

选择一个版本安装，如 6.7.2

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

### 手动下载配置

手动下载指定版本的动态库文件，并配置库路径。

- Windows

  因为 windows 下，不同的 python 版本编译的动态库之间不可共用，所以不同的 python 版本需要下载指定版本对应的动态库。

    - C++内置转码方式

      swig 转换时使用 C++ 内置方式进行 GBK 和 UTF8 的编码转换  
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
      thostmduserapi.dll 
      ```

    - `libiconv`转码方式

      swig 转换时使用 `libiconv` 进行 GBK 和 UTF8 的编码转换  
      如：6.7.0-64, python 3.10  
      从目录 `6.7.0_20230209/win64` 和 `6.7.0_20230209/win64/py310` 下载库文件  
      将下载的文件放在本地同一个目录下
      ```PowerShell 
      # 下载文件
      charset.dll
      iconv.dll
      msvcp140.dll
      _thosttraderapi.pyd
      _thostmduserapi.pyd
      thosttraderapi.py
      thostmduserapi.py
      thosttraderapi_se.dll
      thostmduserapi.dll 
      ```
      如果本地已经安装了`charset.dll/iconv.dll/msvcp140.dll`并且路径配置正确，就不用下载这三个库了。

- Linux  
  选择一个ctpapi版本，如: 6.7.2
  从目录`6.7.2_20230913/linux64`下载所有的文件  
  将下载的文件放在同一目录下
  ```bash
  _thosttraderapi.so
  _thostmduserapi.so
  thosttraderapi.py
  thostmduserapi.py
  libthosttraderapi_se.so
  libthostmduserapi.so
  ```
  将文件所在路径配置库路径(specify_path填写自己的路径)
  ```bash
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<specify_path>
  ```
- MacOS

为了测试是否配置成功，可以下载测试文件 [demo/demo_td.py](demo/demo_td.py)/[demo/demo_md.py](demo/demo_md.py)
，和上面的文件放在同一个目录下即可。

- 测试行情接口

  注意选取有效的行情前置地址, 参考[openctp监控Simnow](http://121.37.80.177:50080/detail.html)  
  注意选取有效的合约, 可通过交易接口查询合约
    ```PowerShell 
    > python demo_md.py tcp://180.168.146.187:10131 AP410 AP401
    ```

- 测试交易接口

  需要在 [simnow官网](http://www.simnow.com.cn) 注册账号  
  注意选取有效的交易前置地址, 参考[openctp监控Simnow](http://121.37.80.177:50080/detail.html)

    ```PowerShell 
    > python demo_md.py tcp://180.168.146.187:10130 <userid> <password>
    ```

`demo_td.py/demo_md.py`
只提供了最简单的测试，更多的测试示例，参考[demo/mdapi.py](demo/mdapi.py)/[demo/tdapi.py](demo/tdapi.py)

## 代码示例

*通过pip安装的可以直接使用代码示例；手动安装配置的，需要修改一下引入方式, 是`import thosttraderapi`
而不是`import openctp_ctp`*

本项目提供了一些 openctp-ctp 的基本使用方式及部分接口示例，具体如下:

- 行情 [demo](demo/mdapi.py)
    - 登录
    - 订阅行情
- 交易 [demo](demo/tdapi.py)
    - 登录
    - 投资者结算结果确认
    - 请求查询合约
    - 请求查询合约手续费率
    - 请求查询合约保证金率
    - 请求查询行情
    - 报单录入请求
    - 报单撤销请求

**代码示例仅仅作为参考，只是完成 openctp-ctp 库及 ctpapi 接口本身的功能，未考虑项目及工程性场景逻辑，
若要将 openctp-ctp 引入项目，勿照搬示例代码。**

## 字符集问题

Linux下安装后，需要安装中文字符集，否则导入时报错：

```text
>>> import openctp_ctp
terminate called after throwing an instance of 'std::runtime_error'
what():  locale::facet::_S_create_c_locale name not valid
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

## 说明

- 通过openctp-ctp库只能连接支持ctpapi(c++)**官方实现**的柜台，如:simnow;不支持连接兼容ctpapi接口但**非官方实现**的柜台，如:openctp(由tts支持)
- openctp-ctp 只支持 ctpapi 生产版本，不支持评测版本
- 限于时间/精力有限，只是在 SimNow 模拟平台进行了简单的测试，若要通过 openctp-ctp
  使用CTPAPI所有的接口或用于生产环境，请自行进行充分测试
- 后续会完善更多的测试, 以及用于生产的验证
- [更新日志](CHANGELOG.md)

**使用 openctp-ctp 进行实盘交易的后果完全由使用者自己承担！！！**
