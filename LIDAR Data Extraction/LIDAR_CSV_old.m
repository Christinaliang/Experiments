close all
clear
clc

file = 'E:\LIDAR Data\CSV\2014_11_11_10_48_51_093.csv';
DATA = xlsread(file);
[rows,cols] = size(DATA);

slits = rows-5;
scans = cols/2;
resol = 270/slits;
ANGLE = -45:resol:225;

for i = 1:scans
    DIST(:,i) = DATA(5:slits+5,2*i-1);
    %INTENS(:,i) = DATA(5:slits+5,2*i);
end

SCAN = 1;

hold on
for j = 1:slits
    X = DIST(SCAN,j)*cosd(ANGLE(j));
    Y = DIST(SCAN,j)*sind(ANGLE(j));
    plot(X,Y);
end
hold off