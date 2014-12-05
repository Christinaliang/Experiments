%
% Display the disparity and apply masks
%
% Authors:
%   Matt Holland
%   Ryan Gasik
%   Fatima Dominguez
%   Jaimiey Sears
% 

function mygui
    % Create a figure and axes
    f = figure('Visible','off');
    ax = axes('Units','pixels');
	
    myVars = load('disparityMap.mat');
    Z = myVars.Z;
    J1 = myVars.J1;
    disparityMap = myVars.disparityMap;
    mask = repmat(Z > 100 & Z < 220, [1, 1, 3]);
    J1(~mask) = 0;
    imshow(J1, 'InitialMagnification', 50);  
    
    minTxt = uicontrol(f,'Style','edit',...
                'String','100',...
                'Position',[100 50 100 20]);

    minLbl = uicontrol('Style','text',...
        'Position',[20 50 60 20],...
        'String','Min Bound');
            
    
    maxTxt = uicontrol(f,'Style','edit',...
                'String','220',...
                'Position',[100 20 100 20]);

    minLbl = uicontrol('Style','text',...
        'Position',[20 20 60 20],...
        'String','Max Bound');
					
    remaskBtn = uicontrol('Style','pushbutton',...
        'Position',[220 35 60 20],...
        'String','Re-Mask',...
        'Callback', @remask);

    colormapBtn = uicontrol('Style','pushbutton',...
        'Position',[420 20 100 20],...
        'String','Disparity Map',...
        'Callback', @disparityMapDisp);
    
    % Make figure visble after adding all components
    set(f,'Visible','on')
    
     function disparityMapDisp(source, callbackdata)
        figure;
        imshow(disparityMap, [0, 64], 'InitialMagnification', 50);
        colormap('jet');
        colorbar;
        title('Disparity Map'); 
     end
    
     function remask(source, callbackdata) 
        minBound = str2num(get(minTxt, 'string'));
        maxBound = str2num(get(maxTxt, 'string'));
        
        Z = myVars.Z;
        J1 = myVars.J1;
        
        %Filter out distances
        mask = repmat(Z > minBound & Z < maxBound, [1, 1, 3]);
        J1(~mask) = 0;
        imshow(J1, 'InitialMagnification', 50);
     end
end