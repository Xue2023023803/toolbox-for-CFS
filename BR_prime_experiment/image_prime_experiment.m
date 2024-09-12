clear all
try  
%% 定义保存路径
save_data=1; % 1=yes; 0=no
if(save_data==1)    
    [subName scanNum theDate]=GetUserInfo; 
end
%% 开窗口
PsychJavaTrouble
AssertOpenGL
Priority(2) %%%设置该程序的优先顺序;
Screen('Preference', 'SkipSyncTests', 2); %%%强行通过所有自检和定标
Screen('Preference','Verbosity',0);
Screen('Preference','SuppressAllWarnings',1);
scr_nbr=max(Screen('Screens'));
[w, scr_rect]=Screen('OpenWindow', scr_nbr);
 HideCursor;
% Coordinates of the centre of the screen
centreX=scr_rect(3)/2;
centreY=scr_rect(4)/2;
shCenter = (scr_rect (3) - scr_rect (1))/2;
svCenter = (scr_rect (4) - scr_rect (2))/2;
black = BlackIndex(w);  % Retrieves the CLUT color code for black.
white = WhiteIndex(w);  % Retrieves the CLUT color code for white.
grey = (black + white) / 2;  % Computes the CLUT color code for grey.
if round(grey)==white
    grey=black;
end
background_colour = black; 
%% 刺激与背景;
BG_LUM=0;% 1=mean lum of the patterns; 0-1; .5 is half the lum of the patterns. 
% the contrast of the stimulus. range=0:1; 
freq=7;  
red_con= 0.2467; % 0.3413; % right oreintation, and red  
green_con= 0.5806; %0.6911; % left O, and green 
GreenFactor = 0.65;
waitFrames=1; % this is for the BR ramps. 
colorR = [1 0 0]; %RED PATTERN
colorG = [0 1 0]; %GREEN PATTERN
colorG = colorG*GreenFactor;
 stepS=1; 
ramp_lin=1:stepS:100; 
ramp_lin=ramp_lin/100; %调节亮度
%% 时间参数
time_ima = 7; %6; % + 2 secs = 7imaginery time
time_stim = 0.75; % stimuli time
time_resp = 0.75; % response window
time_cue = 1; % letter cue time
time_intratrial =1; %time between trials
ISI2=time_ima;% the long period time to hold pattern in mem.
%% 指引参数
metacognition=1; % =1 to get confidence ratings 1-4 =0 to not. 
luminance_manipulation=1; % 1 for luminance on during generation, 2 for off.
mockBR_counter=1; 
real_BR_counter=1; 
%% 按键设置
KbName('UnifyKeyNames');
OneKey=KbName('1');
TwoKey=KbName('2');
ThreeKey=KbName('3');
OneUpKey=KbName('1!');
TwoUpKey=KbName('2@');
ThreeUpKey=KbName('3#');
%% 反应变量
Same=0;
Different = 0;
GreenOverall=0;
RedOverall=0;
MixedOverall=0;
RR = 0;
GG = 0;
RG = 0;
GR = 0;
RM = 0;
GM = 0;
%% 文本与注视点参数设置
text_colour = 50; %colour of cue
text_size = 85; %size of CUE
% Fixation point parameters.
re=6; % external circle radius
ri=4; % internal circle radius
% fixation point colours
fixpt_int=0; % black centre
fixpt_ext=100; % white-ish circle
%% 创造红绿光栅
% *** To lengthen the period of the grating, increase pixelsPerPeriod.
pixelsPerPeriod = 33; % How many pixels will each period/cycle occupy?
spatialFrequency = .75 / pixelsPerPeriod; % How many periods/cycles are there in a pixel?
radiansPerPixel = spatialFrequency * (2 * pi); % = (periods per pixel) * (2 pi radians per period)
periodsCoveredByOneStandardDeviation = 1.5;
gaussianSpaceConstant = periodsCoveredByOneStandardDeviation  * pixelsPerPeriod;
% *** If the grating is clipped on the sides, increase widthOfGrid.
widthOfGrid = 500;
halfWidthOfGrid = widthOfGrid / 2;
widthArray = (-halfWidthOfGrid) : halfWidthOfGrid;  % widthArray is used in creating the meshgrid.
absoluteDifferenceBetweenWhiteAndGray = abs(white - grey);
[x y] = meshgrid(widthArray, widthArray);
 % cardinals
 grat_angle1=pi/2; % left. 
  grat_angle2=2*pi ;
 % circularGaussianMaskMatrix = exp(-((x .^ 2) + (y .^ 2)) / (gaussianSpaceConstant ^ 2.3));%2.3  
 %%%%%%%%%% 
  gratingMatrix1 =(sin(freq*2*pi/halfWidthOfGrid*(x.*sin(grat_angle1)+y.*cos(grat_angle1))-0));
  gratingMatrix2 =(sin(freq*2*pi/halfWidthOfGrid*(x.*sin(grat_angle2)+y.*cos(grat_angle2))-0));
  gratingMatrix2=((gratingMatrix2*red_con)*127)+(127); 
    gratingMatrix1= ((gratingMatrix1*green_con)*127)+(127); 
  circularGaussianMaskMatrix = exp(-((x .^ 2) + (y .^ 2)) / (gaussianSpaceConstant ^ 2.3));%2.3
  imageMatrixG = gratingMatrix1 .* circularGaussianMaskMatrix;
  imageMatrixR = gratingMatrix2 .* circularGaussianMaskMatrix;
