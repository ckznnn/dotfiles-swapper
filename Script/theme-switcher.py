#!/usr/bin/env python3
"""
Theme Switcher GUI  —  GTK 3
Reads the active GTK3 theme name, shows a wallpaper preview card for each
dotfile theme, and runs the chosen script on click.
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk, Pango

import subprocess
import os
import threading
from pathlib import Path
import math

# ── Theme definitions ──────────────────────────────────────────────────────────
THEMES = [
    {
        "id":        "gruvbox-dark",
        "name":      "Gruvbox Dark",
        "script":    "~/dotfiles-swapper/Script/gruvbox-dark.sh",
        "wallpaper": "~/dotfiles-swapper/Wallpapers/gruvbox-dark.png",
        "palette":   ["#282828", "#cc241d", "#98971a", "#d79921",
                      "#458588", "#b16286", "#689d6a", "#ebdbb2"],
        "fg":        "#ebdbb2",
        "bg":        "#282828",
    },
    {
        "id":        "gruvbox-light",
        "name":      "Gruvbox Light",
        "script":    "~/dotfiles-swapper/Script/gruvbox-light.sh",
        "wallpaper": "~/dotfiles-swapper/Wallpapers/gruvbox-light.png",
        "palette":   ["#fbf1c7", "#cc241d", "#98971a", "#d79921",
                      "#458588", "#b16286", "#689d6a", "#3c3836"],
        "fg":        "#3c3836",
        "bg":        "#fbf1c7",
    },
    {
        "id":        "everforest-dark",
        "name":      "Everforest Dark",
        "script":    "~/dotfiles-swapper/Script/everforest-dark.sh",
        "wallpaper": "~/dotfiles-swapper/Wallpapers/everforest-dark.png",
        "palette":   ["#2d353b", "#e67e80", "#a7c080", "#dbbc7f",
                      "#7fbbb3", "#d699b6", "#83c092", "#d3c6aa"],
        "fg":        "#d3c6aa",
        "bg":        "#2d353b",
    },
    {
        "id":        "tokyonight",
        "name":      "Tokyo Night",
        "script":    "~/dotfiles-swapper/Script/tokyonight.sh",
        "wallpaper": "~/dotfiles-swapper/Wallpapers/tokyonight.png",
        "palette":   ["#1a1b26", "#f7768e", "#9ece6a", "#e0af68",
                      "#7aa2f7", "#bb9af7", "#7dcfff", "#c0caf5"],
        "fg":        "#c0caf5",
        "bg":        "#1a1b26",
    },
]


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_gtk_theme_name() -> str:
    """Read the active GTK3 theme from gsettings."""
    try:
        r = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            capture_output=True, text=True, timeout=3,
        )
        return r.stdout.strip().strip("'")
    except Exception:
        return "Unknown"


def rgba_from_hex(hex_color: str) -> Gdk.RGBA:
    rgba = Gdk.RGBA()
    rgba.parse(hex_color)
    return rgba


def sc(widget, *css_classes):
    """Shorthand: add CSS classes to a widget's style context."""
    ctx = widget.get_style_context()
    for cls in css_classes:
        ctx.add_class(cls)


# ── Palette swatch (Cairo DrawingArea) ────────────────────────────────────────
class PaletteSwatch(Gtk.DrawingArea):
    def __init__(self, colours: list):
        super().__init__()
        self._colours = colours
        self.set_size_request(-1, 26)
        self.connect("draw", self._on_draw)

    def _on_draw(self, _widget, cr):
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        n = len(self._colours)
        if n == 0:
            return
        sw = w / n
        r = 5
        for i, hex_c in enumerate(self._colours):
            rgba = rgba_from_hex(hex_c)
            cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, 1.0)
            x = i * sw
            if i == 0:
                # rounded left corners
                cr.new_path()
                cr.move_to(x + r, 0)
                cr.line_to(x + sw, 0)
                cr.line_to(x + sw, h)
                cr.line_to(x + r, h)
                cr.arc(x + r, h - r, r, math.pi / 2, math.pi)
                cr.arc(x + r, r,     r, math.pi,     3 * math.pi / 2)
                cr.close_path()
            elif i == n - 1:
                # rounded right corners
                cr.new_path()
                cr.move_to(x, 0)
                cr.line_to(x + sw - r, 0)
                cr.arc(x + sw - r, r,     r, -math.pi / 2, 0)
                cr.arc(x + sw - r, h - r, r, 0,            math.pi / 2)
                cr.line_to(x, h)
                cr.close_path()
            else:
                cr.rectangle(x, 0, sw, h)
            cr.fill()


