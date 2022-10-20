% Author: Huan Q. Bui
% Colby College '21
% Date: Mar, 2021


%%% THIS CODE IS FOR STUDYING THE POWER-LAW
%%% DECAY OF CONVOLUTION POWER
%%% THE ALGORITHM RELIES ON THE FACT THAT THE
%%% CONV POWER IS ASSOCIATIVE


clear
close all

%%%%%%%%%%%%%%%%%%%
% clock starts
tic 
% clock starts
%%%%%%%%%%%%%%%%%%%


%%% max |\phi^(n) (x)| vs. n  %%%%%%%
 
support_bound = 1000;
sup = [];
points = 13; % how many data points? ==> goes to 2^points convolutions 
steps = 2:1:points; % start with Phi^(0) = Phi, end at Phi^(2^points-1)
% muP = 1/2+1/4;
% muP = 1/2 + 1/8;
% muP = 1/2 + 1/2;
% muP = 1/2 + 1/6;
% muP = 1/4 + 1/4;
muP = 1/2 + 1/2;
% initialize Phi^(2)
conv = fast_convolve(1, support_bound); % create Phi^(1) = Phi*Phi
M = max(abs(conv) , [], 'all'); % find max;
sup = [sup M]; % concatenate
n = [1];   % first entry is Phi^(1) = Phi*Phi
for n_times = steps
    n = [n 2^n_times-1];
    %conv = Nth_fast_convolve(conv, 1, support_bound); % take the conv square
    conv = fast_convolve(2^n_times-1, support_bound); % take the conv square
    M = max(abs(conv) , [], 'all'); % find max;
    sup = [sup M]; % concatenate
    disp(['Progress: ' num2str(n_times) ' out of ' num2str(1+length(steps)) ...
        ', n = ' num2str(2^n_times-1)]);
end
% figure for SUP
figure(1)
p1 = plot(log2(n),log2(sup), '-o', 'color','blue', 'LineWidth', 1) % plot log instead
%xlim([0 max(n)])
%ylim([-0.01 0.7])
xlabel('log_2(n)', 'FontSize',16);
ylabel('', 'FontSize', 16 );
hold on 
nY = 2*n.^(-muP);
p2 = plot(log2(n), log2(nY), 'LineWidth', 2, 'Color', 'red')  % plot log instead
hold off
legend('log_2 f(n)', 'log_2(n^{-1})', 'FontSize',14);





%%%%%%%%%%%%%%%%%%%
% clock ends
Duration = seconds(round(toc));
Duration.Format = 'hh:mm:ss';
disp(['Time taken : ' char(Duration)]);
disp(['Time in sec: ' num2str(toc)]);
disp(' ');
% clock ends
%%%%%%%%%%%%%%%%%%%





%------ New Fast Convolve ---------
function conv_power = Nth_fast_convolve(PhiN, n_times, support_bound)

% convolve an existing PhiN n_times --> get [Phi^(N*n_times)]
conv_power = PhiN;
k=0;
while k < n_times
    k = k + 1;
    conv_power = conv2(PhiN, conv_power, 'full');
    dim_f = size(conv_power);
    
    if dim_f(1) > support_bound || dim_f(2) > support_bound
        conv_power = cropND(conv_power, support_bound);
    end
end
end















%------- Nth Fast Convolve ----------

function conv_power = fast_convolve(n_times, support_bound)


% Phi = zeros(3,3);
% shift = floor(3/2)+1;
% Phi( 0+shift, 1+shift)  =  1/4;
% Phi( 0+shift,-1+shift)  = 1/4;
% Phi( 1+shift, 0+shift)  = 1/4;
% Phi(-1+shift, 0+shift)  = 1/4;
% 




% simple Example with E = diag(1/4, 1/4).
% no cross terms


% Phi = zeros(9,9);
% shift = floor(9/2)+1;
% 
% Phi( 0+shift, 0+shift)  =  complex(93/128, -3/16);
% Phi( 1+shift, 0+shift)  = complex(7/64, 1/16);
% Phi(-1+shift, 0+shift)  = complex(7/64, 1/16);
% Phi( 2+shift, 0+shift)  = -complex(7/128, 1/64);
% Phi(-2+shift, 0+shift)  = -complex(7/128, 1/64);
% Phi( 3+shift, 0+shift)  = 1/64;
% Phi(-3+shift, 0+shift)  = 1/64;
% Phi( 4+shift, 0+shift)  = -1/512;
% Phi(-4+shift, 0+shift)  = -1/512;
% Phi( 0+shift, 1+shift)  = complex(7/64, 1/16);
% Phi(-0+shift,-1+shift)  = complex(7/64, 1/16);
% Phi( 0+shift, 2+shift)  = -complex(7/128, 1/64);
% Phi(-0+shift,-2+shift)  = -complex(7/128, 1/64);
% Phi( 0+shift, 3+shift)  = 1/64;
% Phi(-0+shift,-3+shift)  = 1/64;
% Phi( 0+shift, 4+shift)  = -1/512;
% Phi(-0+shift,-4+shift)  = -1/512;

