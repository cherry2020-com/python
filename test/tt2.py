# -*- coding:utf-8 -*-
import json
import re
import time

html = u"""
<script lanuage="javascript">
var __seniorquery = "";//高级检索通用开关参数
</script>

<form id="pagerForm" action="/admin/closeCode/selectList.do" method="post" onsubmit="return dialogSearch(this);"><input type="hidden" name="targetType" value="" />
	<input type="hidden" name="multiSelect" value="true" />
	<input type="hidden" name="rel" value="" />
	<div class="pageContent"  layoutH="5">
		<ul class="tree" style="overflow:auto;"><li rel="ab646c425104a69b080c9b21465b8728" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>需求变更类</em></a><ul><li rel="a3a2c3c9187d8972998192556fb782ff" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'a3a2c3c9187d8972998192556fb782ff',name:'新需求'})"><em>新需求</em></a><ul></ul></li><li rel="98a0d6ea9bf88f23c46323a5e0a828ac" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'98a0d6ea9bf88f23c46323a5e0a828ac',name:'优化'})"><em>优化</em></a><ul></ul></li><li rel="7cb4e6a7ff4c5152b4ecd9b2d8436ca0" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'7cb4e6a7ff4c5152b4ecd9b2d8436ca0',name:'SAP传输请求'})"><em>SAP传输请求</em></a><ul></ul></li></ul></li><li rel="26b7f7cca52bea3f6f01d9942dc7b7b2" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>权限类</em></a><ul><li rel="02b32ff3d5a45a70c0a60af2b58dc301" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'02b32ff3d5a45a70c0a60af2b58dc301',name:'账号解锁/重置'})"><em>账号解锁/重置</em></a><ul></ul></li><li rel="458c9443f4ad0de1292647374b7d2e65" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'458c9443f4ad0de1292647374b7d2e65',name:'账号增删改'})"><em>账号增删改</em></a><ul></ul></li><li rel="f29420e94e77edde350a9ab34e76d9d1" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'f29420e94e77edde350a9ab34e76d9d1',name:'权限设计问题'})"><em>权限设计问题</em></a><ul></ul></li><li rel="a385d215c64d934023d1da9970a5dfd8" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'a385d215c64d934023d1da9970a5dfd8',name:'权限增删改'})"><em>权限增删改</em></a><ul></ul></li></ul></li><li rel="7035df7c0925208e392fb326ac8cc8ca" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>咨询类</em></a><ul><li rel="524228b1c0639efff4c3cb6cae326312" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'524228b1c0639efff4c3cb6cae326312',name:'ID/权限/权限信息等'})"><em>ID/权限/权限信息等</em></a><ul></ul></li><li rel="7645b2fe34dd6ac29380b0a1995608b9" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'7645b2fe34dd6ac29380b0a1995608b9',name:'系统功能'})"><em>系统功能</em></a><ul></ul></li><li rel="7ee98e300a851bfcf3639d86e17304fe" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'7ee98e300a851bfcf3639d86e17304fe',name:'业务流程'})"><em>业务流程</em></a><ul></ul></li></ul></li><li rel="31c78889b54c964ac0da8c3f718bc489" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>用户类</em></a><ul><li rel="fe053666831d80888be41f41f6780b74" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'fe053666831d80888be41f41f6780b74',name:'业务流程定义问题'})"><em>业务流程定义问题</em></a><ul></ul></li><li rel="b7026db56f48039d632569f384bbaba2" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'b7026db56f48039d632569f384bbaba2',name:'用户操作问题'})"><em>用户操作问题</em></a><ul></ul></li></ul></li><li rel="adc56c1ab265c5d7917617236cd205bc" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>系统类</em></a><ul><li rel="20b6e5a6a5ad7db5a9677887c6724d93" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'20b6e5a6a5ad7db5a9677887c6724d93',name:'Bug问题'})"><em>Bug问题</em></a><ul></ul></li><li rel="64392d6d9590cb47b119dc55ba98aa60" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'64392d6d9590cb47b119dc55ba98aa60',name:'配置问题'})"><em>配置问题</em></a><ul></ul></li><li rel="05765726bcc3a7708741990f28b6b400" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'05765726bcc3a7708741990f28b6b400',name:'发版问题'})"><em>发版问题</em></a><ul></ul></li><li rel="f9a59754ecd085eb8fc9d621527ad84c" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'f9a59754ecd085eb8fc9d621527ad84c',name:'操作系统问题'})"><em>操作系统问题</em></a><ul></ul></li><li rel="76cab04cfeada9b9d40a62c851d3ff35" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'76cab04cfeada9b9d40a62c851d3ff35',name:'产品问题'})"><em>产品问题</em></a><ul></ul></li><li rel="461fab88dcd20925354a233ea574cf46" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'461fab88dcd20925354a233ea574cf46',name:'接口中间件问题'})"><em>接口中间件问题</em></a><ul></ul></li><li rel="2536f738add7afbee2cbf54a6a90b7e3" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'2536f738add7afbee2cbf54a6a90b7e3',name:'性能问题'})"><em>性能问题</em></a><ul></ul></li></ul></li><li rel="4955b80eb5a7b59e45628b5be5de2421" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>基础架构类</em></a><ul><li rel="20042e6812613869c575afa64fd2e445" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'20042e6812613869c575afa64fd2e445',name:'数据库问题'})"><em>数据库问题</em></a><ul></ul></li><li rel="c6d16969e999b2ba12d5c195e32a188f" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'c6d16969e999b2ba12d5c195e32a188f',name:'硬件问题'})"><em>硬件问题</em></a><ul></ul></li><li rel="246df19344689fe9ee11665c9f89747b" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'246df19344689fe9ee11665c9f89747b',name:'网络问题'})"><em>网络问题</em></a><ul></ul></li><li rel="7eca392b6c86cbec57468ea39f86df0c" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'7eca392b6c86cbec57468ea39f86df0c',name:'信息安全问题'})"><em>信息安全问题</em></a><ul></ul></li></ul></li><li rel="587adaa8ca5e0e58e1bd702faeba66fd" target="closeCodeManageKey" ><a href="javascript:void(0);"><em>数据类</em></a><ul><li rel="0701a5fda7bfe39262f97b33d2591744" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'0701a5fda7bfe39262f97b33d2591744',name:'自身维护错误'})"><em>自身维护错误</em></a><ul></ul></li><li rel="189413e96322ce6079b8f8b7e56fdd88" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'189413e96322ce6079b8f8b7e56fdd88',name:'系统问题'})"><em>系统问题</em></a><ul></ul></li><li rel="4081f42445aa011ab63be436c6246ac3" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'4081f42445aa011ab63be436c6246ac3',name:'期初数据问题'})"><em>期初数据问题</em></a><ul></ul></li><li rel="5042600128a69095a6f7ad8af6a0073e" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'5042600128a69095a6f7ad8af6a0073e',name:'数据同步/数据变更'})"><em>数据同步/数据变更</em></a><ul></ul></li><li rel="255c463df4c27c71d347f1c93ae60f84" target="closeCodeManageKey" ><a href="javascript:void(0);" onclick="$.bringBack({closeCodeManageKey:'255c463df4c27c71d347f1c93ae60f84',name:'数据导入导出'})"><em>数据导入导出</em></a><ul></ul></li></ul></li></ul></div>
</form>"""
result = {}

for j in re.findall(r'\{.*?\}', html):
 #   "u'{ticketTypeManageKey:\'4b1659330388f78f3fd10d9b19ddf4d3\',name:\'业务范围咨询\'}'"
    j = j.replace('closeCodeManageKey:', '"closeCodeManageKey":')
    j = j.replace('name:', '"name":')
    j = j.replace("'", '"')
    _json = json.loads(j)
    result[_json['name']] = _json['closeCodeManageKey']

print json.dumps(result)
print result[u'其它']

# from utils.fiddler_session import RawToPython
# r = RawToPython('./tmp.txt')
# for k, v in result.items():
#     r.set_param(url_param={'ticketTypeKey': v})
#     print k, r.requests().text
#     time.sleep(0.5)