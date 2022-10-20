%%% Author: Huan Q. Bui
%%% Colby College '21
%%% Date: Aug 07, 2020


% if max(size(gcp)) == 0 % parallel pool needed
%    parpool('local',2); % create the parallel pool
% end

clear all 
close all

%%%%%%%%%%%%%%%%%%%
% clock starts
tic 
% clock starts
%%%%%%%%%%%%%%%%%%%

% bound = 75;
bound = 100;

X = -bound:1:bound;
Y = -bound:1:bound;

% integrate over [-bd,bd]x[-bd,bd]
bd  = 6;
% bd = 13;
% define \tau for renormalized integral
tau = 360;
% tau = 281;
% dilation factor
t = 200;
%dimension
d=2;
% trace of E
%muE = 1/2+1/4;
E11 = 1/6;
E22 = 1/2;
muE = E11 + E22;

[II,JJ] = meshgrid(X,Y);
H1 = gpuArray(zeros(length(II),length(JJ)));
H2 = gpuArray(zeros(length(II),length(JJ)));
R = length(II);
C = length(JJ);


% parfor always goes on the outer loop
parfor r = 1:R
   for c = 1:C
        H1(r,c) =  Hxy1(II(1,r), JJ(c,1), bd, tau ,t , d, muE );
        % H2(r,c) = iHxy2(II(1,r), JJ(c,1), bd, tau ,t , d, muE );
        disp(['Calculated: ' num2str((r-1)*C + c) ' out of ' num2str(R*C)]);
        
        [msg, id] = lastwarn;
        warning('off', id)
   end
end



%%%%%%%%%%%%%%% plot original H %%%%%%%%%%%%%%%


% just in case we need to extract data from figure
% fig = gcf;
% axObjs=fig.Children;
% dataObjs=axObjs.Children;


figure(1)
h1 = surf(II,JJ,H1);
set(h1, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.25 , 'FaceAlpha',1);
xlabel('x', 'FontSize',14);
ylabel('y', 'FontSize',14);
%axis([-60 60 -60 60 -0.007 0.014])
%axis([-30 30 -30 30 -0.015 0.03])
axis([-75 75 -75 75 -0.014 0.016])
%axis([-75 75 -75 75 -0.007 0.007])
%view(25,15)
view(50,20)

% figure(2)
% h2 = surf(II,JJ,H2);
% set(h2, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.25 , 'FaceAlpha',1);
% xlabel('x', 'FontSize',14);
% ylabel('y', 'FontSize',14);
% %axis([-60 60 -60 60 -0.007 0.014])
% % axis([-30 30 -30 30 -0.015 0.03])
% % view(25,15)
% axis([-100 100 -100 100 -0.014 0.016])
% view(50,20)
% 
% 
% figure(3)
% H3 = H1+H2;
% h3 = surf(II,JJ,H3);
% set(h3, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.25 , 'FaceAlpha',1);
% xlabel('x', 'FontSize',14);
% ylabel('y', 'FontSize',14);
% %axis([-60 60 -60 60 -0.007 0.014])
% %axis([-30 30 -30 30 -0.015 0.03])
% %view(25,15)
% axis([-100 100 -100 100 -0.014 0.016])
% view(50,20)


% %%%%%%%%%%%%%%%% H2 %%%%%%%%%%%%%%%%%%%%
% 
% % convert Ht to Hm where m is something else
% m = 2000;
% H2000 = (t/m)^muE.*H;
% newX = (m/t)^E11.*X;
% newY = (m/t)^E22.*Y;
% [newII,newJJ] = meshgrid(newX,newY);
% figure(2)
% h2 = surf(newII,newJJ,H2000);
% set(h2, 'LineWidth',0.1,'edgecolor','black', 'EdgeAlpha', 0.15 , 'FaceAlpha',1);
% xlabel('x', 'FontSize',14);
% ylabel('y', 'FontSize',14);
% 
% axis([-70 70 -70 70 -0.01 0.01])
% view(44,12)


%%%%%%%%%%%%%%%%%%%
% clock ends
Duration = seconds(round(toc));
Duration.Format = 'hh:mm:ss';
disp(['Time taken : ' char(Duration)]);
disp(['Time in sec: ' num2str(toc)]);
disp(' ');
% clock ends
%%%%%%%%%%%%%%%%%%%

% save workspace
save('dec_17_2021_Ex7_1.mat')




% -- Integration --

function Hxy1 = Hxy1(II,JJ, bd, tau ,t , d, muE )

% note: the following definitions of "fun" are equivalent under change of vars
% we're only interested in the real part, so just do Cos() for this example
% since we only have iQ, ie things in the exp is purely imaginary
%fun = @(x,y) cos( (-II.*x.*(t^(-1/2)) - JJ.*y.*(t^(-1/4))) - x.^2/24 + x.*y.^2./96 - y.^4/96);

% renormalized integral approach
%fun = @(x,y) (abs(x.^2/24 - x.*y.^2./96 + y.^4/96) < tau).*...%
%        cos( II.*x.*t^(-1/2) + JJ.*y.*t^(-1/4) + x.^2/24 - x.*y.^2./96 + y.^4/96); %...
%        + 1i*sin( (-II.*x.*(t^(-1/2)) - JJ.*y.*(t^(-1/4))) - x.^2/24 + x.*y.^2./96 - y.^4/96);

%fun = @(x,y) (abs(x.^4/32 + y.^4/32) < tau).*...%
%   cos( (-II.*x.*(t^(-1/4)) - JJ.*y.*(t^(-1/4))) - x.^4/32 - y.^4/32); %...

fun = @(x,y) (abs(x.^6/128 + y.^2/8) < tau).*...%
   cos( (-II.*x.*(t^(-1/6)) - JJ.*y.*(t^(-1/2))) - x.^6/128 - y.^2/8); %...

% no need to call real() here 
%  'method', 'iterated' for better output quality
Hxy1 = (t^(-muE)/(2*pi)^d)*integral2(fun,-bd,bd,-bd,bd, 'AbsTol',1e-5, 'RelTol',1e-5);

end


function iHxy2 = iHxy2(II,JJ, bd, tau ,t , d, muE )
% renormalized integral approach
fun = @(x,y) (abs((1/2+3i/8).*(x.^4 + y.^4)) < tau).*(cos(II.*x.*t^(-1/4) + JJ.*y.*t^(-1/4)+(3/8).*(x.^4+y.^4)).*exp(-(1/2).*(x.^4+y.^4))...
            -sin(II.*x.*t^(-1/4) + JJ.*y.*t^(-1/4)+(3/8).*(x.^4+y.^4)).*exp(-(1/2).*(x.^4+y.^4)));
iHxy2 = (t^(-muE)/(2*pi)^d)*real((1i^(t+2.*(II+JJ)))*integral2(fun,-bd,bd,-bd,bd, 'AbsTol',1e-5, 'RelTol',1e-5));

end