%% 创造mock
mock_right=imageMatrixR;
mock_left=imageMatrixG;
amp=27;
EE=smooth((smooth(amp*randn(1, widthOfGrid), 35))+250); % was 100 at the end 
% makes the appropriate sections value of 0; so the two images can be added
% together. 
EE=round(EE); 
for loop=1:widthOfGrid    
mock_right(1:(EE(loop)), loop)=0;
mock_left((EE(loop)):widthOfGrid, loop)=0;   
end 
%% 创造颜色
pattern1 = zeros([size(imageMatrixR) 3]);
pattern2 = zeros([size(imageMatrixR) 3]);
Mock_patternLeft = zeros([size(mock_left) 3]);
Mock_patternRight = zeros([size(mock_left) 3]);


pattern1(:,:,1)=colorR(1)*abs(imageMatrixR);
pattern1(:,:,2)=colorR(2)*abs(imageMatrixR);
pattern1(:,:,3)=colorR(3)*abs(imageMatrixR);

pattern2(:,:,1)=colorG(1)*abs(imageMatrixG);
pattern2(:,:,2)=colorG(2)*abs(imageMatrixG);
pattern2(:,:,3)=colorG(3)*abs(imageMatrixG);

Mock_patternRight(:,:,1)=colorG(1)*abs(mock_left);
Mock_patternRight(:,:,2)=colorG(2)*abs(mock_left);
Mock_patternRight(:,:,3)=colorG(3)*abs(mock_left);

Mock_patternLeft(:,:,1)=colorR(1)*abs(mock_right);
Mock_patternLeft(:,:,2)=colorR(2)*abs(mock_right);
Mock_patternLeft(:,:,3)=colorR(3)*abs(mock_right);

  meanRED=(max(max(pattern1(:,:,1))))/2;
meanGREEN=(max(max(pattern2(:,:,2))))/2;

meanRED=(meanRED*BG_LUM)*1.4;
meanGREEN=(meanGREEN*BG_LUM)*1.4;
%% 融合
pattern = pattern1 + pattern2; 
Pattern_Mock= Mock_patternRight + Mock_patternLeft; 
%% 光栅与mock位置设置
[Y X Z]= size(pattern);
side(1)=centreX-X/2;
side(2)=centreY-Y/2;
side(3)=centreX+X/2;
side(4)=centreY+Y/2;
patch_sizeS(1)=0;
patch_sizeS(2)=0; 
patch_sizeS(3)=X;
patch_sizeS(4)=Y;
%% 纹理装载
texture_BR=Screen('MakeTexture', w, pattern);
texture_Mock=Screen('MakeTexture', w, Pattern_Mock);
%% 试次设置
ntrials=120;
cases = zeros(ntrials,1); %trials * R & G
array1=1:ntrials;
array8=1:round((ntrials)*.875);
 cue_array=mod(array8, 2); 
 cue_array=Shuffle(cue_array);
 array8=1:round((ntrials)*.125);
