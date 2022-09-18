# convertYNcatalog2hypoDD
convert YN phase to PALM hypodd file input

1、修改了，转换目录的北京时间到UTC time。
2、在震相行中取出第一个找到Pg或Pn，继续向下找如果Sg存在就提取，找不到就不提取。
3、删除了目录行最后的序号。
