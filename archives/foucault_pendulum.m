%%% SIMPLE PENDULUM IN ROTATING & INERTIAL FRAME

% constants
N = 4000 ;
t = linspace(0,100*pi,N);
w0 = 1;
Omega = w0*0.1;
% CW = 1/2;   % unit length
% CCW = 1/2;  % unit length

CW  = (w0 + Omega)/(2*w0);   % terrestrial start
CCW = (w0 - Omega)/(2*w0);   % terrestrial start 

% solution
x = CW*cos((w0-Omega)*t) + CCW*cos((w0+Omega)*t);
y = CW*sin((w0-Omega)*t) - CCW*sin((w0+Omega)*t);
plot(x,y, 'Color','k')
xlabel('X')
ylabel('Y')
drawnow;