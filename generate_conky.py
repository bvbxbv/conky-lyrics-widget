#!/usr/bin/env python3
import tomli
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "configs" / "settings.toml", "rb") as f:
    settings = tomli.load(f)

cfg = settings

conky_conf = f"""
conky.config = {{
	alignment = '{cfg['window']['alignment']}',
	gap_x = {cfg['window']['gap_x']},
	gap_y = {cfg['window']['gap_y']},
	minimum_height = {cfg['window']['height']},
	minimum_width = {cfg['window']['width']},
	maximum_width = {cfg['window']['max_width']},
	background = {str(cfg['window']['background']).lower()},
	border_width = {cfg['window']['border_width']},
	own_window = {str(cfg['window']['own_window']).lower()},
	own_window_class = '{cfg['window']['own_window_class']}',
	own_window_type = '{cfg['window']['own_window_type']}',
	own_window_transparent = {str(cfg['window']['transparent']).lower()},
	own_window_argb_visual = {str(cfg['window']['argb_visual']).lower()},
	own_window_argb_value = {cfg['window']['argb_value']},
	own_window_colour = '{cfg['window']['bg_color']}',
	default_color = '{cfg['colors']['default']}',
	double_buffer = true,
	draw_borders = false,
	draw_graph_borders = true,
	draw_outline = false,
	draw_shades = false,
	extra_newline = false,
	update_interval = {cfg['system']['update_interval']},
	cpu_avg_samples = {cfg['system']['cpu_avg_samples']},
	net_avg_samples = {cfg['system']['net_avg_samples']},
	use_xft = true,
	font = '{cfg['fonts']['main']}'
}}

conky.text = [[
${{voffset 30}}
${{goto 6}}${{color {cfg['colors']['accent']}}}${{font {cfg['fonts']['header']}}}  {cfg['sections']['music_section_title']}${{font}}

#current song
${{goto 20}}${{color {cfg['colors']['accent_dimmed']}}}${{execi {cfg['intervals']['title_update_interval']} bash -c '
track=$(playerctl metadata --format "{{{{artist}}}} - {{{{title}}}}" 2>/dev/null || echo "{cfg['display']['player_idle']}");
if [ ${{#track}} -gt {cfg['music']['title_max_length']} ]; then
	track="${{track:0:{cfg['music']['title_max_length']}}}…"
fi
echo "$track"
'}}${{goto 385}}${{execi {cfg['intervals']['time_update_interval']} bash -c 'pos=$(playerctl position 2>/dev/null || echo 0); pos=${{pos%.*}}; printf "%02d:%02d" $((pos/60)) $((pos%60))'}}{cfg['display']['timer_delimiter']}${{execi {cfg['intervals']['time_update_interval']} bash -c 'len=$(playerctl metadata mpris:length 2>/dev/null || echo 0); sec=$((len/1000000)); printf "%02d:%02d" $((sec/60)) $((sec%60))'}}${{color}}

# lyrics
${{execi {cfg['intervals']['lyrics_update_interval']} sh -c 'playerctl metadata --format "{{{{artist}}}} {{{{title}}}}" | python3 {BASE_DIR}/scripts/run.py | head -n 43'}}
# system info
${{goto 10}}-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

${{goto 24}}${{color {cfg['colors']['accent']}}} System ${{voffset 8}}
${{goto 24}}OS:        ${{color {cfg['colors']['accent_dimmed']}}}$sysname $nodename $machine  ${{alignr}}${{color {cfg['colors']['accent']}}}
${{goto 24}}Kernel:    ${{color {cfg['colors']['accent_dimmed']}}}$kernel
${{goto 24}}Uptime:    ${{color {cfg['colors']['accent_dimmed']}}}$uptime

${{goto 24}}${{color {cfg['colors']['accent']}}} Memory ${{voffset 8}}
${{goto 24}}${{color {cfg['colors']['accent_dimmed']}}}RAM:  $mem/$memmax ${{alignr}}$memperc% ${{color {cfg['colors']['accent']}}}${{membar 4, 124}}
${{goto 24}}Swap: ${{color {cfg['colors']['accent_dimmed']}}}$swap/$swapmax ${{alignr}}$swapperc% ${{color {cfg['colors']['accent']}}}${{swapbar 4, 124}}${{voffset 8}}

${{goto 24}}{cfg['sections']['cpu_section_title']}${{voffset 8}}
${{goto 24}}0: ${{freq_g 1}}GHz ${{color {cfg['colors']['accent_dimmed']}}}${{alignr}}${{cpu cpu0}}% ${{color {cfg['colors']['accent']}}}${{cpubar cpu0 4, 124}}
${{goto 24}}1: ${{freq_g 2}}GHz ${{color {cfg['colors']['accent_dimmed']}}}${{alignr}}${{cpu cpu1}}% ${{color {cfg['colors']['accent']}}}${{cpubar cpu1 4, 124}}
${{goto 24}}2: ${{freq_g 3}}GHz ${{color {cfg['colors']['accent_dimmed']}}}${{alignr}}${{cpu cpu2}}% ${{color {cfg['colors']['accent']}}}${{cpubar cpu2 4, 124}}
${{goto 24}}3: ${{freq_g 4}}GHz ${{color {cfg['colors']['accent_dimmed']}}}${{alignr}}${{cpu cpu3}}% ${{color {cfg['colors']['accent']}}}${{cpubar cpu3 4, 124}}${{voffset 8}}
${{goto 24}}${{color {cfg['colors']['accent']}}}${{cpugraph 30, 420}}
]]
"""

with open(BASE_DIR / "conky.conf", "w") as f:
    f.write(conky_conf)