# ── Fallback colour preview (no wallpaper found) ───────────────────────────────
class ColourPreview(Gtk.DrawingArea):
    def __init__(self, bg: str, fg: str, name: str):
        super().__init__()
        self._bg   = bg
        self._fg   = fg
        self._name = name
        self.set_size_request(300, 169)
        self.connect("draw", self._on_draw)

    def _on_draw(self, _widget, cr):
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        bg = rgba_from_hex(self._bg)
        cr.set_source_rgba(bg.red, bg.green, bg.blue, 1)
        cr.paint()
        fg = rgba_from_hex(self._fg)
        cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.13)
        import cairo as _cairo
        cr.select_font_face("monospace",
                            _cairo.FONT_SLANT_NORMAL,
                            _cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(28)
        te = cr.text_extents(self._name)
        cr.move_to((w - te.width)  / 2 - te.x_bearing,
                   (h + te.height) / 2 - te.y_bearing - te.height)
        cr.show_text(self._name)


# ── Individual theme card ──────────────────────────────────────────────────────
class ThemeCard(Gtk.Box):
    def __init__(self, theme: dict, on_apply):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        sc(self, "theme-card")
        self.set_hexpand(True)

        # ── Preview image or colour fallback ───────────────────────────────────
        wp_path = Path(os.path.expanduser(theme["wallpaper"]))
        if wp_path.exists():
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    str(wp_path), 300, 169, True
                )
                img = Gtk.Image.new_from_pixbuf(pb)
                img.set_size_request(300, 169)
                preview = img
            except Exception:
                preview = ColourPreview(theme["bg"], theme["fg"], theme["name"])
        else:
            preview = ColourPreview(theme["bg"], theme["fg"], theme["name"])

        # Wrap in an EventBox so the frame border renders nicely
        preview_wrap = Gtk.EventBox()
        sc(preview_wrap, "preview-wrap")
        preview_wrap.add(preview)
        self.pack_start(preview_wrap, False, False, 0)

        # ── Palette strip ──────────────────────────────────────────────────────
        swatch = PaletteSwatch(theme["palette"])
        sc(swatch, "palette-strip")
        self.pack_start(swatch, False, False, 0)

        # ── Footer: name + button ──────────────────────────────────────────────
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sc(footer, "card-footer")
        footer.set_hexpand(True)

        lbl = Gtk.Label(label=theme["name"])
        sc(lbl, "theme-name")
        lbl.set_halign(Gtk.Align.START)
        lbl.set_hexpand(True)
        lbl.set_ellipsize(Pango.EllipsizeMode.END)
        footer.pack_start(lbl, True, True, 0)

        btn = Gtk.Button(label="Apply")
        sc(btn, "apply-btn")
        btn.connect("clicked", lambda _: on_apply(theme))
        footer.pack_end(btn, False, False, 0)

        self.pack_start(footer, False, False, 0)


