% Author: Huan Q. Bui
% Colby College '21
% Date: Aug 07, 2020



clear all
close all

%%%%%%%%%%%%%%%%%%%
% clock starts
tic 
% clock starts
%%%%%%%%%%%%%%%%%%%


% %%%%%% max |\phi^(n) (x)| vs. n  %%%%%%%
%  
% support_bound = 700;
% n = 0:10:500;
% sup = [];
% %scaled_sup = [];
% % muP = 1/2+1/4;
% %muP = 1/2 + 1/8;
% muP = 1/2 + 1/2;
% %muP = 1/2 + 1/6;
% % muP = 1/4 + 1/4;
% for n_times = n
%     M = max(abs(fast_convolve(n_times, support_bound)) , [], 'all'); % find max;
%     sup = [sup M]; % concatenate
%     %scaled_sup = [scaled_sup (n_times^muP)*M]; % concatenate
%     disp(['Progress: ' num2str(n_times)]);
% end
% % figure for SUP
% figure(1)
% p1 = plot(n,sup, '-o', 'color','blue', 'LineWidth', 1)
% %plot(log(n),log(sup), '-o', 'color','blue', 'LineWidth', 1) % plot log instead
% %xlim([0 max(n)])
% %ylim([-0.01 0.7])
% %xlabel('log(n)', 'FontSize',16);
% xlabel('n', 'FontSize',16);
% ylabel('', 'FontSize', 16 );
% % figure for SCALED_SUP
% hold on 
% n1 = n+1;
% nY = n1.^(-muP);
% C=1;
% p2 = plot(n1, C.*nY, 'LineWidth', 2, 'Color', 'red')
% %plot(log(n), log(nY), 'LineWidth', 2)  % plot log instead
% hold off
% legend('f(n)','n^{-1}', 'FontSize',14);
% %legend('f(n) = log(max_{K}|\phi^{(n)}|)','log(n^{-\mu_\phi}) = log(n^{-3/4})', 'FontSize',14);
% 
% % figure(2)
% % plot(n,scaled_sup, '-o', 'color','blue', 'LineWidth', 1)
% % xlim([0 max(n)])
% % ylim([0 1.8])
% % xlabel('n', 'FontSize',16);
% % legend('n^{\mu_\phi} \cdot f(n) = n^{3/4}f(n)', 'FontSize',14)





%%%%%% PLOT THE CONVOLUTION POWER %%%%%%%

h = figure(1);
% h.Position = [100 100 1200 500];
n_times = 200;
support_bound = 400;

disp('Calculating...');
data = real(fast_convolve(n_times, support_bound));    % plot the real part
%data = imag(fast_convolve(n_times, support_bound));    % plot the img part
% data = abs(fast_convolve(n_times, support_bound));      % plot the abs
dim = size(data);
x = floor(-dim(1)/2)+1:1:floor(dim(1)/2);
y = floor(-dim(2)/2)+1:1:floor(dim(2)/2);
[X, Y] = meshgrid(x, y);
s = surf(X, Y, data, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.25 , 'FaceAlpha',1);
xlabel('x', 'FontSize',14);
ylabel('y', 'FontSize',14);
% title(['Re(\phi^{(', num2str(n_times), ')})'], 'FontSize', 16 );
% title(['|\phi^{(', num2str(n_times), ')}|'], 'FontSize', 16 );
% colorbar;
% s = meshc(X, Y, data);
%xlim([-floor(dim(1)/2)  floor(dim(2)/2)]);
%ylim([-floor(dim(1)/2)  floor(dim(2)/2)]);

% xlim([-floor(dim(1)/4)  floor(dim(2)/4)]);
% ylim([-floor(dim(1)/4)  floor(dim(2)/4)]);

% Evan's configs
%axis([-floor(dim(1)/2) floor(dim(2)/2) -floor(dim(1)/2) floor(dim(2)/2) -0.012 0.016])
%axis([-50 50 -50 50 -0.007 0.014])
%view(40,40)

axis([-50 50 -50 50 -0.014 0.016])
view(50,20)


