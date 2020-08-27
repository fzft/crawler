html = """  
<!DOCTYPE HTML>



<META http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" href="../css/print.css" type="text/css">
<link rel="stylesheet" href="../css/wssb.css" type="text/css">
<meta http-equiv="Content-Language" content="GBK">
<meta http-equiv="content-type" content="text/html; charset=GBK">  


<html>

<head>
<title>企业所得税月（季）度预缴纳税申报表（A类）——打印</title>
</head>
<body marginwidth="0" marginheight="0"  topmargin="0" >
<OBJECT  id="factory" style="DISPLAY:  none"  codeBase="../ScriptX.cab#Version=5,60,0,360"  classid="clsid:1663ed61-23eb-11d2-b92f-008048fdd814"  viewastext></OBJECT>
<object id="button" style="DISPLAY:  none" classid="CLSID:8856F961-340A-11D0-A96B-00C04FD705A2"></object>
<script language="JavaScript">
function doprint() {
  factory.printing.header = ""
  factory.printing.footer = ""
  factory.printing.leftMargin  =  0
  factory.printing.topMargin  =  0
  factory.printing.rightMargin  =  0
  factory.printing.bottomMargin  =  0
  factory.printing.portrait = true
  document.all("printbtn").style.visibility = 'hidden';//打印时隐藏打印按钮 
  factory.printing.Print(false);
  document.all("printbtn").style.visibility = 'visible';//打印完显示打印按钮 
 }
 function printsetup(){ 
　　// 打印页面设置 
　　factory.printing.PageSetup(); 
　　} 
 function printpreview(){ 
　　// 打印页面预览
    factory.printing.header = ""
    factory.printing.footer = ""
    factory.printing.leftMargin  =  0
    factory.printing.topMargin  =  0
    factory.printing.rightMargin  =  0
    factory.printing.bottomMargin  =  0
    factory.printing.portrait = true
    document.all("printbtn").style.visibility = 'hidden';//打印时隐藏打印按钮 
　　factory.printing.Preview();
    document.all("printbtn").style.visibility = 'visible';//打印完显示打印按钮 
　　}
function saveas(){ 
　　// 打印页面另存为
    document.all("printbtn").style.visibility = 'hidden';//打印时隐藏打印按钮 
    document.all("printbtn").style.display = 'none';//打印时隐藏打印按钮 
　　document.all.button.ExecWB(4,1);
    //document.all("printbtn").style.visibility = 'visible';//打印完显示打印按钮 
　　}
function hide(){ 
　　// 打印页面另存为
    document.all("printbtn").style.visibility = 'hidden';//打印时隐藏打印按钮 
    document.all("printbtn").style.display = 'none';//打印时隐藏打印按钮 
　　//document.all("printbtn").style.visibility = 'visible';//打印完显示打印按钮 
　　}
 var SF=1,SF1=0.1,Max=3;
</script>
<div id="printbtn" align="center" style="DISPLAY:">
<INPUT  type="button" name="Button" value="放大" onClick="if(SF<Max){SF+=SF1;MyDiv.style.zoom=SF;}"  align="middle">
<INPUT onClick="if(SF>SF1){SF-=SF1;MyDiv.style.zoom=SF;}" type="button" name="Button" value="缩小" align="middle"> 
<INPUT onclick=javascript:doprint() type="button" name="Button" value="打印" align="middle">
<INPUT onclick=javascript:printsetup(); type="button" name="Button" value="打印设置" align="middle"> 
<INPUT onclick=javascript:printpreview(); type="button" name="Button" value="打印预览" align="middle">
<!--<input type="button" name="Button" value="另存为" onClick="javascript:saveas()">   --> 
<input type="button" name="Button" value="隐藏" onClick="javascript:hide()"> 
</div>
<Div id="MyDiv"> 


<table border="0" width="730" align="center" class="unnamed1" cellspacing="1"> 
<tr>
 <td width="100%" valign="center">
 <table width="97%" cellpadding="0" cellspacing="0" align="center">
   <tr>
     <td width="100%" colspan="1" class="pop" align="center"><b>中华人民共和国</b></td>
   </tr>
   <tr>
     <td width="100%" colspan="1" class="pop" align="center"><b>企业所得税月(季)度预缴纳税申报表(A类)</b></td>
   </tr>
 </table>
 </td>
</tr>
</table>
<table border="0" width="730"  align="center" class="unnamed1" cellspacing="1">
  <tr class="unnamed1">
    <td  align="center" width="100%" colspan="1">税款所属期间： 2018-01-01                 
    至  2018-03-31</td> 
  </tr>
</table>
<table border="0" width="730"  align="center" class="unnamed1" cellspacing="1"> 
  
  <tr  class="unnamed1" colspan="2">
    <td  align="left" width="60%"> 纳税人识别号： 91330723MA28DQKG8X</td>   
  </tr>
  <tr  class="unnamed1">
    <td  align="left" width="60%"> 纳税人名称： 武义合伟休闲用品有限公司</td>   
    <td  align="right" width="40%" > 金额单位：元(列至角分)</td> 
  </tr>
</table>

<table width="730" border="1" cellspacing="0" cellpadding="0" bordercolorlight="#000000" bordercolordark="#FFFFFF" align="center"  class="unnamed1" >
 <tr>
    <td width="8%" height="20" align="center" bgcolor="#FFFFFF">&nbsp;行次</td>
    <td width="60%" colspan="3" align="center" bgcolor="#FFFFFF">项　　　目</td>
    <td width="16%" align="center" bgcolor="#FFFFFF">本期金额</td>
    <td width="16%" align="center" bgcolor="#FFFFFF">累计金额</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">1</td>
    <td colspan="5" bgcolor="#FFFFFF">&nbsp;<b>一、按照实际利润额预缴</b></td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">2</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;营业收入</td>
    <td align="right">1145957.25 </td>
    <td align="right">1145957.25 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">3</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;营业成本</td>
    <td align="right">1016711.91 </td>
    <td align="right">1016711.91 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">4</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;利润总额</td>
    <td align="right">-738.66 </td>
    <td align="right">-738.66</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">5</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;加:特定业务计算的应纳税所得额</td>
    <td align="right">0</td>
    <td align="right">0</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">6</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;减:不征税收入和税基减免应纳税所得额（请填附表1）</td>
    <td align="right">0  </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">7</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;&nbsp;&nbsp;&nbsp;固定资产加速折旧（扣除）调减额（请填附表2）</td>
    <td align="right">0  </td>
    <td align="right">0  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">8</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;&nbsp;&nbsp;&nbsp;弥补以前年度亏损</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">9</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;实际利润额（4行+5行-6行-7行-8行）	</td>
    <td align="right">-738.66  </td>
    <td align="right">-738.66  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">10</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;税率（25%）</td>
    <td align="right">25  </td>
    <td align="right">25  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">11</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;应纳所得税额（9行×10行）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">12</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;减:减免所得税额（请填附表3）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">13</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;&nbsp;&nbsp;&nbsp;实际已预缴所得税额</td>
    <td align="center">————</td>
    <td align="right">0  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">14</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;&nbsp;&nbsp;&nbsp;特定业务预缴（征）所得税额</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">15</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;应补（退）所得税额（11行-12行-13行-14行）</td>
    <td align="center">————</td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">16</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;减：以前年度多缴在本期抵缴所得税额</td>
    <td align="right">0 </td>
    <td align="right">0</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">17</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;本月（季）实际应补（退）所得税额</td>
    <td align="center">————</td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">18</td>
    <td colspan="5" bgcolor="#FFFFFF">&nbsp;<b>二、按照上一纳税年度应纳税所得额平均额预缴</b></td>
  </tr>

  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">19</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;上一纳税年度应纳税所得额</td>
    <td align="center">————</td>
    <td align="right">0</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">20</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;本月（季）应纳税所得额（19行×1/4或1/12）</td>
    <td align="right">0</td>
    <td align="right">0</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">21</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;税率（25％）</td>
    <td align="right">25  </td>
    <td align="right">25  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">22</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;本月（季）应纳所得税额（20行×21行）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">23</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;减：减免所得税额(请填附表3）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">24</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;本月（季）实际应纳所得税额（22行-23行）</td>
    <td align="right">0 </td>
    <td align="right">0  </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">25</td>
    <td colspan="5" bgcolor="#FFFFFF">&nbsp;<b>三、按照税务机关确定的其他方法预缴</b></td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">26</td>
    <td colspan="3" bgcolor="#FFFFFF">&nbsp;本月（季）税务机关确定的预缴所得税额</td>
    <td align="right">0</td>
    <td align="right">0</td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">27</td>
    <td colspan="5" align="center" bgcolor="#FFFFFF"><b>总分机构纳税人</b></td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">28</td>
    <td width="14%" colspan="2" rowspan="4" align="center" bgcolor="#FFFFFF">总机构</td>
    <td width="46%" bgcolor="#FFFFFF">&nbsp;总机构分摊所得税额（15行或24行或26行×总机构<br>&nbsp;分摊预缴比例）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">29</td>
	<td  bgcolor="#FFFFFF">&nbsp;财政集中分配所得税额</td>
    <td align="right">0 </td>
    <td width="184" align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">30</td>
    <td bgcolor="#FFFFFF">&nbsp;分支机构分摊所得税额(15行或24行或26行×分支机<br>&nbsp;构分摊比例）</td>
    <td align="right">0</td>
    <td width="184" align="right">0 </td>
  </tr>
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">31</td>
    <td bgcolor="#FFFFFF">&nbsp;其中：总机构独立生产经营部门应分摊所得税额</td>
    <td align="right">0 </td>
    <td width="184" align="right">0 </td>
  </tr>
  
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">32</td>
	  <td colspan="2" rowspan="2" align="center" bgcolor="#FFFFFF">分支机构</td>
    <td bgcolor="#FFFFFF">&nbsp;分配比例（%）</td>
    <td align="right">0 </td>
    <td align="right">0 </td>
  </tr>
  
  <tr>
    <td height="20" align="center" bgcolor="#FFFFFF">33</td>
    <td bgcolor="#FFFFFF">&nbsp;分配所得税额</td>
    <td align="right">0  </td>
    <td align="right">0  </td>
  </tr>
  <tr>
     <td colspan="6"　bgcolor="#FFFFFF"><b>　　　是否属于小型微利企业：　　　　　　　　是<input type="checkbox" name="sfsyxxwlqy1" value="0" checked  disabled />　　　　　　　　　　　　否<input type="checkbox" name="sfsyxxwlqy2" value="0"  disabled /></b></td>
  </tr>
  
  <tr>
    <td colspan="6"><table width="98%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
        <td>　　谨声明：此纳税申报表是根据《中华人民共和国企业所得税法》、《中华人民共和国企业所得税法实施条例》和国家有关税收规定填报的，是真实的、可靠的、完整的。</td>
      </tr>
      <tr>
        <td height="42" valign="bottom">法定代表人（签字）：　　　　　　　　　　　　　　　　年　月　日</td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td height="104" colspan="6"><table width="98%" align="center"  class="style2" border="0" cellspacing="0" cellpadding="0" bordercolorlight="#000000" bordercolordark="#FFFFFF">
	<tr>
        	<td width="28%" class="" ><br>纳税人公章：<br><br>会计主管：<br><br>填表日期：　　年　　月　　日</td>
        	<td width="37%" class=""><br>代理申报中介机构公章：<br><br>经办人：<br><br>经办人执业证件号码：<br><br>代理申报日期：　   年　　月　　日</td>
        	<td width="33%" class=""><br>主管税务机关受理专用章：<br><br>受理人：<br><br>受理日期：　   年　　月　　日</td>
        </tr>
</table>
</td>
  </tr>
</table>

<table width="730" border="0"  align="center" cellpadding="0" cellspacing="1" class="unnamed1">
  	<tr>
  		<td  height="30">
  	<p align="right">国家税务总局监制&nbsp;&nbsp; 
  	   </td>
  	</tr>
  </table>  
</div>     
</body>     
     
</html>     



		       """

if __name__ == '__main__':
    from http_utils.http_response import HtmlResponse
    response = HtmlResponse(url='www.baidu.com', body=html.encode(), encoding='utf-8')
    ret = response.css_find_by_index('table:nth-child(4) tr:nth-child(18) td:nth-child(4)::text')
    ret = response.css_find_by_index('table:nth-child(4) tr:nth-child(18) td:nth-child(5)::text')
    print(ret)