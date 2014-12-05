%
% Perform Stereo Camera Calibration
%
% Authors:
%   Matt Holland
%   Ryan Gasik
%   Fatima Dominguez
%   Jaimiey Sears
%



%
% Config
%

% Number of calibration image pairs
numImagePairs = 3;

% Directory that the calibration images are stored in
imageDir = '.\calibrationImages\';

%The size of the squares on the calibration checkerbox
squareSize = 22; % millimeters


%
% Implementation
%

% path to the left images in the calibration pair
imageFiles1 = cell(numImagePairs, 1);

% path to the right images in the calibration pair
imageFiles2 = cell(numImagePairs, 1);

%generate path to calibration images
for i = 1:numImagePairs
    imageFiles1{i} = strcat(imageDir, sprintf('left%02d.png', i));
    imageFiles2{i} = strcat(imageDir, sprintf('right%02d.png', i));
end

%load the calibration images
images1 = cast([], 'uint8');
images2 = cast([], 'uint8');
for i = 1:numel(imageFiles1)
    %left image
    im = imread(imageFiles1{i});
    
    %scale down image to avoid running out of memory
    im = imresize(im, [600 800]);
    images1(:, :, :, i) = im;

    
    %Right Image
    im = imread(imageFiles2{i});
 
    %scale down image to avoid running out of memory
    im = imresize(im, [600 800]);
    images2(:, :, :, i) = im;
end

%Detect checkerbaord in images
[imagePoints, boardSize] = detectCheckerboardPoints(images1, images2);
 
% Display one image with the detected checkerboard
figure;
imshow(images1(:,:,:,1), 'InitialMagnification', 50);
hold on;
plot(imagePoints(:, 1, 1, 1), imagePoints(:, 2, 1, 1), '*-g');
title('Successful Checkerboard Detection'); 

% Generate world coordinates of the checkerboard points.
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Compute the stereo camera parameters.
stereoParams = estimateCameraParameters(imagePoints, worldPoints);

% Evaluate calibration accuracy.
figure;
showReprojectionErrors(stereoParams);

%save the calibration paramaters to a file for later use
save('calibration.mat', 'stereoParams')