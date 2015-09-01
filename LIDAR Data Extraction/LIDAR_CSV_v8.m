function LIDAR_CSV_v8(~) 
%Implemented:
% -Read / compute Input Data (distance and angle) (Ian Averman / Matt
% Delaney)
% -Sample code to compute (X,Y) coordinates for each point in a scan (Ian
% Averman)
% -Sample code to compute the top-left angle in a scan (Matt Delaney)
%Todo:
% -Improve left point selection using a median filter of some sort
% -Compute angles for every scan that has useable data
% -Determine which frames have usable data
   % -Possibly by detecting if By-Cy and Bx-Cx are sufficiently large

close all
clc

file = 'C:\Users\delaney15\Desktop\2014_11_11_10_54_57_359.csv';
global DATA;
if 1 ~= exist('DATA','var')
    DATA = xlsread(file);
end
[rows,cols] = size(DATA);

slits = rows-5;
scans = cols/2;
resol = 270/slits;
ANGLE = -45:resol:225;
if 1 ~= exist('DIST','var')
    DIST=zeros(1081,cols/2);
    %DIST (Scan, Data)
    for i = 1:scans
        DIST(:,i) = DATA(5:slits+5,2*i-1);
        %INTENS(:,i) = DATA(5:slits+5,2*i);
    end
end
%test scans are 1221 to 1427 on file 2014_11_11_10_54_57_359.csv
%SCAN Corresponds to scan # (SCAN - 1)
SCAN_MIN = 1222;
SCAN_MAX = 1428;

%preallocate memory for speed.
X = zeros(1,slits);
Y = zeros(1,slits);
%absolute (relative-to-the-arena) positions
Xabs = zeros(1,slits*(SCAN_MAX-SCAN_MIN));
Yabs = zeros(1,slits*(SCAN_MAX-SCAN_MIN));
Zabs = zeros(1,slits*(SCAN_MAX-SCAN_MIN));