mock_cue_array =mod(array8, 2); 
 mock_cue_array=Shuffle(mock_cue_array);
 % phase jitter. 
 array2=mod(array1, 10); 
phase_array= Shuffle(array2)*4;
% mock BR trail array. 
array2=mod(array1, 8); 
condition_array=Shuffle(array2); 

 FlushEvents;
 
 %% 呈现实验开始
 Screen('FillRect', w, background_colour);
Screen('TextSize',w, 40);
Screen('DrawText', w, '按任意键开始', centreX/3,centreY/3, [100 100 100]);
Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
Screen('Flip',w);
FlushEvents;
 while GetChar==0 
 end
 
 %% 实验循环
 for t=1:ntrials
     FlushEvents;  
      %% 呈现线索（1s)
      if condition_array(t)==1 % 12.5% of trials are mock.
            if mock_cue_array(mockBR_counter)==1
                cue = 'R';
            elseif mock_cue_array(mockBR_counter)==0
                cue = 'G';
            end
      else
            if cue_array(real_BR_counter)==1
                cue = 'R';
            elseif cue_array(real_BR_counter)==0
                cue = 'G';
            end
      end
       Screen('FillRect', w, background_colour);
    
    
    Screen('TextSize',w, text_size);
    TextWidth = Screen (w,'TextBounds', cue);
    Screen (w, 'DrawText', cue,shCenter-(TextWidth(3)/2), svCenter-(TextWidth(4)/2),text_colour);
    Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
    Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
     Screen('Flip',w);
    auxTime=GetSecs;
    while(GetSecs<=auxTime+time_cue)
    end
    %% 亮度变化 与表象（7s)
%     if luminance_manipulation==1
%       % Ramp the lum up 
%             for lumL=1:length(ramp_lin) % ramps up over 100 frames 
%                 Screen('FillRect', w, [meanRED*ramp_lin(lumL) meanGREEN*ramp_lin(lumL) 0]);%这里设置mean为0，所以没有亮度变化
%                 Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
%                 Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
%                  Screen('Flip', w, waitFrames);
%             end            
%             % wait at full lum
%              start=GetSecs;
%             while  (GetSecs-start < ISI2);  
%             end                      
%             % ramp the lum back down. 
%             for lumL=1:length(ramp_lin)
%                 Screen('FillRect', w, [meanRED*ramp_lin(round(101-lumL)) meanGREEN*ramp_lin(round(101-lumL)) 0]);
%                 Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
%                 Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
%                 Screen('Flip', w, waitFrames);
%             end   
% else
    
     Screen('FillRect', w, background_colour);
    Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
    Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
    Screen('Flip',w);          
auxTime=GetSecs;
while(GetSecs<=auxTime+time_ima)
end   

%% 清晰度评估(按键反应)
 if metacognition==1           
            cue = '清晰度?';
            Screen('TextSize', w, text_size);      
            TextWidth = Screen (w,'TextBounds', cue);
            Screen (w, 'DrawText', cue,shCenter-(TextWidth(3)/2), svCenter-(TextWidth(4)/2),text_colour);
            Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
            Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
            Screen('Flip', w);            
            %      start=GetSecs;
                 %while  (GetSecs-start < ISI2); end %          
            [ch, when] = GetChar; %按键
            %tt=find(keyCode);
            if (ch=='1')
                metaC_array(t)=1;
            elseif     (ch=='2')
                metaC_array(t)=2;
            elseif     (ch=='3')
                metaC_array(t)=3;
            elseif (ch=='4')
                metaC_array(t)=4;
            end
           FlushEvents('keyDown');
            FlushEvents; 
            % give a bit of time before presenting the question stimulus
            Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
            Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
            Screen('Flip', w);                                
 end
            FlushEvents('keyDown'); 
 %% 呈现刺激（0.65）
  if condition_array(t)==1 % 25% of trials are mock. 
        Screen('DrawTexture', w, texture_Mock, patch_sizeS,side);
    else
        Screen('DrawTexture', w, texture_BR, patch_sizeS,side);
  end
    Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
    Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
    
    Screen('Flip',w);
    
     Snd('Play',sin(100:1000));
    
    auxTime=GetSecs;
    while(GetSecs<=auxTime+time_stim)
    end
    %% 按键反应颜色   
    Screen('FillRect', w, background_colour);