% EXAMPLE 0 in the paper
Phi = zeros(5,5);
shift = floor(5/2)+1;

Phi( 0+shift, 0+shift)  =  (1/192)*(144 - 64i);
Phi( 1+shift, 0+shift)  = (1/192)*(16 + 16i);
Phi(-1+shift, 0+shift)  = (1/192)*(16 + 16i);
Phi( 2+shift, 0+shift)  = -4*(1/192) ;
Phi(-2+shift, 0+shift)  = -4*(1/192)  ;    
Phi( 0+shift, 1+shift)  = (1/192)*(16+16i);
Phi( 0+shift,-1+shift)  = (1/192)*(16+16i);
Phi( 0+shift, 2+shift)  = -4*(1/192);
Phi( 0+shift,-2+shift)  = -4*(1/192);
Phi( -1+shift, -1+shift)  = (1/192)*1i;  
Phi( 1+shift, -1+shift)  = -(1/192)*1i;   
Phi( -1+shift, 1+shift)  = -(1/192)*1i;  
Phi( 1+shift, 1+shift)  = (1/192)*1i;  


% %%%%% EXAMPLE 1 in PAPER %%%%%%%%%%%
% Phi = zeros(9,9);
% shift = floor(9/2)+1;
% 
% % mono terms 
% Phi( 0+shift, 0+shift)  = complex(173/256,-7/32);
% Phi( 1+shift, 0+shift)  = complex(1/8,1/16);
% Phi(-1+shift, 0+shift)  = complex(1/8,1/16);
% Phi( 2+shift, 0+shift)  = -1/32;
% Phi(-2+shift, 0+shift)  = -1/32;
% Phi( 0+shift, 1+shift)  = complex(7/64,1/16);
% Phi( 0+shift,-1+shift)  = complex(7/64,1/16);
% Phi( 0+shift, 2+shift)  = -complex(7/128,1/64);
% Phi( 0+shift,-2+shift)  = -complex(7/128,1/64);
% Phi( 0+shift, 3+shift)  = 1/64;
% Phi( 0+shift,-3+shift)  = 1/64;
% Phi( 0+shift, 4+shift)  = -1/512;
% Phi( 0+shift,-4+shift)  = -1/512;



% %%%%% EXAMPLE 2 in PAPER %%%%%%%%%%%
% Phi = zeros(9,9);
% shift = floor(9/2)+1;
% 
% % mono terms 
% Phi( 0+shift, 0+shift)  = (301/384-7i/48);
% Phi(-1+shift,-0+shift)  = (7/96+1i/24);
% Phi( 1+shift, 0+shift)  = (3/32+1i/24);
% Phi( 2+shift, 0+shift)  = -1/48;
% Phi(-2+shift,-0+shift)  = -1/48;
% Phi( 0+shift, 1+shift)  = (7/96+1i/24);
% Phi(-0+shift,-1+shift)  = (7/96+1i/24);
% Phi( 0+shift, 2+shift)  = -(7/192+1i/96);
% Phi(-0+shift,-2+shift)  = -(7/192+1i/96);
% Phi( 0+shift, 3+shift)  = 1/96;
% Phi(-0+shift,-3+shift)  = 1/96;
% Phi( 0+shift, 4+shift)  = -1/768;
% Phi(-0+shift,-4+shift)  = -1/768;
% 
% % cross terms
% Phi(-1+shift,-1+shift)  =  1/192;
% Phi(-1+shift, 1+shift)  =  1/192;
% Phi( 1+shift, 1+shift)  = -1/192;
% Phi( 1+shift,-1+shift)  = -1/192;

