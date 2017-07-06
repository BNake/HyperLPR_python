## HyperLPR Python

### 介绍

一个简单的中文车牌识别Python实现。

### 前言

之前有个HyperLPR的C++项目，其识别效果并不是很好，编译存在一定困难。在结合了一些近年来OCR、场景文字检测论文等论文，使用Python简单的实现了一下。

### 特性

+ 单张720p 识别时间在单核Intel 2.2G CPU(MBP2015 15inch)不低于 140ms。比EasyPR单核识别速度快近10倍左右的时间。
+ 识别率在EasyPR数据集上0-error达到67.3% 1-error识别率达到 88.6%
+ 单线程平均检测时间在EASY数据集在保持在160ms以下。基于Haar+adaboost检测方法在速度、召回率、准确率上都不逊于MSER方法。
+ 代码框架简单，总代码不到1k行。

### 缺点

+ 代码较为简单，存在BUG
+ 在大角度下（大于-+15度）下不能取得良好的定位效果，后续会有解决方案。
+ 目前仅能识别标准蓝牌

### 注意事项

本项目仅仅用于研究和测试，请勿用于商业



### 依赖

+ Keras + Theano backend (Tensorflow data order)
+ Theano
+ Numpy
+ Scipy
+ OpenCV

### 测试结果

总识别率 0.673170731707
第1位(汉字)匹配率: 0.863414634146 第2位(省份)匹配率: 0.878048780488 第3位匹配率: 0.90243902439第4位匹配率: 0.921951219512 第5位匹配率: 0.931707317073 第6位匹配率: 0.921951219512 第7位匹配率: 0.863414634146

完全匹配: 138
匹配错误1位: 41
匹配错误2位: 11
匹配错误3位: 3
匹配错误4位: 1
匹配错误5位: 1
匹配错误6位: 4
匹配完全错误: 4

错误4位以上的车牌 川MAGU8C->川AGU801 晋P186KM->晋AP186W 青FPH161->津AHP676 川A1MS68->津MSY678 湘A107G3->湘A07G31 津TDG11M->皖EZM618 甘R75Y34->粤BR75Y3 鄂D0L666->陕B8C666