%xlabel('x','fontsize',38)                                                      
%ylabel('y','fontsize',38)                                                      
%set(gca,'fontsize',38)
%set(gcf,'papersize',[20,12])
%set(gcf,'paperposition',[0,0,20,12])

box off



% %%%% generate evolution %%%%%
% 
% 
% %filename = 'C:\Users\buiqu\Documents\GitHub\huanium\LaTeX projects\CLAS 2021 Math\Ex10_minmax.gif';
% filename = 'test.gif';
% 
% data = real(fast_convolve(1, support_bound));    % plot the real part
% dim = size(data);
% x = floor(-dim(1)/2)+1:1:floor(dim(1)/2);
% y = floor(-dim(2)/2)+1:1:floor(dim(2)/2);
% [X, Y] = meshgrid(x, y);
% 
% 
% subplot(1,2,1)
% surf(X, Y, data, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0, 'FaceAlpha',1);
% %mesh(X,Y,data, 'LineWidth',1,'edgecolor','black', 'EdgeAlpha', 0.5 , 'FaceAlpha',1);
% view([+30 20])
% %view([+140 30]) %gaussian
% xlabel('X', 'FontSize',16);
% ylabel('Y', 'FontSize',16);
% % title(['Re(\phi^{(', num2str(n_times), ')})'], 'FontSize', 16 );
% title(['Re(\phi^{(', num2str(i-1), ')})'], 'FontSize', 16 );
% %title(['\phi^{(', num2str(i-1), ')}'], 'FontSize', 16 );
% % colorbar;
% % s = meshc(X, Y, data);
% xlim([-floor(dim(1)/2)  floor(dim(2)/2)]);
% ylim([-floor(dim(1)/2)  floor(dim(2)/2)]);
% % zlim([0 0.004]);
% zlim([min(data(:)) max(data(:))]);
% 
% subplot(1,2,2)
% surf(X, Y, data, 'LineWidth',0.25,'edgecolor','black', 'EdgeAlpha', 0.1 , 'FaceAlpha',1);
% %mesh(X,Y,data, 'LineWidth',1,'edgecolor','black', 'EdgeAlpha', 0.5 , 'FaceAlpha',1);
% view([+0 90])
% xlabel('X', 'FontSize',16);
% ylabel('Y', 'FontSize',16);
% title(['Re(\phi^{(', num2str(n_times), ')})'], 'FontSize', 16 );
% %title(['Re(\phi^{(', num2str(i-1), ')})'], 'FontSize', 16 );
% title(['\phi^{(', num2str(i-1), ')}'], 'FontSize', 16 );
% % colorbar;
% % s = meshc(X, Y, data);
% xlim([-floor(dim(1)/2)  floor(dim(2)/2)]);
% ylim([-floor(dim(1)/2)  floor(dim(2)/2)]);
% drawnow
% 
% 
% 
% for i=1:5:n_times
%     data = real(fast_convolve(i, support_bound));    % plot the real part
%     dim = size(data);
%     x = floor(-dim(1)/2)+1:1:floor(dim(1)/2);
%     y = floor(-dim(2)/2)+1:1:floor(dim(2)/2);
%     [X, Y] = meshgrid(x, y);
%     subplot(1,2,1)
%     surf(X, Y, data, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.0 , 'FaceAlpha',1);
%     view([+30 20])
%     %view([+140 30]) %gaussian
%     xlabel('X', 'FontSize',16);
%     ylabel('Y', 'FontSize',16);
%     title(['Re(\phi^{(', num2str(i-1), ')})'], 'FontSize', 16 );
%     %title(['\phi^{(', num2str(i-1), ')}'], 'FontSize', 16 );
%     % colorbar;
%     % s = meshc(X, Y, data);
%     xlim([-floor(dim(1)/2)  floor(dim(2)/2)]);
%     ylim([-floor(dim(1)/2)  floor(dim(2)/2)]);
%     zlim([min(data(:)) max(data(:))]);
% 
% 
% 
%     subplot(1,2,2)
%     surf(X, Y, data, 'LineWidth',0.25,'edgecolor','black', 'EdgeAlpha', 0.1 , 'FaceAlpha',1);
%     view([+0 90])
%     %view(2)
%     xlabel('X', 'FontSize',16);
%     ylabel('Y', 'FontSize',16);
%     % title(['Re(\phi^{(', num2str(n_times), ')})'], 'FontSize', 16 );
%     %title(['|\phi^{(', num2str(i-1), ')}|'], 'FontSize', 16 );
%     title(['Re(\phi^{(', num2str(i-1), ')})'], 'FontSize', 16 );
%     %title(['\phi^{(', num2str(i-1), ')}'], 'FontSize', 16 );
%     % colorbar;
%     % s = meshc(X, Y, data);
%     xlim([-floor(dim(1)/2)  floor(dim(2)/2)]);
%     ylim([-floor(dim(1)/2)  floor(dim(2)/2)]);
%     drawnow
%     
%     
%     %sgtitle('Simple Random Walk in Z^2', 'FontSize', 16 ) 
%     
%     
%     % save as GIF
%     % Capture the plot as an image
%     frame = getframe(h);
%     im = frame2im(frame);
%     [imind,cm] = rgb2ind(im,256);
%     % Write to the GIF File
%     if i == 1
%         imwrite(imind,cm,filename,'gif', 'Loopcount',inf, 'DelayTime', 0.075);
%     else
%         imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime', 0.075);
%     end
%     
% end


