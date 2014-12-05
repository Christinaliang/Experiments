%
% Display a 3D scatter plot of the data
%
% Authors:
%   Matt Holland
%   Ryan Gasik
%   Fatima Dominguez
%   Jaimiey Sears
%

%load scatter plot data
load('scatter.mat')

%display it as a figure
figure
scatter3(Xs,Ys,Zs,.01)