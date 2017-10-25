function plot_graph( handle, numofaxis, filename )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

    % change settings
    linecolors = linspecer(numofaxis,'qualitative');

    opt = [];

%     opt.BoxDim          = [6 4];
    opt.ShowBox         = 'on';
    opt.Colors          = [linecolors];
    opt.FontName        = 'Helvetica Neue';

% %     opt.Title           = 'Photocurrent PSD'; % title
    opt.XLabel          = 'Frequency (MHz)';   % xlabel
    opt.YLabel          = 'PSD (dB/Hz)'; % ylabel
    %opt.ZLabel            = % Z axis label

    opt.XMinorTick      = 'off';     % 'on' or 'off': show X minor tick?
    opt.YMinorTick      = 'off';     % 'on' or 'off': show Y minor tick?
    %opt.ZMinorTick     = % 'on' or 'off': show Z minor tick?
    
    opt.FileName        = filename;    % Save? comment the following line if you do not want to save
%     opt.Legend          = {'1', '2','3'};% {'legend1','legend2',...}

    %opt.FontSize        = % integer; default: 26
    %opt.LineWidth       = % vector [width1, width2, ..]: element i changes the property of i-th dataset; default: 2
    %opt.LineStyle       = % cell array {'style1', 'style2', ..}: element i changes the property of i-th dataset; default: '-'
%     opt.Markers         = {'None','None','none','*','*','*'}; % cell array {'marker1', 'marker2', ..}: element i changes the property of i-th dataset; default: 'None'
%     opt.MarkerSpacing   = [50 50];% vector [space1, space2, ..]: element i changes the property of i-th dataset; default: 0
    %opt.Colors          = % 3xN matrix, [red, green, blue] where N is the number of datasets.
    %opt.AxisColor       = % [red, green, blue]; color of the axis lines; default: black
    %opt.AxisLineWidth   = % Witdth of the axis lines; default: 2
    %opt.XTick           = % [tick1, tick2, ..]: major ticks for X axis.
    %opt.YTick           = % [tick1, tick2, ..]: major ticks for Y axis.
    %opt.ZTick           = % [tick1, tick2, ..]: major ticks for Z axis.
    %opt.TickDir         = % tick direction: 'in' or 'out'; default: 'in'
    %opt.TickLength      = % tick length; default: [0.02, 0.02]
%     opt.XLim            = [-25,25];% [min, max]: X axis limit.
    %opt.YLim            = % [min, max]: Y axis limit.
    %opt.ZLim            = % [min, max]: Z axis limit.
%     opt.XScale          = 'log';% 'linear' or 'log': X axis scale.
    %opt.YScale          = % 'linear' or 'log': Y axis scale.
    %opt.ZScale          = % 'linear' or 'log': Z axis scale.
    %opt.XGrid           = % 'on' or 'off': show grid in X axis?
    %opt.YGrid           = % 'on' or 'off': show grid in Y axis?
    %opt.ZGrid           = % 'on' or 'off': show grid in Z axis?
    %opt.XDir            = % 'in' or 'out': X axis tick direction
    %opt.YDir            = % 'in' or 'out': Y axis tick direction
    %opt.ZDir            = % 'in' or 'out': Z axis tick direction
    %opt.LegendBox       = % bounding box of legend: 'on'/'off'; default: 'off'
    %opt.LegendBoxColor  = % color of the bounding box of legend; default: 'none'
    %opt.LegendTextColor = % color of the legend text; default: [0,0,0]
    %opt.LegendLoc       = % 'NorthEast', ..., 'SouthWest': legend location
    %opt.Resolution      = % Resolution (dpi) for bitmapped file. Default:600.
    %opt.HoldLines       = % true/false. true == only modify axes settings, do not touch plot lines/surfaces. Default false.

    % apply the settings
    setPlotProp(opt, handle);

    fig = gcf;
    fig.PaperPositionMode = 'auto';
    fig_pos = fig.PaperPosition;
    fig.PaperSize = [fig_pos(3) fig_pos(4)];
    print(fig,opt.FileName,'-dpdf');

end