# ── Main window ────────────────────────────────────────────────────────────────
class ThemeSwitcherWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Theme Switcher")
        self.set_default_size(960, 600)
        self.set_border_width(0)
        self.connect("destroy", Gtk.main_quit)

        self._gtk_theme = get_gtk_theme_name()
        self._load_css()
        self._build_ui()

    # ── CSS (GTK3 variables: @theme_bg_color, @theme_fg_color, etc.) ──────────
    def _load_css(self):
        css = b"""
        /* GTK3 themes expose @theme_bg_color, @theme_fg_color,
           @theme_base_color, @theme_selected_bg_color etc.
           We use these so the UI inherits whatever theme is active.    */

        window {
            background-color: @theme_bg_color;
        }

        .header-area {
            padding: 10px 18px;
            background-color: @theme_bg_color;
        }

        .app-title {
            font-size: 17px;
            font-weight: bold;
            color: @theme_fg_color;
        }

        .gtk-badge {
            font-size: 11px;
            color: alpha(@theme_fg_color, 0.55);
            padding: 2px 10px;
            border-radius: 99px;
            background-color: alpha(@theme_fg_color, 0.08);
            border: 1px solid alpha(@theme_fg_color, 0.15);
        }

        .cards-viewport {
            background-color: @theme_bg_color;
        }

        .cards-area {
            background-color: @theme_bg_color;
            padding: 20px;
        }

        .theme-card {
            background-color: @theme_base_color;
            border-radius: 12px;
            border: 1px solid alpha(@theme_fg_color, 0.12);
        }

        .preview-wrap {
            border-radius: 12px 12px 0 0;
        }

        .palette-strip {
            margin: 0;
        }

        .card-footer {
            padding: 9px 11px;
            background-color: @theme_base_color;
            border-radius: 0 0 12px 12px;
        }

        .theme-name {
            font-size: 13px;
            font-weight: bold;
            color: @theme_fg_color;
        }

        .apply-btn {
            font-size: 12px;
            font-weight: bold;
            padding: 3px 14px;
            border-radius: 99px;
            background-color: @theme_selected_bg_color;
            color: @theme_selected_fg_color;
            border: none;
        }

        .apply-btn:hover {
            background-color: shade(@theme_selected_bg_color, 1.1);
        }

        .apply-btn:active {
            background-color: shade(@theme_selected_bg_color, 0.9);
        }

        .status-bar {
            padding: 5px 20px;
            font-size: 11px;
            color: alpha(@theme_fg_color, 0.5);
            border-top: 1px solid alpha(@theme_fg_color, 0.1);
            background-color: @theme_bg_color;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    # ── UI ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        sc(header, "header-area")

        title = Gtk.Label(label="Theme Switcher")
        sc(title, "app-title")
        title.set_halign(Gtk.Align.START)
        header.pack_start(title, True, True, 0)

        badge = Gtk.Label(label=f"GTK theme: {self._gtk_theme}")
        sc(badge, "gtk-badge")
        header.pack_end(badge, False, False, 0)

        root.pack_start(header, False, False, 0)
        root.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL),
                        False, False, 0)

        # Scrollable card grid
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        sc(scroll, "cards-viewport")

        flow = Gtk.FlowBox()
        sc(flow, "cards-area")
        flow.set_selection_mode(Gtk.SelectionMode.NONE)
        flow.set_max_children_per_line(4)
        flow.set_min_children_per_line(1)
        flow.set_column_spacing(16)
        flow.set_row_spacing(16)
        flow.set_homogeneous(True)
        flow.set_hexpand(True)

        for theme in THEMES:
            card = ThemeCard(theme, self._apply_theme)
            flow.add(card)

        scroll.add(flow)
        root.pack_start(scroll, True, True, 0)

        # Status bar
        self._status = Gtk.Label(label="Select a theme to apply it.")
        sc(self._status, "status-bar")
        self._status.set_halign(Gtk.Align.START)
        root.pack_start(self._status, False, False, 0)

        self.show_all()

    # ── Apply theme (runs script in background thread) ─────────────────────────
    def _apply_theme(self, theme: dict):
        script = os.path.expanduser(theme["script"])
        self._set_status(f"Applying {theme['name']}…")

        def run():
            try:
                result = subprocess.run(
                    ["bash", script],
                    capture_output=True, text=True, timeout=30,
                )
                if result.returncode == 0:
                    GLib.idle_add(self._set_status,
                                  f"✓  {theme['name']} applied successfully.")
                else:
                    err = result.stderr.strip() or "unknown error"
                    GLib.idle_add(self._set_status,
                                  f"✗  Error: {err}")
            except FileNotFoundError:
                GLib.idle_add(self._set_status,
                              f"✗  Script not found: {script}")
            except subprocess.TimeoutExpired:
                GLib.idle_add(self._set_status,
                              f"✗  Timed out running {theme['name']}")

        threading.Thread(target=run, daemon=True).start()

    def _set_status(self, msg: str):
        self._status.set_text(msg)


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    win = ThemeSwitcherWindow()
    Gtk.main()


if __name__ == "__main__":
    main()
