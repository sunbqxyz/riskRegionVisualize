# 中国风险地区（县级）可视化

基于[风险地区历史数据集](https://github.com/sunbqxyz/china_covid_riskareas_history)和[RiskLevelApi](https://github.com/panghaibin/RiskLevelAPI)提供的数据，利用中国县级区划SHP文件和cartopy绘制生成针对给定数据集的风险地区分布图。

## 地理逆编码

readRiskApi.py 读取风险区数据集，并通过名称匹配的方式，将风险区地址转化为地理编码，对于部分不标准的风险区地址（常见于各类“开发区”），利用高德地图逆编码API进行解决，并将结果保存至本地，以减少重复调用，最终，会输出latest_code.json。

**使用前，需将GDKey替换为个人申请的高德api key**

## Shapefile读取与绘制

cnmap.py 读取latest_code.json，并将其中code对应的县绘制为橙色、对应的市输出为灰色，详见例图。

注意：项目中使用的中国地图因为美观原因经过特殊修改，如需发布，请按照相关条例送自然资源主管部门审核，并自行承担全部法律责任。

![例图](https://github.com/sunbqxyz/riskRegionVisualize/blob/main/example.png)



