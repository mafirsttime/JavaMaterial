

[toc]



# go入门



## 开发环境

安装：

go1.17.6.darwin-amd64。pkg

path： cd /usr/local/go

```
$go version
go version go1.17.6 darwin/amd64
```





### GOPROXY

Go1.14版本之后，都推荐使用go mod模式来管理依赖环境了，也不再强制我们把代码必须写在GOPATH下面的src目录了，你可以在你电脑的任意位置编写go代码。（网上有些教程适用于1.11版本之前。）

默认GoPROXY配置是：GOPROXY=https://proxy.golang.org,direct，由于国内访问不到https://proxy.golang.org，所以我们需要换一个PROXY，这里推荐使用https://goproxy.io或https://goproxy.cn。

可以执行下面的命令修改GOPROXY：

```
go env -w GOPROXY=https://goproxy.cn,direct
```



```
# go环境变量配置
# sudo vim /etc/profile
export GOROOT=/usr/local/go
export GOPATH=/home/bruce/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOROOT/bin
export PATH=$PATH:$GOPATH/bin
# 环境变量生效
source /etc/profile
```