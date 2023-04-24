function ParamUI(ParameterTable, UsrFunc)
% ParamUI(ParameterTable, UsrFunc)
% - Process: create UI based on ParameterTable, assign UI values to Prm structure, call user function
% - Input: ParameterTable, UsrFunc 
%   - ParameterTable: A table containing the following columns: PrameterVariable, ParameterLabel, InitialValue, Min, Max, Step
%     -Example: {'A', 'Parameter A', 0.5, 0, 1, 0.1;'F1', 'Flag 1', true,[],[],[];'S1', 'Select 1', 'Two',[],[],{'One','Two','Three'}}
%     - Prm structure definition Prm.(ParameterVariable) Example: Prm.A=12, Prm.F1=false Prm.S1='Two' Member is ParameterVariable only, Prm structure is global variable
%   - UsrFunc: Function handle Example: userFunction = @(Prm) disp(Prm)
%
    global Prm;
    Prm =struct();
    UIWidth = 380;
    PanelHeight = 300;
    ySpace = 40;
    UIHeight = numel(ParameterTable(:, 1)) * ySpace + ySpace*3;
    mainFig = uifigure('Name','ParamUI');
    mainFig.Position = [100, 100, UIWidth, PanelHeight];
    UIPanel = uipanel(mainFig, 'Position', [0, 0, UIWidth, PanelHeight], 'Scrollable', 'on');
    
    for i = 1:size(ParameterTable, 1)
        paramVar = ParameterTable{i, 1};
        paramLabel = ParameterTable{i, 2};
        initialValue = ParameterTable{i, 3};
        minVal = ParameterTable{i, 4};
        maxVal = ParameterTable{i, 5};
        stepVal = ParameterTable{i, 6};
        
        Prm.(paramVar) = initialValue;
        
        if isnumeric(initialValue)
            slider = uislider(UIPanel, 'Position', [140, UIHeight - i * ySpace, 100, 3], ...
                'Limits', [minVal, maxVal], 'Value', initialValue, 'MajorTicks', [], 'MinorTicks', [], ...
                'ValueChangedFcn', @(src, ~) UIUpdate(src, paramVar, stepVal));
            uilabel(UIPanel, 'Position', [20, UIHeight - i * ySpace - 10, 100, 20], 'Text', paramLabel);
            uilabel(UIPanel, 'Position', [260, UIHeight - i * ySpace - 10, 100, 20], 'Text', num2str(initialValue), 'Tag', [paramVar '_ValueLabel']);
            
        elseif islogical(initialValue)
            checkbox = uicheckbox(UIPanel, 'Position', [20, UIHeight - i * ySpace - 10, 100, 20], 'Text', paramLabel, ...
                'Value', initialValue, 'ValueChangedFcn', @(src, ~) UIUpdate(src, paramVar));
            
        elseif iscell(stepVal)
            dropdown = uidropdown(UIPanel, 'Position', [130, UIHeight - i * ySpace - 10, 100, 20], 'Items', stepVal, ...
                'Value', initialValue, 'ValueChangedFcn', @(src, ~) UIUpdate(src, paramVar));
            uilabel(UIPanel, 'Position', [20, UIHeight - i * ySpace - 10, 100, 20], 'Text', paramLabel);
        end
        UIPanel.Scrollable = 'on';
    end
    UsrFunc(Prm);
    
    function UIUpdate(src, paramVar, stepVal)
        if isa(src, 'matlab.ui.control.Slider')
            src.Value = round(src.Value / stepVal) * stepVal;
            Prm.(paramVar) = src.Value;
            valueLabel = findobj(UIPanel, 'Tag', [paramVar '_ValueLabel']);
            valueLabel.Text = num2str(src.Value);
            
        elseif isa(src, 'matlab.ui.control.CheckBox')
            Prm.(paramVar) = src.Value;
            
        elseif isa(src, 'matlab.ui.control.DropDown')
            Prm.(paramVar) = src.Value;
        end
        
        UsrFunc(Prm);
    end
end