%    cue = '按键反应';
%    Screen('TextSize', w, text_size);
%    TextWidth = Screen (w,'TextBounds', cue);
%    Screen (w, 'DrawText', cue,shCenter-(TextWidth(3)/2), svCenter-(TextWidth(4)/2),text_colour);
    Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
    Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
    Screen('Flip',w);
     %KbWait;       
        [ch, when] = GetChar;
        %tt=find(keyCode);    
        if (ch=='1')
            response_array(t)=1;
        elseif     (ch=='2')
            response_array(t)=2;
        elseif     (ch=='3')
            response_array(t)=3;
        end  
  %ch        
       FlushEvents('keyDown');
        FlushEvents;
 auxTime=GetSecs;
    while(GetSecs<=auxTime+time_intratrial)
    end
    if condition_array(t)==1 % 25% of trials are mock.
        mockBR_counter=mockBR_counter+1;    
    else
        real_BR_counter=real_BR_counter+1;
    end
    if t==60;
    Screen('TextSize',w, 40);
 Screen('DrawText', w, '休息一下', centreX/3,centreY/3, [100 100 100]);   
Screen('DrawText', w, '按任意键继续', centreX/2,centreY/2, [100 100 100]);
Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
Screen('Flip',w);
FlushEvents;
 while GetChar==0 
 end
    end
 end
 Screen('TextSize',w, 40);
Screen('DrawText', w, '实验结束 ', centreX/3,centreY/3, [100 100 100]);
Screen('DrawText', w, '谢谢您的参与 ', centreX/2,centreY/2, [100 100 100]);
Screen('FillOval', w, fixpt_ext, [centreX-re centreY-re centreX+re centreY+re]);
Screen('FillOval', w, fixpt_int, [centreX-ri centreY-ri centreX+ri centreY+ri]);
Screen('Flip',w);
pause(3);
 %% 整理数据
 primed=zeros(1, ntrials); 
mixed=zeros(1, ntrials); 
mock_primed=zeros(1, ntrials); 
mixed_percept=zeros(1, ntrials);
mock_counter=1; 
BR_cue_counter=1; 
% Meta_primed=zeros(ntrials, 4);
% % 
for aa=1:length(response_array)           
       if condition_array(aa)==1  % mock.                       
               if mock_cue_array(mock_counter)==1 && response_array(aa)==3 % R
                mock_primed(aa)=1;

               elseif mock_cue_array(mock_counter)==0 && response_array(aa)==1 % G

                  mock_primed(aa)=1; 
               end
           
           mock_counter=mock_counter+1;
                             
       elseif condition_array(aa)~=1 
                     
               if cue_array(BR_cue_counter)==1 && response_array(aa)==3 % R

                   primed(aa)=1;                  
%                    Meta_primed(aa,metaC_array(aa))=1; 
%                  
               elseif cue_array(BR_cue_counter)==0 && response_array(aa)==1 % G

                   primed(aa)=1;
%                     Meta_primed(aa,metaC_array(aa))=1; 
                end
%                
               
               if response_array(aa)==2
                   
                   mixed_percept(aa)=1; 
                   
               end 
                             
               BR_cue_counter=BR_cue_counter+1;
                          
       end 
                     
end 
 Rate_BRprimed=(sum(primed)/((ntrials*.8)-sum(mixed_percept)))*100;
 Rate_Mockprimed=(sum(mock_primed)/(ntrials*.2))*100;
 vivid_sum=sum(metaC_array);
 %% 结束
 Priority(0);
Screen('CloseAll');
ShowCursor;

catch

        
ShowCursor;
Screen('CloseAll');
psychrethrow(lasterror);
    
end
%% 保存数据
if save_data==1         
    outfilename=['imagery_glass' subName scanNum '_'  theDate '_.mat'];
    aa=num2str(outfilename);
    save(aa); % saves everything
end