%%%%%%%%%%%%%%%%%%%
% clock ends
Duration = seconds(round(toc));
Duration.Format = 'hh:mm:ss';
disp(['Time taken : ' char(Duration)]);
disp(['Time in sec: ' num2str(toc)]);
disp(' ');
% clock ends
%%%%%%%%%%%%%%%%%%%



%------- Fast Convolve ----------

function conv_power = fast_convolve(n_times, support_bound)



% %%% Dec 3 2021 
% %%% Example 4
% %%% E = diag(1/4,1/4)
% Phi = zeros(13,13);
% shift = floor(13/2)+1;
% Phi( 1+shift, 0+shift)  = complex(552,-540);
% Phi(-1+shift, 0+shift)  = complex(552,-540);
% Phi( 2+shift, 0+shift)  = -complex(177,-499/2);
% Phi(-2+shift, 0+shift)  = -complex(177,-499/2);
% Phi( 3+shift, 0+shift)  = complex(-28,+10);
% Phi(-3+shift, 0+shift)  = complex(-28,+10);
% Phi( 4+shift, 0+shift)  = complex(42,-59);
% Phi(-4+shift, 0+shift)  = complex(42,-59);
% Phi( 5+shift, 0+shift)  = complex(-12,18);
% Phi(-5+shift, 0+shift)  = complex(-12,18);
% Phi( 6+shift, 0+shift)  = complex(1,-3/2);
% Phi(-6+shift, 0+shift)  = complex(1,-3/2);
% 
% Phi( 0+shift, 0+shift)  = complex(2584,1292);
% Phi( 0+shift, 1+shift)  = complex(552,-540);
% Phi( 0+shift,-1+shift)  = complex(552,-540);
% Phi( 0+shift, 2+shift)  = -complex(177,-499/2);
% Phi(-0+shift,-2+shift)  = -complex(177,-499/2);
% Phi( 0+shift, 3+shift)  = complex(-28,+10);
% Phi(-0+shift,-3+shift)  = complex(-28,+10);
% Phi( 0+shift, 4+shift)  = complex(42,-59);
% Phi(-0+shift,-4+shift)  = complex(42,-59);
% Phi( 0+shift, 5+shift)  = complex(-12,18);
% Phi(-0+shift,-5+shift)  = complex(-12,18);
% Phi( 0+shift, 6+shift)  = complex(1,-3/2);
% Phi(-0+shift,-6+shift)  = complex(1,-3/2);
% 
% Phi = Phi/2^12;