for SCAN=SCAN_MIN:1:SCAN_MAX

    for j = 1:slits
        X(j) = DIST(j,SCAN)*cosd(ANGLE(j));
        Y(j) = DIST(j,SCAN)*sind(ANGLE(j));
    end

    % Building this triangle to find angle c:
    %      C
    %     / \    
    %    /   B
    %   /   
    %  /   
    % A 
    %
    % A is the due-west pixel. C is the top-left-most pixel. B is the pixel
    % where the "Jump" occurs.
    % Will use the law of cosines (http://en.wikipedia.org/wiki/Law_of_cosines)
    % to calculate.


    % The slit value for "due west" is roughly 900.
    %TODO: Change the slitA value dynamically (median filter?).
    slitA = 850; %changed from 900!!!!!!!
    Ax = X(slitA);
    Ay = Y(slitA);

    %The top-left pixel is the pixel in the top-left quadrant with the largest
    %distance value.
    [cDistGuess, cSlitGuess] = max(DIST(565:890,SCAN));
    %Correct for the fact that MATLAB thinks slit 565 is slit 1
    cSlitGuess = cSlitGuess + 565;
    %Find x and y values
    Cx = X(cSlitGuess);
    Cy = Y(cSlitGuess);

    %Find the bottom corner from the "sudden drop"
    [bDistGuess, bSlitGuess] = min(DIST(540:cSlitGuess,SCAN));
    bSlitGuess = bSlitGuess + 539;
    % We now have x and y values.
    Bx = X(bSlitGuess);
    By = Y(bSlitGuess);

    % Calculate the angle!
    AB = pdist([Ax,Ay;Bx,By],'euclidean');
    BC = pdist([Bx,By;Cx,Cy],'euclidean');
    AC = pdist([Ax,Ay;Cx,Cy],'euclidean');
    DISTANCE_FROM_LEFT_WALL = 1850;
    HEIGHT = 1100;
    %Law of cosines!
    cosOfAngleC = (AB*AB - BC*BC - AC*AC)/((-2)*AC*BC);
    angleC = acosd(cosOfAngleC);
    
    %calculate distance to the wall point
    y = DISTANCE_FROM_LEFT_WALL * sind(90-angleC) / sind(angleC);
    elevation = atand(HEIGHT / y);
    %code below is under development


    %we have spherical coordinates. Convert to XYZ.
    for j = 1:slits
        [Xt,Yt,Zt] = sph2cart(ANGLE(j)*(pi/180),(elevation)*(pi/180),DIST(j,SCAN));
        Xabs(j+slits*(SCAN-SCAN_MIN)) = Xt;
        Yabs(j+slits*(SCAN-SCAN_MIN)) = Yt;
        Zabs(j+slits*(SCAN-SCAN_MIN)) = Zt;
    end
end

%resolution to create the mesh at.
MESH_RESOLUTION = 500;
%Hard-coded values to try and focus on the arena surface and not the walls.
%Ian: X(-2750,2000),Y(2000,6000)
%FieldOnly: X(-1500,1500),Y(2000,5500)
XMIN = -1300;
XMAX = 1500;
YMIN = 2000;
YMAX = 5500;
xlin = linspace(XMIN,XMAX,MESH_RESOLUTION);
ylin = linspace(YMIN,YMAX,MESH_RESOLUTION);
%xlin = linspace(min(Xabs),max(Xabs),MESH_RESOLUTION);
%ylin = linspace(min(Yabs),max(Yabs),MESH_RESOLUTION);
[Xmesh,Ymesh] = meshgrid(xlin,ylin);
f = scatteredInterpolant(Xabs.',Yabs.',Zabs.');
Zmesh = f(Xmesh,Ymesh);
figure(1);
mesh(Xmesh,Ymesh,Zmesh);
xlabel('X');
ylabel('Y');
zlabel('Z');

%2x2 max filter
ZmeshFiltered = ordfilt2(Zmesh,4,ones(2,2));
figure(2);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('2D box maximum filter');
mesh(Xmesh,Ymesh,ZmeshFiltered);
view([0 -90]);
%average value is 2266, although the walls mess with this quite a bit.
% median is roughly 2170 for the test data.
medianValue = median(median(ZmeshFiltered(:)));
%low pass: 2170 - detection level (mm)
low_pass_offset = 230;
LOW_PASS_THRESHOLD = medianValue-low_pass_offset;
%high pass: 2170 + detection level (mm).
high_pass_offset = 70;
HIGH_PASS_THRESHOLD = medianValue+high_pass_offset;
% Apply the thresholds
ZmeshThresholdedLOW = ZmeshFiltered < LOW_PASS_THRESHOLD;
ZmeshThresholdedHIGH = (ZmeshFiltered > HIGH_PASS_THRESHOLD);
ZmeshThresholded = (ZmeshThresholdedLOW *(-1000)) + (ZmeshThresholdedHIGH * (1000));
figure(3);
subplot(1,2,1);
title('Basic Threshold Filter');
mesh(Xmesh,Ymesh,ZmeshThresholded);
xlabel('X');
ylabel('Y');
zlabel('Z');
view([0 90]);
%add some user interface tools
low_pass_box = uicontrol('Style', 'edit',...
    'Position', [400 0 120 20],...
    'String', num2str(low_pass_offset),...
    'Callback', @LowPassThreshUpdate); 
low_pass_box_label = uicontrol('Style','text',...
    'Position',[400 25 120 20],...
    'String','Pit Detection Depth (mm)');
high_pass_box = uicontrol('Style', 'edit',...
    'Position', [20 0 120 20],...
    'String', num2str(high_pass_offset),...
    'Callback', @HighPassThreshUpdate); 
high_pass_box_label = uicontrol('Style','text',...
    'Position',[20 25 150 20],...
    'String','Rock Detection Height (mm)');
figure(4);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Facility Depth Mesh with Pits highlighted');
mesh(Xmesh,Ymesh,ZmeshFiltered);

extractObstacles(ZmeshThresholdedLOW, 'b');
extractObstacles(ZmeshThresholdedHIGH, 'r');
    function extractObstacles(inputThresholdedMesh,circleColor)
        %FEATURE EXTRACTION TIME
        global PitMatrix;
        PitMatrix = bwmorph(inputThresholdedMesh, 'erode');
        newRows = YMAX - YMIN;
        newCols = XMAX - XMIN;
        PitMatrix = imresize(PitMatrix, [newRows newCols]);
        % Only pay attention to the obstacle area
        PitMatrix = PitMatrix(1:2500,:);
        global PIT_STATS; 
        PIT_STATS = regionprops(PitMatrix, 'Area', 'Centroid', 'MajorAxisLength', 'MinorAxisLength', 'Orientation','EquivDiameter');                    
        
        %imagesc(flip(PitMatrix,1));
        hold on
        for k= 1:size(PIT_STATS)
            %draw circles to the plots we've made indicating where the pits
            %are
            figure(4);
            viscircles(PIT_STATS(k).Centroid + [XMIN YMIN], PIT_STATS(k).EquivDiameter /2,'LineStyle','-', 'EdgeColor',circleColor);
            figure(3);
            subplot(1,2,1);
            viscircles(PIT_STATS(k).Centroid + [XMIN YMIN], PIT_STATS(k).EquivDiameter /2,'LineStyle',':','EdgeColor',circleColor);
            subplot(1,2,2);
            viscircles(PIT_STATS(k).Centroid + [XMIN YMIN], PIT_STATS(k).EquivDiameter /2,'LineStyle',':','EdgeColor',circleColor);
        end
        figure(4);
        view([1 -90]);
        hold off

    end



        function LowPassThreshUpdate(src, ~)
            updateFilterVal=get(src,'String');
            if isempty(str2double(updateFilterVal))
                set(src,'string','0');
                warndlg('Input must be numerical');
            else
                low_pass_offset = str2double(updateFilterVal);
                %recalculate the thresholds
                LOW_PASS_THRESHOLD = medianValue-low_pass_offset;
                %high pass: 2170 + detection level (mm).
                HIGH_PASS_THRESHOLD = medianValue+high_pass_offset;
                ZmeshThresholdedLOW = (ZmeshFiltered < LOW_PASS_THRESHOLD);
                ZmeshThresholdedHIGH = (ZmeshFiltered > HIGH_PASS_THRESHOLD);
                ZmeshThresholded = (ZmeshThresholdedLOW *(-1000)) + (ZmeshThresholdedHIGH * (1000));
                figure(3);
                mesh(Xmesh,Ymesh,ZmeshThresholded);
                view([0 90]);
            end
        end
            function HighPassThreshUpdate(src, ~)
            updateFilterVal=get(src,'String');
            if isempty(str2double(updateFilterVal))
                set(src,'string','0');
                warndlg('Input must be numerical');
            else
                high_pass_offset = str2double(updateFilterVal);
                %recalculate the thresholds
                LOW_PASS_THRESHOLD = medianValue-low_pass_offset;
                %high pass: 2170 + detection level (mm).
                HIGH_PASS_THRESHOLD = medianValue+high_pass_offset;
                ZmeshThresholdedLOW = (ZmeshFiltered < LOW_PASS_THRESHOLD);
                ZmeshThresholdedHIGH = (ZmeshFiltered > HIGH_PASS_THRESHOLD);
                ZmeshThresholded = (ZmeshThresholdedLOW *(-1000)) + (ZmeshThresholdedHIGH * (1000));
                 figure(3);
                mesh(Xmesh,Ymesh,ZmeshThresholded);
                view([0 90]);
            end
        end
%figure(3);
%scatter3(Xabs,Yabs,Zabs,1,'.');
%xlabel('X');
%ylabel('Y');
%zlabel('Z');
   end