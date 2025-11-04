%% LAB Color Threshold Finder for WRO 2025 Future Engineers
% Date: 11 October 2025
% Created by: Atakan ERSOY
% Team: ANTi - Representing Turkey
% MATLAB application for automatic LAB color threshold detection with
% custom LAB colorspace conversion
% Required dependencies: 
%   - Image Processing Toolbox

classdef ANTi_LabThresholdFinder < handle
    properties
        % Main UI components
        fig
        orig_axes
        thresh_axes
        
        % Data storage
        image_paths
        images
        lab_images
        current_index
        original_img
        lab_img
        image_scale
        
        % Color management
        color_names = {'red', 'green', 'magenta', 'blue', 'orange', 'black'}
        color_rgb = [1 0 0; 0 1 0; 1 0 1; 0 0 1; 1 0.5 0; 0 0 0]
        
        % Threshold values
        thresholds
        active_color
        
        % UI controls
        sliders
        color_buttons

        % UI text helpers
        image_info
        threshold_display
        stats_display
        
        % ROI selection stored per each color
        roi_rect
        roi_active
        roi_handles
    end
    
    methods
        function obj = ANTi_LabThresholdFinder()
            %% Initialize LAB Threshold Finder Application
            obj.create_ui();
            obj.initialize_data();
        end
        
        function create_ui(obj)
            %% Create Main User Interface with Auto-Centering
            % Get screen size for centering
            screen_size = get(groot, 'ScreenSize');
            screen_width = screen_size(3);
            screen_height = screen_size(4);
            
            % Calculate window size and position for centering
            window_width = 1600;
            window_height = 1000;
            x_pos = (screen_width - window_width) / 2;
            y_pos = (screen_height - window_height) / 2;
            
            obj.fig = uifigure('Name', 'LAB Color Threshold Finder - WRO Future Engineers', ...
                'Position', [x_pos, y_pos, window_width, window_height]);
            
            % Create main layout with more space for right side control panel
            grid = uigridlayout(obj.fig, [2, 3]);
            grid.RowHeight = {'1x', '1x'};
            grid.ColumnWidth = {'1x', '1x', 500};
            
            % Original image display
            obj.orig_axes = uiaxes(grid);
            obj.orig_axes.Layout.Row = 1;
            obj.orig_axes.Layout.Column = [1, 2];
            title(obj.orig_axes, 'Original Image');
            
            % Threshold image display
            obj.thresh_axes = uiaxes(grid);
            obj.thresh_axes.Layout.Row = 2;
            obj.thresh_axes.Layout.Column = [1, 2];
            title(obj.thresh_axes, 'Threshold Result');
            
            % Control panel
            control_panel = uipanel(grid, 'Scrollable', 'on');
            control_panel.Layout.Row = [1, 2];
            control_panel.Layout.Column = 3;
            
            obj.create_control_panel(control_panel);
        end
        
        function create_control_panel(obj, parent)
            %% Create Control Panel Layout with All Controls
            main_grid = uigridlayout(parent, [25, 3]);
            rh = repmat({35}, 1, 25);  % Default all rows to 35px height
            % Last 17–20 rows (Statistics display) 15px
            rh{17} = 15;
            rh{18} = 15;
            rh{19} = 15;
            rh{20} = 15;
            % Last 22–25 rows (Instructions display) 10px
            rh{22} = 10;
            rh{23} = 10;
            rh{24} = 10;
            rh{25} = 10;
            main_grid.RowHeight = rh;
            main_grid.ColumnWidth = [100, 120, 250]; % column widths
            
            % File operations - Row 1-2
            browse_btn = uibutton(main_grid, 'Text', 'Browse Images');
            browse_btn.Layout.Row = 1;
            browse_btn.Layout.Column = [1, 3];
            browse_btn.ButtonPushedFcn = @(btn,event) obj.load_images();
            
            % Navigation buttons - Row 2
            prev_btn = uibutton(main_grid, 'Text', 'Previous');
            prev_btn.Layout.Row = 2;
            prev_btn.Layout.Column = 1;
            prev_btn.ButtonPushedFcn = @(btn,event) obj.prev_image();
            
            next_btn = uibutton(main_grid, 'Text', 'Next');
            next_btn.Layout.Row = 2;
            next_btn.Layout.Column = 2;
            next_btn.ButtonPushedFcn = @(btn,event) obj.next_image();
            
            % Image info - Row 3
            info_label = uilabel(main_grid, 'Text', 'Image:');
            info_label.Layout.Row = 3;
            info_label.Layout.Column = 1;
            
            obj.image_info = uilabel(main_grid, 'Text', 'No images loaded');
            obj.image_info.Layout.Row = 3;
            obj.image_info.Layout.Column = [2, 3];
            
            % Color selection - Row 4
            color_label = uilabel(main_grid, 'Text', 'Active Color:');
            color_label.Layout.Row = 4;
            color_label.Layout.Column = 1;
            
            % Create a grid for color buttons
            color_grid = uigridlayout(main_grid, [1, 6]);
            color_grid.Layout.Row = 4;
            color_grid.Layout.Column = [2, 3];
            color_grid.RowHeight = {25};
            
            obj.color_buttons = gobjects(1, 6);
            for i = 1:6
                % Determine text color for better contrast
                if i == 6 % black color
                    text_color = [1, 1, 1]; % white text for black background
                else
                    text_color = [0, 0, 0]; % black text for colored backgrounds
                end
                
                obj.color_buttons(i) = uibutton(color_grid, ...
                    'Text', upper(obj.color_names{i}), ...
                    'BackgroundColor', obj.color_rgb(i, :), ...
                    'FontColor', text_color, ...
                    'FontWeight', 'bold', ...
                    'FontSize', 9); % Fit font size
                obj.color_buttons(i).Layout.Row = 1;
                obj.color_buttons(i).Layout.Column = i;
                obj.color_buttons(i).ButtonPushedFcn = @(btn,event) obj.set_active_color(i);
            end
            
            % ROI Selection Button - Row 5
            roi_btn = uibutton(main_grid, 'Text', 'Select ROI for Auto-Threshold');
            roi_btn.Layout.Row = 5;
            roi_btn.Layout.Column = [1, 3];
            roi_btn.ButtonPushedFcn = @(btn,event) obj.select_roi();
            roi_btn.BackgroundColor = [0.8, 0.8, 1]; % Light blue
            
            % LAB threshold sliders with labels - Rows 6-11
            slider_props = {'FontSize', 11, 'HorizontalAlignment', 'right', 'FontWeight', 'bold'};
            
            % L MIN - Row 6
            lmin_label = uilabel(main_grid, 'Text', 'L Min:', slider_props{:});
            lmin_label.Layout.Row = 6;
            lmin_label.Layout.Column = 1;
            
            obj.sliders.l_min = uislider(main_grid, 'Limits', [0, 100], 'Value', 0);
            obj.sliders.l_min.Layout.Row = 6;
            obj.sliders.l_min.Layout.Column = [2, 3];
            obj.sliders.l_min.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'l_min');
            
            % L MAX - Row 7
            lmax_label = uilabel(main_grid, 'Text', 'L Max:', slider_props{:});
            lmax_label.Layout.Row = 7;
            lmax_label.Layout.Column = 1;
            
            obj.sliders.l_max = uislider(main_grid, 'Limits', [0, 100], 'Value', 100);
            obj.sliders.l_max.Layout.Row = 7;
            obj.sliders.l_max.Layout.Column = [2, 3];
            obj.sliders.l_max.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'l_max');
            
            % A MIN - Row 8
            amin_label = uilabel(main_grid, 'Text', 'A Min:', slider_props{:});
            amin_label.Layout.Row = 8;
            amin_label.Layout.Column = 1;
            
            obj.sliders.a_min = uislider(main_grid, 'Limits', [-128, 127], 'Value', -128);
            obj.sliders.a_min.Layout.Row = 8;
            obj.sliders.a_min.Layout.Column = [2, 3];
            obj.sliders.a_min.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'a_min');
            
            % A MAX - Row 9
            amax_label = uilabel(main_grid, 'Text', 'A Max:', slider_props{:});
            amax_label.Layout.Row = 9;
            amax_label.Layout.Column = 1;
            
            obj.sliders.a_max = uislider(main_grid, 'Limits', [-128, 127], 'Value', 127);
            obj.sliders.a_max.Layout.Row = 9;
            obj.sliders.a_max.Layout.Column = [2, 3];
            obj.sliders.a_max.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'a_max');
            
            % B MIN - Row 10
            bmin_label = uilabel(main_grid, 'Text', 'B Min:', slider_props{:});
            bmin_label.Layout.Row = 10;
            bmin_label.Layout.Column = 1;
            
            obj.sliders.b_min = uislider(main_grid, 'Limits', [-128, 127], 'Value', -128);
            obj.sliders.b_min.Layout.Row = 10;
            obj.sliders.b_min.Layout.Column = [2, 3];
            obj.sliders.b_min.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'b_min');
            
            % B MAX - Row 11
            bmax_label = uilabel(main_grid, 'Text', 'B Max:', slider_props{:});
            bmax_label.Layout.Row = 11;
            bmax_label.Layout.Column = 1;
            
            obj.sliders.b_max = uislider(main_grid, 'Limits', [-128, 127], 'Value', 127);
            obj.sliders.b_max.Layout.Row = 11;
            obj.sliders.b_max.Layout.Column = [2, 3];
            obj.sliders.b_max.ValueChangingFcn = @(sld,event) obj.slider_changed(sld, event, 'b_max');
            
            % Action buttons - Rows 12-13
            auto_btn = uibutton(main_grid, 'Text', 'Auto Threshold (ROI/Full)');
            auto_btn.Layout.Row = 12;
            auto_btn.Layout.Column = [1, 2];
            auto_btn.ButtonPushedFcn = @(btn,event) obj.auto_threshold();
            auto_btn.Tooltip = 'Auto threshold on ROI if selected, otherwise full image';
            
            copy_btn = uibutton(main_grid, 'Text', 'Copy Thresholds');
            copy_btn.Layout.Row = 12;
            copy_btn.Layout.Column = 3;
            copy_btn.ButtonPushedFcn = @(btn,event) obj.copy_thresholds();
            
            reset_btn = uibutton(main_grid, 'Text', 'Reset Current Color');
            reset_btn.Layout.Row = 13;
            reset_btn.Layout.Column = [1, 2];
            reset_btn.ButtonPushedFcn = @(btn,event) obj.reset_thresholds();
            
            clear_roi_btn = uibutton(main_grid, 'Text', 'Clear ROI');
            clear_roi_btn.Layout.Row = 13;
            clear_roi_btn.Layout.Column = 3;
            clear_roi_btn.ButtonPushedFcn = @(btn,event) obj.clear_roi();
            
            % Threshold display - Row 14-15
            thresh_label = uilabel(main_grid, 'Text', 'Thresholds:');
            thresh_label.Layout.Row = 14;
            thresh_label.Layout.Column = 1;
            thresh_label.FontWeight = 'bold';
            thresh_label.FontSize = 11;
            
            obj.threshold_display = uitextarea(main_grid, ...
                'Value', {'L: (0, 100)', 'A: (-128, 127)', 'B: (-128, 127)'});
            obj.threshold_display.Layout.Row = [14, 15];
            obj.threshold_display.Layout.Column = [2, 3];
            obj.threshold_display.FontName = 'Courier New';
            obj.threshold_display.FontWeight = 'bold';
            obj.threshold_display.FontSize = 11;
            
            % Statistics display - Rows 16-20
            stats_label = uilabel(main_grid, 'Text', 'Statistics:');
            stats_label.Layout.Row = 16;
            stats_label.Layout.Column = 1;
            stats_label.FontWeight = 'bold';
            stats_label.FontSize = 11;
            
            obj.stats_display = uitextarea(main_grid, ...
                'Value', {'No image loaded'}, ...
                'Editable', false);
            obj.stats_display.Layout.Row = [17, 20];
            obj.stats_display.Layout.Column = [1, 3];
            obj.stats_display.FontName = 'Courier New';
            obj.stats_display.FontSize = 10;
            
            % Instructions - Rows 21-25
            instruct_label = uilabel(main_grid, 'Text', 'Instructions:');
            instruct_label.Layout.Row = 21;
            instruct_label.Layout.Column = 1;
            instruct_label.FontWeight = 'bold';
            instruct_label.FontSize = 11;
            
            instruct_text = uitextarea(main_grid, ...
                'Value', {
                '1. Click "Select ROI" and draw rectangle';
                '2. Use "Auto Threshold" for ROI or full image';
                '3. Adjust sliders for fine-tuning';
                '4. Copy thresholds for your code';
                '5. Switch colors to save different ROIs/thresholds'
                }, ...
                'Editable', false);
            instruct_text.Layout.Row = [22, 25];
            instruct_text.Layout.Column = [1, 3];
            instruct_text.FontSize = 10;
            instruct_text.BackgroundColor = [0.95, 0.95, 0.95];
        end
        
        function initialize_data(obj)
            %% Initialize Data Structures
            obj.image_paths = {};
            obj.images = {};
            obj.lab_images = {};
            obj.current_index = 1;
            obj.active_color = 1;
            
            % Initialize ROI data for all colors
            obj.roi_active = false(1, 6);
            obj.roi_rect = cell(1, 6);
            obj.roi_handles = cell(1, 6);
            
            % Initialize thresholds for all colors
            obj.thresholds = repmat(struct(...
                'l_min', 0, 'l_max', 100, ...
                'a_min', -128, 'a_max', 127, ...
                'b_min', -128, 'b_max', 127), 1, 6);
        end
        
        function load_images(obj)
            %% Load Multiple Images for Analysis
            [files, path] = uigetfile(...
                {'*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff', 'Image Files'}, ...
                'Select Images', 'MultiSelect', 'on');
            
            if isequal(files, 0)
                return;
            end
            
            if ~iscell(files)
                files = {files};
            end
            
            obj.image_paths = {};
            obj.images = {};
            obj.lab_images = {};
            
            for i = 1:length(files)
                filename = fullfile(path, files{i});
                try
                    img = imread(filename);
                    if ndims(img) == 3
                        obj.image_paths{end+1} = filename;
                        obj.images{end+1} = img;
                        obj.lab_images{end+1} = obj.rgb_to_lab_colorspace(img);
                    end
                catch ME
                    fprintf('Failed to load image: %s (%s)\n', filename, ME.message);
                end
            end
            
            if ~isempty(obj.images)
                obj.current_index = 1;
                obj.display_current_image();
                obj.update_threshold();
            end
        end
        
        function lab_img = rgb_to_lab_colorspace(obj, rgb_img)
            %% Convert RGB to LAB Color Space
            % implements custom LAB color space conversion required for the
            % specific camera hardware used in the project
            
            % Convert to double for calculations
            rgb = im2double(rgb_img);
            
            % Apply standard RGB Quantization
            r_quant = round(rgb(:,:,1) * 31);
            g_quant = round(rgb(:,:,2) * 63);
            b_quant = round(rgb(:,:,3) * 31);
            
            % Expand back to 0-255 range
            R = (r_quant * 255 + 15.5) / 31;
            G = (g_quant * 255 + 31.5) / 63;
            B = (b_quant * 255 + 15.5) / 31;
            
            % Convert to XYZ
            R_lin = obj.gamma_correction(R / 255);
            G_lin = obj.gamma_correction(G / 255);
            B_lin = obj.gamma_correction(B / 255);
            
            X = 0.4124 * R_lin + 0.3576 * G_lin + 0.1805 * B_lin;
            Y = 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin;
            Z = 0.0193 * R_lin + 0.1192 * G_lin + 0.9505 * B_lin;
            
            % Normalize and convert to LAB
            X = X / 0.95047;
            Z = Z / 1.08883;
            
            % LAB conversion
            L = 116 * obj.lab_f(Y) - 16;
            a = 500 * (obj.lab_f(X) - obj.lab_f(Y));
            b = 200 * (obj.lab_f(Y) - obj.lab_f(Z));
            
            % Scale to standard LAB ranges
            L = int16(round(L));
            a = int16(round(a));
            b = int16(round(b));
            
            lab_img = cat(3, L, a, b);
        end
        
        function result = gamma_correction(~, c)
            %% Gamma Correction for Linearization
            result = zeros(size(c));
            mask = c <= 0.04045;
            result(mask) = c(mask) / 12.92;
            result(~mask) = ((c(~mask) + 0.055) / 1.055) .^ 2.4;
        end
        
        function result = lab_f(~, t)
            %% LAB Conversion Helper Function
            result = zeros(size(t));
            mask = t > 0.008856;
            result(mask) = t(mask) .^ (1/3);
            result(~mask) = 7.787 * t(~mask) + 16/116;
        end
        
        function display_current_image(obj)
            %% Display Current Image in UI (Auto-scaled to fit each image individually to manage different image dimensions in the same window)
            if isempty(obj.images)
                return;
            end
            
            obj.original_img = obj.images{obj.current_index};
            obj.lab_img = obj.lab_images{obj.current_index};
            
            % Clear and display original image with individual auto-scaling
            cla(obj.orig_axes);
            
            % Get axes dimensions for proper scaling
            axes_pos = obj.orig_axes.Position;
            axes_width = axes_pos(3);
            axes_height = axes_pos(4);
            
            % Get image dimensions
            [img_height, img_width, ~] = size(obj.original_img);
            
            % Calculate scaling to fit image within axes while maintaining aspect ratio
            width_ratio = axes_width / img_width;
            height_ratio = axes_height / img_height;
            scale_ratio = min(width_ratio, height_ratio);
            
            % Calculate display dimensions
            display_width = img_width * scale_ratio;
            display_height = img_height * scale_ratio;
            
            % Display image with calculated dimensions
            imshow(obj.original_img, 'Parent', obj.orig_axes);
            
            % Set axes limits to ensure proper display
            xlim(obj.orig_axes, [0.5, img_width + 0.5]);
            ylim(obj.orig_axes, [0.5, img_height + 0.5]);
            
            % Set axes position to center the image
            obj.orig_axes.Position(3) = display_width;
            obj.orig_axes.Position(4) = display_height;
            obj.orig_axes.Position(1) = (axes_pos(1) + (axes_width - display_width) / 2);
            obj.orig_axes.Position(2) = (axes_pos(2) + (axes_height - display_height) / 2);
            
            % Disable axes interactivity to prevent moving
            obj.orig_axes.Interactions = [];
            disableDefaultInteractivity(obj.orig_axes);
            
            title(obj.orig_axes, sprintf('Original Image %d/%d', ...
                obj.current_index, length(obj.images)));
            
            % Store image dimensions for ROI boundary checking
            obj.image_scale = [size(obj.original_img, 2), size(obj.original_img, 1)];
            
            % Update image info
            [~, name, ext] = fileparts(obj.image_paths{obj.current_index});
            info_text = sprintf('%s%s\n%dx%d pixels', ...
                name, ext, size(obj.original_img, 2), size(obj.original_img, 1));
            obj.image_info.Text = info_text;
            
            % Display current ROI for active color
            obj.display_current_roi();
        end
        
        function display_current_roi(obj)
            %% Display ROI for current active color
            if obj.roi_active(obj.active_color) && ~isempty(obj.roi_rect{obj.active_color})
                hold(obj.orig_axes, 'on');
                % Remove existing ROI handles for this color
                if ~isempty(obj.roi_handles{obj.active_color}) && isvalid(obj.roi_handles{obj.active_color})
                    delete(obj.roi_handles{obj.active_color});
                end
                
                % Draw new ROI rectangle
                obj.roi_handles{obj.active_color} = rectangle(obj.orig_axes, ...
                    'Position', obj.roi_rect{obj.active_color}, ...
                    'EdgeColor', obj.color_rgb(obj.active_color, :), ...
                    'LineWidth', 2, ...
                    'LineStyle', '--');
                hold(obj.orig_axes, 'off');
            end
        end
        
        function slider_changed(obj, ~, ~, ~)
            %% Handle slider changes with immediate update
            if ~isempty(obj.lab_img)
                % Update the threshold value immediately
                obj.update_threshold();
            end
        end
        
        function update_threshold(obj)
            %% Update Threshold Display Based on Current Settings
            if isempty(obj.lab_img)
                return;
            end
            
            % Get current thresholds
            l_min = obj.sliders.l_min.Value;
            l_max = obj.sliders.l_max.Value;
            a_min = obj.sliders.a_min.Value;
            a_max = obj.sliders.a_max.Value;
            b_min = obj.sliders.b_min.Value;
            b_max = obj.sliders.b_max.Value;
            
            % Store in thresholds array for active color
            obj.thresholds(obj.active_color).l_min = l_min;
            obj.thresholds(obj.active_color).l_max = l_max;
            obj.thresholds(obj.active_color).a_min = a_min;
            obj.thresholds(obj.active_color).a_max = a_max;
            obj.thresholds(obj.active_color).b_min = b_min;
            obj.thresholds(obj.active_color).b_max = b_max;
            
            % Apply threshold
            L = obj.lab_img(:,:,1);
            A = obj.lab_img(:,:,2);
            B = obj.lab_img(:,:,3);
            
            mask = (L >= l_min) & (L <= l_max) & ...
                   (A >= a_min) & (A <= a_max) & ...
                   (B >= b_min) & (B <= b_max);
            
            % Create highlighted image
            highlighted = obj.original_img;
            color_vec = reshape(obj.color_rgb(obj.active_color, :), 1, 1, 3);
            color_mask = repmat(uint8(round(color_vec * 255)), size(highlighted,1), size(highlighted,2), 1);
            
            for c = 1:3
                channel = highlighted(:,:,c);
                cm = color_mask(:,:,c);
                % Blend with 50% weight safely, preserving uint8
                tmp = double(channel);
                tmp(mask) = tmp(mask) * 0.5 + double(cm(mask)) * 0.5;
                channel = uint8(round(tmp));
                highlighted(:,:,c) = channel;
            end
            
            % Display result
            imshow(highlighted, 'Parent', obj.thresh_axes);
            title(obj.thresh_axes, sprintf('Threshold Result - %s', ...
                obj.color_names{obj.active_color}));
            
            % Update threshold display with formatted text
            threshold_text = {
                sprintf('L: (%3d, %3d)', l_min, l_max), ...
                sprintf('A: (%3d, %3d)', a_min, a_max), ...
                sprintf('B: (%3d, %3d)', b_min, b_max)
                };
            obj.threshold_display.Value = threshold_text;
            
            % Update statistics
            obj.update_statistics(mask);
        end
        
        function update_statistics(obj, mask)
            %% Update Statistics Display
            if isempty(obj.lab_img)
                return;
            end
            
            L = obj.lab_img(:,:,1);
            A = obj.lab_img(:,:,2);
            B = obj.lab_img(:,:,3);
            
            masked_L = double(L(mask));
            masked_A = double(A(mask));
            masked_B = double(B(mask));
            
            if isempty(masked_L)
                stats_text = {'No pixels in threshold range'};
            else
                total_pixels = numel(L);
                masked_pixels = numel(masked_L);
                stats_text = {
                    sprintf('L: %5.1f to %5.1f (mean: %5.1f)', min(masked_L), max(masked_L), mean(masked_L)), ...
                    sprintf('A: %5.1f to %5.1f (mean: %5.1f)', min(masked_A), max(masked_A), mean(masked_A)), ...
                    sprintf('B: %5.1f to %5.1f (mean: %5.1f)', min(masked_B), max(masked_B), mean(masked_B)), ...
                    sprintf('Pixels: %d / %d (%.1f%%)', masked_pixels, total_pixels, masked_pixels/total_pixels*100)
                    };
            end
            
            obj.stats_display.Value = stats_text;
        end
        
        function set_active_color(obj, color_idx)
            %% Set Active Color for Thresholding with ROIs per color
            obj.active_color = color_idx;
            
            % Highlight the active color button
            for i = 1:length(obj.color_buttons)
                if i == color_idx
                    obj.color_buttons(i).FontWeight = 'bold';
                    obj.color_buttons(i).FontSize = 10;
                    obj.color_buttons(i).BackgroundColor = obj.color_rgb(i, :) * 0.8; % Darker for active
                else
                    obj.color_buttons(i).FontWeight = 'normal';
                    obj.color_buttons(i).FontSize = 9;
                    obj.color_buttons(i).BackgroundColor = obj.color_rgb(i, :);
                end
            end
            
            % Update sliders to match current color's thresholds
            obj.sliders.l_min.Value = obj.thresholds(color_idx).l_min;
            obj.sliders.l_max.Value = obj.thresholds(color_idx).l_max;
            obj.sliders.a_min.Value = obj.thresholds(color_idx).a_min;
            obj.sliders.a_max.Value = obj.thresholds(color_idx).a_max;
            obj.sliders.b_min.Value = obj.thresholds(color_idx).b_min;
            obj.sliders.b_max.Value = obj.thresholds(color_idx).b_max;
            
            % Display ROI for the new active color
            obj.display_current_roi();
            
            obj.update_threshold();
        end

        function select_roi(obj)
            %% Select Region of Interest for Auto-Threshold with boundary checking
            if isempty(obj.original_img)
                msgbox('Please load an image first.');
                return;
            end
            
            % Display instruction
            title(obj.orig_axes, 'Draw ROI Rectangle - Release mouse when done');
            
            % Allow user to draw rectangle with boundary constraints
            try
                % Get image boundaries
                img_width = size(obj.original_img, 2);
                img_height = size(obj.original_img, 1);
                
                % Create constrained rectangle
                h = drawrectangle(obj.orig_axes, ...
                    'DrawingArea', [0, 0, img_width, img_height], ...
                    'Label', 'Drag to position, then press Enter');
                

                obj.roi_rect{obj.active_color} = h.Position;
                obj.roi_active(obj.active_color) = true;
                
                % Ensure ROI is within bounds (safety check)
                rect = obj.roi_rect{obj.active_color};
                rect(1) = max(0, min(rect(1), img_width - rect(3)));
                rect(2) = max(0, min(rect(2), img_height - rect(4)));
                rect(3) = max(1, min(rect(3), img_width - rect(1)));
                rect(4) = max(1, min(rect(4), img_height - rect(2)));
                obj.roi_rect{obj.active_color} = rect;
                
                % Display the ROI
                obj.display_current_roi();
                
                title(obj.orig_axes, sprintf('ROI Selected for %s - Image %d/%d', ...
                    obj.color_names{obj.active_color}, obj.current_index, length(obj.images)));
                
                % Auto-threshold on the ROI
                obj.auto_threshold_roi();
                
                delete(h);
                
            catch ME
                title(obj.orig_axes, 'ROI Selection Failed');
                obj.roi_active(obj.active_color) = false;
            end
        end

        function auto_threshold_roi(obj)
            %% Auto-Threshold Based on Selected ROI for current color
            if ~obj.roi_active(obj.active_color) || isempty(obj.roi_rect{obj.active_color}) || isempty(obj.lab_img)
                return;
            end
            
            % Extract ROI from LAB image
            rect = obj.roi_rect{obj.active_color};
            x = round(rect(1));
            y = round(rect(2));
            w = round(rect(3));
            h = round(rect(4));
            
            % Ensure ROI is within image bounds
            [img_h, img_w, ~] = size(obj.lab_img);
            x = max(1, min(x, img_w));
            y = max(1, min(y, img_h));
            w = max(1, min(w, img_w - x + 1));
            h = max(1, min(h, img_h - y + 1));
            
            roi_L = double(obj.lab_img(y:y+h-1, x:x+w-1, 1));
            roi_A = double(obj.lab_img(y:y+h-1, x:x+w-1, 2));
            roi_B = double(obj.lab_img(y:y+h-1, x:x+w-1, 3));
            
            % Calculate thresholds with some margin
            l_min = max(0, floor(prctile(roi_L(:), 5)));
            l_max = min(100, ceil(prctile(roi_L(:), 95)));
            a_min = max(-128, floor(prctile(roi_A(:), 5)));
            a_max = min(127, ceil(prctile(roi_A(:), 95)));
            b_min = max(-128, floor(prctile(roi_B(:), 5)));
            b_max = min(127, ceil(prctile(roi_B(:), 95)));
            
            % Update sliders
            obj.sliders.l_min.Value = l_min;
            obj.sliders.l_max.Value = l_max;
            obj.sliders.a_min.Value = a_min;
            obj.sliders.a_max.Value = a_max;
            obj.sliders.b_min.Value = b_min;
            obj.sliders.b_max.Value = b_max;
            
            obj.update_threshold();
        end
        
        function auto_threshold(obj)
            %% Automatically Calculate Thresholds (use drawn ROI for current color if available)
            if isempty(obj.lab_img)
                return;
            end
            
            if obj.roi_active(obj.active_color) && ~isempty(obj.roi_rect{obj.active_color})
                % Use ROI for current active color
                obj.auto_threshold_roi();
            else
                % Use full image
                L = double(obj.lab_img(:,:,1));
                A = double(obj.lab_img(:,:,2));
                B = double(obj.lab_img(:,:,3));
                
                % Use percentiles for robust threshold estimation
                l_min = max(0, floor(prctile(L(:), 10)));
                l_max = min(100, ceil(prctile(L(:), 90)));
                a_min = max(-128, floor(prctile(A(:), 10)));
                a_max = min(127, ceil(prctile(A(:), 90)));
                b_min = max(-128, floor(prctile(B(:), 10)));
                b_max = min(127, ceil(prctile(B(:), 90)));
                
                % Update sliders
                obj.sliders.l_min.Value = l_min;
                obj.sliders.l_max.Value = l_max;
                obj.sliders.a_min.Value = a_min;
                obj.sliders.a_max.Value = a_max;
                obj.sliders.b_min.Value = b_min;
                obj.sliders.b_max.Value = b_max;
                
                obj.update_threshold();
            end
        end
        
        function copy_thresholds(obj)
            %% Copy Current Thresholds to Clipboard
            th = obj.thresholds(obj.active_color);
            threshold_str = sprintf('(%d, %d, %d, %d, %d, %d)', ...
                th.l_min, th.l_max, th.a_min, th.a_max, th.b_min, th.b_max);
            
            clipboard('copy', threshold_str);
            msgbox(sprintf('Thresholds for %s copied to clipboard:\n%s', ...
                obj.color_names{obj.active_color}, threshold_str), ...
                'Thresholds Copied');
        end
        
        function reset_thresholds(obj)
            %% Reset Current Color Thresholds to Default Values
            obj.thresholds(obj.active_color) = struct(...
                'l_min', 0, 'l_max', 100, ...
                'a_min', -128, 'a_max', 127, ...
                'b_min', -128, 'b_max', 127);
            
            obj.set_active_color(obj.active_color);
        end
        
        function clear_roi(obj)
            %% Clear ROI Selection for current color
            obj.roi_active(obj.active_color) = false;
            obj.roi_rect{obj.active_color} = [];
            
            % Clear any drawn rectangles for current color
            if ~isempty(obj.roi_handles{obj.active_color}) && isvalid(obj.roi_handles{obj.active_color})
                delete(obj.roi_handles{obj.active_color});
                obj.roi_handles{obj.active_color} = [];
            end
            
            % Refresh display
            obj.display_current_image();
        end
        
        function prev_image(obj)
            %% Navigate to Previous Image
            if length(obj.images) > 1
                obj.current_index = mod(obj.current_index - 2, length(obj.images)) + 1;
                obj.display_current_image();
                obj.update_threshold();
            end
        end
        
        function next_image(obj)
            %% Navigate to Next Image
            if length(obj.images) > 1
                obj.current_index = mod(obj.current_index, length(obj.images)) + 1;
                obj.display_current_image();
                obj.update_threshold();
            end
        end
    end
end