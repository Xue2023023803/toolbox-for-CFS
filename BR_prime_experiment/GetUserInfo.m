function [subName, scanNum, theDate] = GetUserInfo()

% function [subName, scanNum, theDate] = GetUserInfo();
% 获取用户信息：主体名称、扫描或实验编号以及当前日期
% 
% 创建者：Frank Tong，创建日期：2000年5月10日（原日期格式：mmddyy）
% 修改日期：2001年8月9日，修改为日期格式 yymmdd

% 从用户处获取主体姓名首字母
subName = input('\n age and gender of subject? (default="tmp")  ','s');		
if isempty(subName); subName = 'tmp'; end	% 如果没有输入，则默认为"tmp"

% 从用户处获取这次扫描的序列号
scanNum = input('\n Series number for this scan?  ','s');			

% 获取当前计算机上的日期，格式为'mm/dd/yy'
theDate = datestr(date,2);											
theDate(6) = []; theDate(3) = [];		% 删除日期中的'/'，转换为'mmddyy'

% 在2001年8月9日添加的行，修改日期格式为'yymmdd'
theDate = [theDate(5:6) theDate(1:2) theDate(3:4)];					