% % EXAMPLE 3 in the paper
% Phi = zeros(17,17);
% shift = floor(17/2)+1;
% % E = diag(1/2,1/8)
% % mono terms
% Phi( 0+shift, 0+shift)  = complex(26527/32768,-43/192);
% Phi( -1+shift,0+shift)  = complex(253/3072,1/48);
% Phi( 1+shift, 0+shift)  = complex(259/3072,1/48);
% Phi( 2+shift,shift)  = -1/48;
% Phi( -2+shift,shift)  = -1/48;
% Phi( shift, -1 + shift)  = complex(715/12288,7/48);
% Phi( shift, +1 + shift)  = complex(715/12288,7/48);
% Phi(shift, -2+shift)  = -complex(1001/24576,7/96);
% Phi(shift,  2+shift)  = -complex(1001/24576,7/96);
% Phi( 0+shift, -3+shift)  = complex(91/4096,1/48);
% Phi( 0+shift, 3+shift)  = complex(91/4096,1/48);
% Phi( shift,  4+shift)  = -complex(455/49152,1/384);
% Phi( shift, -4+shift)  = -complex(455/49152,1/384);
% Phi( 0+shift, 5+shift)  = 35/12288;
% Phi(-0+shift, -5+shift)  = 35/12288;
% Phi( 0+shift, 6+shift)  = -5/8192;
% Phi(-0+shift, -6+shift)  = -5/8192;
% Phi( 0+shift, 7+shift)  = 1/12288;
% Phi(-0+shift, -7+shift)  = 1/12288;
% Phi( 0+shift, 8+shift)  = -1/196608;
% Phi(-0+shift, -8+shift)  = -1/196608;
% 
% % cross terms
% Phi(-1 +shift, -2+shift)  = 1/1536;
% Phi( 1 +shift, -2+shift)  = -1/1536;
% Phi(-1 +shift, +2+shift)  = 1/1536;
% Phi( 1 +shift, +2+shift)  = -1/1536;
% Phi(-1 +shift, -4+shift)  = -1/6144;
% Phi( 1 +shift, -4+shift)  = 1/6144;
% Phi(-1 +shift, +4+shift)  = -1/6144;
% Phi( 1 +shift, +4+shift)  = 1/6144;




% % NEW EXAMPLE! in the paper
% Phi = zeros(21,21);
% shift = floor(21/2)+1;
% % interesting example where \Omega = {(0,0), (pi,pi)} (see paper)
% Phi(  0+shift, 0+shift)  = 346751/524288 - 341i/1024;
% Phi( -1+shift, 0+shift)  = 15/128 + 15i/128;
% Phi(  1+shift, 0+shift)  = 15/128 + 15i/128;
% Phi( -2+shift, 0+shift)  = -53361/1048576 - 19i/256;
% Phi(  2+shift, 0+shift)  = -53361/1048576 - 19i/256;
% Phi( -3+shift, 0+shift)  = 1/128 + 1i/128;
% Phi(  3+shift, 0+shift)  = 1/128 + 1i/128;
% Phi( -4+shift, 0+shift)  = 495/262144 + 7i/512;
% Phi(  4+shift, 0+shift)  = 495/262144 + 7i/512;
% Phi( -6+shift, 0+shift)  = -1045/2097152 - 1i/256;
% Phi(  6+shift, 0+shift)  = -1045/2097152 - 1i/256;
% Phi( -8+shift, 0+shift)  = 69/1048576 + 1i/2048;
% Phi(  8+shift, 0+shift)  = 69/1048576 + 1i/2048;
% Phi(-10+shift, 0+shift)  = -9/2097152;
% Phi( 10+shift, 0+shift)  = -9/2097152;
% Phi(  0+shift, 1+shift)  = 1/8 + 1i/8;
% Phi(  0+shift,-1+shift)  = 1/8 + 1i/8;
% Phi(  0+shift, 2+shift)  = -1/32 - 15i/512;
% Phi(  0+shift,-2+shift)  = -1/32 - 15i/512;
% Phi(  0+shift, 4+shift)  = 3i/256;
% Phi(  0+shift,-4+shift)  = 3i/256;
% Phi(  0+shift, 6+shift)  = -1i/512;
% Phi(  0+shift,-6+shift)  = -1i/512;

conv_power = Phi;

k=0;
while k < n_times
    k = k + 1;
    conv_power = conv2(Phi, conv_power, 'full');
    dim_f = size(conv_power);
    
    if dim_f(1) > support_bound || dim_f(2) > support_bound
        conv_power = cropND(conv_power, support_bound);

    end
end
end

% ------ crop ND ---------

function img = cropND(img, sup_bd)

size_img = size(img);
if sup_bd < size_img(1) && sup_bd < size_img(2)
    img = img( floor(size_img(1)/2)-floor(sup_bd/2)+1: 1 :floor(size_img(1)/2)+floor(sup_bd/2),...
        floor(size_img(2)/2)-floor(sup_bd/2)+1: 1 :floor(size_img(1)/2)+floor(sup_bd/2));
end
end
    
    

        
    
    


