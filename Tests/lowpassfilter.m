%% Reading Data for 10 seconds
Fs = 44100; %known beforehand
samples = [1,20*Fs];
[data,Fs] = audioread('coke.mp3',samples);
downsampled = downsample(data,2);

%% Play sound
sound(downsampled,Fs/2)
%sound(data,Fs);
%data shows the recording is from 2 channel microphones i.e left and right

%extracting either left or right channel data

dataRight = downsampled(:,1);
dataLeft = data(:,2);

%% Again play from one channel
sound(dataRight,Fs);
%sounds the same, now let's analyze the frequency content of the signal

%% Plot the Audio data in time domain and analyze in frequency domain
%%Time specifications:
dt = 1/Fs;
t = 0:dt:(length(dataRight)*dt-dt);
figure(1)
plot(t,dataRight)
xlabel('Time')
ylabel('Normalized Amplitude')
title('Time domain data')

%Frequency Specifications

dataRightDFT = fft(dataRight);
dataRightDFT = dataRightDFT(1:length(dataRight)/2+1);
%create a frequency vector
freq = 0:Fs/length(dataRight):Fs/2;
figure(2)

subplot(211);
plot(freq,abs(dataRightDFT))
title('Frequency Response')
subplot(212);
plot(freq,unwrap(angle(dataRightDFT)));
xlabel('Hz')
axis tight

%The frequency visualization also doesn't give information we're looking
%for because trying to calculate the spectral components of the signal 
%will be pointless for stochastic signal because, for every realisation of 
%the random process you will have different expressions for 
%Discrete Fourier Transform

%% Power spectral density
%for that we look Power spectral density to analyze the power distributed
%over frequency components.

figure(3)
plot(psd(spectrum.periodogram,dataRight,'Fs',Fs/2,'NFFT',length(dataRight)));

%from psd it can be seen that below 4.6 kHz, more power is concentrated so,
%below nearly 4.6 kHz is required signal and above 4.6 kHz, the signal can be
%clipped

%% Implementing Filter
cutoff = 4000/Fs/2;   %in normalized -> Fc / (Fs/2) 
order = 20;
h = fir1(order,cutoff);
tic;
filteredSignal = conv(h,dataRight);
timeElapsed = toc;
figure(4)
%plot(filteredSignal)
%axis tight;
plot(psd(spectrum.periodogram,filteredSignal,'Fs',Fs,'NFFT',length(filteredSignal)));
sound(filteredSignal,Fs/2)
%we can see that in log scale the frequency component over 4700 hertz is
%rolled over and cutoff 

%% Saving audio files.
audiowrite('Without_filter.wav', dataRight,Fs);
audiowrite('With_Filter.wav',filteredSignal,Fs);