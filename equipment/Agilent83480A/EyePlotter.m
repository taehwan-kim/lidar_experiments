
eyeObject = commscope.eyediagram();
reset(eyeObject);
eyeObject.SamplingFrequency = 1/1E-10;
eyeObject.SamplesPerSymbol = 200;
eyeObject.SymbolsPerTrace = 2;
eyeObject.MaximumAmplitude = 1;
eyeObject.MinimumAmplitude = 0;
eyeObject.PlotType = '2D Color';
eyeObject.AmplitudeResolution = 0.005;
eyeObject.ColorScale = 'log';
data_size = size(eye);
traces = data_size(2);
eyeObject.NumberOfStoredTraces = traces;
for index=2:traces
    update(eyeObject,1000*eye(:,index));
end
plot(eyeObject);
%analyze(eyeObject);
%properties = eyeObject.Measurements