% % 
% Phi = zeros(3,3);
% shift = floor(3/2)+1;
% Phi( 0+shift, 1+shift)  =  1/4;
% Phi( 0+shift,-1+shift)  = 1/4;
% Phi( 1+shift, 0+shift)  = 1/4;
% Phi(-1+shift, 0+shift)  = 1/4;



% simple Example with E = diag(1/4, 1/4).
% no cross terms
% 
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






% % EXAMPLE 0 in the paper
% Phi = zeros(5,5);
% shift = floor(5/2)+1;
% 
% Phi( 0+shift, 0+shift)  =  (1/192)*(144 - 64i);
% Phi( 1+shift, 0+shift)  = (1/192)*(16 + 16i);
% Phi(-1+shift, 0+shift)  = (1/192)*(16 + 16i);
% Phi( 2+shift, 0+shift)  = -4*(1/192) ;
% Phi(-2+shift, 0+shift)  = -4*(1/192)  ;    
% Phi( 0+shift, 1+shift)  = (1/192)*(16+16i);
% Phi( 0+shift,-1+shift)  = (1/192)*(16+16i);
% Phi( 0+shift, 2+shift)  = -4*(1/192);
% Phi( 0+shift,-2+shift)  = -4*(1/192);
% Phi( -1+shift, -1+shift)  = (1/192)*1i;  
% Phi( 1+shift, -1+shift)  = -(1/192)*1i;   
% Phi( -1+shift, 1+shift)  = -(1/192)*1i;  
% Phi( 1+shift, 1+shift)  = (1/192)*1i;  


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
% %%%%% Example Nov 29, 2021 %%%%%%%%%
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




% NEW EXAMPLE! Example 10, in the paper
Phi = zeros(21,21);
shift = floor(21/2)+1;
% interesting example where \Omega = {(0,0), (pi,pi)} (see paper)
Phi(  0+shift, 0+shift)  = 346751/524288 - 341i/1024;
Phi( -1+shift, 0+shift)  = 15/128 + 15i/128;
Phi(  1+shift, 0+shift)  = 15/128 + 15i/128;
Phi( -2+shift, 0+shift)  = -53361/1048576 - 19i/256;
Phi(  2+shift, 0+shift)  = -53361/1048576 - 19i/256;
Phi( -3+shift, 0+shift)  = 1/128 + 1i/128;
Phi(  3+shift, 0+shift)  = 1/128 + 1i/128;
Phi( -4+shift, 0+shift)  = 495/262144 + 7i/512;
Phi(  4+shift, 0+shift)  = 495/262144 + 7i/512;
Phi( -6+shift, 0+shift)  = -1045/2097152 - 1i/256;
Phi(  6+shift, 0+shift)  = -1045/2097152 - 1i/256;
Phi( -8+shift, 0+shift)  = 69/1048576 + 1i/2048;
Phi(  8+shift, 0+shift)  = 69/1048576 + 1i/2048;
Phi(-10+shift, 0+shift)  = -9/2097152;
Phi( 10+shift, 0+shift)  = -9/2097152;
Phi(  0+shift, 1+shift)  = 1/8 + 1i/8;
Phi(  0+shift,-1+shift)  = 1/8 + 1i/8;
Phi(  0+shift, 2+shift)  = -1/32 - 15i/512;
Phi(  0+shift,-2+shift)  = -1/32 - 15i/512;
Phi(  0+shift, 4+shift)  = 3i/256;
Phi(  0+shift,-4+shift)  = 3i/256;
Phi(  0+shift, 6+shift)  = -1i/512;
Phi(  0+shift,-6+shift)  = -1i/512;

conv_power = Phi;

k=0;
while k < n_times
    k = k + 1;
    conv_power = conv2(Phi, conv_power, 'full');
    dim_f = size(conv_power);
    
    if dim_f(1) > support_bound || dim_f(2) > support_bound
        conv_power = cropND(conv_power, support_bound);
    end
    
    disp(['Calculated ' num2str(k) ' out of ' num2str(n_times) ' times'])
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
    
    

        
    
    


