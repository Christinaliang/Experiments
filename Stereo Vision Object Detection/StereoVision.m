%
% Perform Stereo Vision computation on a pair of images
%
% Authors:
%   Matt Holland
%   Ryan Gasik
%   Fatima Dominguez
%   Jaimiey Sears
%


%Path to the images
imgLeftPath = '..\calibrationImages\left02.png';
imgRightPath = '..\calibrationImages\right02.png';

%The min and max range to detect objects in the image (centimeters)
maxZ = 700;
minZ = 300;




%load the calibration data
load('calibration.mat');

% Read in the stereo pair of images.
I1 = imread(imgLeftPath);
I2 = imread(imgRightPath);
I1 = imresize(I1, [600 800]);
I2 = imresize(I2, [600 800]);

% Rectify the images.
[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);

%Compute the disparity of the images
disparityMap = disparity(rgb2gray(J1), rgb2gray(J2));

%Display disparity figure
%figure;
%imshow(disparityMap, [0, 64], 'InitialMagnification', 50);
%colormap('jet');
%colorbar;
%title('Disparity Map');


%Construct a point cloud from the disparity
pointCloud = reconstructScene(disparityMap, stereoParams);

% Convert from millimeters to centimeters.
pointCloud = pointCloud / 10 ;


% Plot points between 3 and 7 meters away from the camera.
z = pointCloud(:, :, 3);
zdisp = z;
zdisp(z < minZ | z > maxZ) = NaN;
pointCloudDisp = pointCloud;
pointCloudDisp(:,:,3) = zdisp;
Z = pointCloud(:, :, 3);

save('disparityMap.mat', 'Z', 'J1', 'disparityMap')


%Apply a mask over areas not within the given bounds
%mask = repmat(Z > 700 & Z < 1100, [1, 1, 3]);
%J1(~mask) = 0;
%figure
%imshow(J1, 'InitialMagnification', 50);

X = pointCloudDisp(:,:,1);
Y = pointCloudDisp(:,:,2);
Z = pointCloudDisp(:,:,3);

%Reshape X,Y, Z for plotting
Xs = reshape(X,[1 numel(X)]);
Ys = reshape(Y,[1 numel(Y)]);
Zs = reshape(Z,[1 numel(Z)]);

save('scatter.mat', 'Xs', 'Ys', 'Zs');
%
%scatter3(Xs,Ys,Zs,.01)