% inspired by 
% https://blogs.mathworks.com/graphics/2015/03/16/how-the-tiger-got-its-stripes/

clear
 
% writerObj = VideoWriter('brusselator', 'MPEG-4');
% %writerObj.Quality = 75;
% writerObj.FrameRate = 20;
% open(writerObj);





%%%%%%%%%%% BRUSSELATOR PARAMETERS %%%%%%%%%%%%

% scaling_factor = 10; % works great!
scaling_factor = 7;
% wave number ~ 1/sqrt(diffusion rate)

% stripes
% scaling_factor = 1;
dV = 10*scaling_factor; % should be fixed
A = 3; % should be fixed
% dU = 4*scaling_factor;
% B = 10.2;

% honeycomb
dV = 10*scaling_factor; % should be fixed
A = 3; % should be fixed
dU = 5.2*scaling_factor;
B = 10.2;

% hexa_dots
% dV = 10*scaling_factor; % should be fixed
% A = 3; % should be fixed
% dU = 2*scaling_factor;
% B = 11;

% % osc_hex
% dV = 10*scaling_factor; % should be fixed
% A = 3; % should be fixed
% dU = 5.6*scaling_factor;
% B = 10.2;

% test
% dV = 10*scaling_factor; % should be fixed
% A = 3; % should be fixed
% dU = 6*scaling_factor;
% B = 10.5;

% oscillating stripes
% scaling_factor = 1;
% dV = 10*scaling_factor; % should be fixed
% A = 3; % should be fixed
% dU = 6.1*scaling_factor;
% B = 10.5;

% oscillating squares?
% mind the scaling_factor... large = better
% small means more dots get crammed 
% dU = 6.0*scaling_factor;
% B = 10.25;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%% GRAY-SCOTT PATTERNS &&&&&&&&&&&&&&

% pattern type:
%scaling_factor = 0.25;

% spreading_loops
% f = 0.04; % feed
% k = 0.06; % kill

% chaotic_growth:
% f = 0.018; % feed
% k = 0.051; % kill

% f = 0.02; % feed
% k = 0.05; % kill

% stripey_droplets
% f = 0.055;
% k = 0.063;

% mitosis
% f=.0367; 
% k=.0649;
% 

% dU = 1*scaling_factor;
% dV = 0.5*scaling_factor;

%%%%%%%%%%%%%%%%%%%%%%%%%%

% Size of grid for osc_patterns
width = 128;
% Size of grid for stable_patterns
% width = 1024;
% Size of grid for GRAY-SCOTT
% width = 256;
% osc_patterns dt
dt = 0.001;

% dt for GRAY-SCOTT
% A = 1; % ignore this 
% B = 1; % ignore this
% dt = 0.25;
% t=0;


stoptime = 200000;
[t, U, V] = initial_conditions(width, A, B);
axes('Position',[0 0 1 1])
axis off
% Add a scaled-color image
figure(1);
hi = image(U);
hi.CDataMapping = 'scaled'; % or scaled
colormap gray

% And a text object to show the current time.
ht = text(5,width-5,'Time = 0');
ht.Color = [.95 .2 .8];
drawnow
tic
n_frames = 1;
loop_count = 250;



while t<stoptime
    % brusselator
    U = U + (dU*laplacian(U) + A - (B+1).*U + V.*U.^2)*dt; 
    V = V + (dV*laplacian(V) + B.*U - V.*U.^2)*dt;

    % Gray-Scott
%     U = U + (dU*laplacian(U) - U.*V.^2 + f.*(1-U))*dt;
%     V = V + (dV*laplacian(V) + U.*V.^2 - (f+k).*V)*dt;

    hi.CData = U;
    t = t+dt;
    ht.String = ['Time = ' num2str(t)];
    
    drawnow;
    
%   for movie writing

%     if loop_count > 500
%          drawnow;
%          loop_count = 0;
%      else
%          loop_count = loop_count + 1;
%      end
    
%     generate a movie
%     if loop_count > 250
%         writeVideo(writerObj,getframe(1));
%         loop_count = 0;
%     else
%         loop_count = loop_count + 1;
%     end
end

%close(writerObj);
delta = toc;



%%%%%%%%% FUNCTIONS %%%%%%%%%%




function [t, U, V] = initial_conditions(n, A, B)
t = 0;


% BRUSSELATOR
U = A + rand(n);
V = B/A + rand(n);

% %GRAY-SCOTT
% U = ones(n);
% % Initialize V to zero which a clump of ones
% V = zeros(n);
% V(round(n/2)-1:round(n/2)+1 ,round(n/2)-1:round(n/2)+1) = 1;
% V(round(n/2)-1+6:round(n/2)+1+6, round(n/2)-1+6:round(n/2)+1+6) = 1;

% % PHOTO
% %I1=imread('C:\Users\buiqu\Documents\GitHub\huanium\LaTeX projects\HuanBui_ExpNonLinear\Project 2\mccoy.jpg');
% I1=imread('/home/huanium/Desktop/huanium/LaTeX projects/HuanBui_ExpNonLinear/Project 2/mccoy.jpg');
% I2 = imresize(I1,[512 512]); 
% In=im2double(rgb2gray(I2)); 
% U = In/100;
% V = In/100;


end
  
% circshift ensures periodic boundary condition
function out = laplacian(in)
out = -in ...
    + 0.25*(circshift(in,[ 1, 0]) + circshift(in,[-1, 0])  ...
    +      circshift(in,[ 0, 1]) + circshift(in,[ 0,-1])); ...
    
    % this diagonal shift term introduces some weirdness... do not include
    %- (.25/8)*(circshift(in,[ 1, 1]) + circshift(in,[-1, 1])  ...
    %+      circshift(in,[-1,-1]) + circshift(in,[ 1,-1]));

end

  
  